import itertools
import hashlib
import pypipegraph as ppg
import numpy as np
import pandas as pd
from pandas import DataFrame
from mbf.genomics import DelayedDataFrame
from mbf.qualitycontrol import register_qc, qc_disabled
from mbf.genomics.util import parse_a_or_c_to_anno
from mbf.genomics.annotator import Annotator
from typing import List, Dict, Tuple, Any
from pypipegraph import Job
import dppd
import dppd_plotnine  # noqa: F401

dp, X = dppd.dppd()

# import pypipegraph as ppg


class ComparisonAnnotator(Annotator):
    def __init__(
        self,
        comparisons,
        group_a,
        group_b,
        comparison_strategy,
        laplace_offset=1 / 1e6,
        other_groups_for_variance=[],
    ):
        """Create a comparison (a - b)"""
        self.comparisons = comparisons

        if hasattr(comparison_strategy, "__call__"):
            self.comparison_strategy = comparison_strategy()
        else:
            self.comparison_strategy = comparison_strategy
        if isinstance(
            self.comparison_strategy.columns, str
        ):  # pragma: no cover definsive
            raise ValueError(
                "ComparisonStrategy %s had a string as columns, must be a list"
                % self.comparison_strategy
            )
        self.comp = (group_a, group_b)
        self.other_groups_for_variance = other_groups_for_variance
        self.columns = []
        self.column_lookup = {}
        for col in sorted(self.comparison_strategy.columns):
            cn = self.name_column(col)
            self.columns.append(cn)
            self.column_lookup[col] = cn
        self.laplace_offset = laplace_offset
        self.result_dir = self.comparisons.result_dir / f"{group_a}_vs_{group_b}"
        self.result_dir.mkdir(exist_ok=True, parents=True)
        self._check_comparison_groups(group_a, group_b)
        if len(self.columns[0]) >= 60:
            self.cache_name = (
                "Comp %s" % hashlib.md5(self.columns[0].encode("utf-8")).hexdigest()
            )
        try:
            self.vid = self._build_vid()
        except AttributeError:  # the sample annotators don't have a vid
            pass

    @classmethod
    def _prep_init_params_for_freezing(cls, *args, **kwargs):
        """collect what we need to freeze in order to singletonize this Annotator"""
        key = {}
        key["arg_0"] = args[0].name  # can't freeze the ddf in the comparison
        for ii in range(1, len(args)):
            key["arg_%i" % ii] = args[ii]
        key["arg_3"] = key["arg_3"].__class__.__name__ + getattr(
            key["arg_3"], "name", "not_an_object_with_name"
        )
        key.update(kwargs)
        return key

    def _build_vid(self):
        a = set()
        b = set()
        all_columns = True
        for s in self.comparisons.groups_to_samples[self.comp[0]]:
            if s[0] is not None:
                a.add(s[0].vid)
                all_columns = False
        for s in self.comparisons.groups_to_samples[self.comp[1]]:
            if s[0] is not None:
                b.add(s[0].vid)
                all_columns = False
        if a or b:
            return sorted(a) + ["vs"] + sorted(b)
        elif all_columns:
            raise AttributeError("No vids - as expected")

    def name_column(self, col):
        if self.comparison_strategy.supports_other_samples:
            supports_other_samples = ",Other=%s" % bool(self.other_groups_for_variance)
        else:
            supports_other_samples = ""
        return f"Comp. {self.comparisons.name} {self.comp[0]} - {self.comp[1]} {col} ({self.comparison_strategy.name}{supports_other_samples})"

    def __getitem__(self, itm):
        """look up the full column name from log2FC, p, FDR, etc"""
        return self.column_lookup[itm]

    def filter(self, filter_definition, new_name=None, sheet_name=None):  # noqa: C901
        """Turn a filter definition [(column, operator, threshold)...]
        into a filtered genes object.

        Example:
        comp.filter(genes, '2x', [
            ('FDR', '<=', 0.05) # a name from our comparison strategy - inspect column_lookup to list
            ('log2FC', '|>', 1),  #absolute
            ...
            (anno, '>=', 50),
            ((anno, 1), '>=', 50),  # for the second column of the annotator
            ((anno, 'columnX'), '>=', 50),  # for the second column of the annotator
            ('annotator_columnX', '=>' 50), # search for an annotator with that column. Use if exactly one, complain otherwise



            ]
        """
        lookup = self.column_lookup.copy()
        for c in self.columns:
            lookup[c] = c

        subset_relevant_columns = set(lookup.values())
        subset_relevant_columns.update(self.sample_columns(self.comp[0]))
        subset_relevant_columns.update(self.sample_columns(self.comp[1]))
        for g in self.other_groups_for_variance:
            subset_relevant_columns.update(self.sample_columns(g))

        further_filters = []
        add_direction = False
        thresholds = {}
        filter_str = []
        for column, op, threshold in sorted(filter_definition):
            if op == "==":
                oop = "＝"
            elif op == ">":
                oop = "＞"
            elif op == "<":
                oop = "＜"
            elif op == ">=":
                oop = "≥"
            elif op == "<=":
                oop = "≤"
            elif op == "|>":
                oop = "|＞"
            elif op == "|<":
                oop = "|＜"
            elif op == "|>=":
                oop = "|≥"
            elif op == "|<=":
                oop = "|≤"
            else:
                oop = op
            filter_str.append(f"{column}_{oop}_{threshold:.2f}")
            if hasattr(column, "columns"):
                subset_relevant_columns.update(column.columns)
            elif isinstance(column, tuple):
                if column[1] is not None:
                    subset_relevant_columns.add(column[1])
                else:
                    subset_relevant_columns.add(column[0].column_names[0])
            else:
                if column in lookup:
                    subset_relevant_columns.add(
                        lookup[column]
                    )  # aren't those in there anyway?
                else:
                    subset_relevant_columns.add(
                        column
                    )  # just presume it's an annotator one
            if column == "log2FC":
                if "|" in op:
                    add_direction = True
            thresholds[column] = threshold

        if isinstance(new_name, str):
            pass
        else:
            filter_str = "__".join(filter_str)
            _new_name = f"Filtered_{self.comparison_strategy.name}_{self.comp[0]}-{self.comp[1]}_{filter_str}"
            if callable(new_name):
                new_name = new_name(_new_name)
            else:
                new_name = _new_name

        if "log2FC" in lookup:
            further_filters.append(
                ("logFC", lookup["log2FC"], 2, thresholds.get("log2FC", 0))
            )
            if add_direction:
                further_filters.append(("Direction", lookup["log2FC"], 1, 0))
        for x in ["p", "FDR"]:  # less than
            if x in lookup:
                further_filters.append((x, lookup[x], 5, thresholds.get(x, 1)))

        for x in ["minExpression"]:  # min of columns > x
            if x in lookup:
                further_filters.append((x, [lookup[x]], 4, thresholds.get(x, 0)))

        # we need the filter func for the plotting, so we do it ourselves
        filter_func, annos = self.comparisons.ddf.definition_to_function(
            filter_definition, lookup
        )
        kwargs = {}
        if hasattr(self, "vid"):
            kwargs["vid"] = self.vid
        res = self.comparisons.ddf.filter(
            new_name,
            filter_func,
            annotators=annos,
            column_lookup=lookup,
            result_dir=(self.result_dir / sheet_name / new_name)
            if sheet_name is not None
            else (self.result_dir / new_name),
            sheet_name=sheet_name,
            **kwargs,
        )
        if not qc_disabled():
            if "p" in self.comparison_strategy.columns:
                self.register_qc_volcano(self.comparisons.ddf, res, filter_func)
            # self.register_qc_ma_plot(self.comparisons.ddf, res, filter_func)
        res.plot_columns = self.samples()
        res.venn_annotator = self
        res.subset_relevant_columns = subset_relevant_columns
        res.further_filter_columns = further_filters
        return res

    def calc(self, df):
        columns_a = list(self.sample_columns(self.comp[0]))
        columns_b = list(self.sample_columns(self.comp[1]))
        columns_other = {}
        for g in self.other_groups_for_variance:
            columns_other[g] = self.sample_columns(g)
        comp = self.comparison_strategy.compare(
            df,
            columns_a,
            columns_b,
            columns_other,
            self.laplace_offset,
        )
        res = {}
        for col in sorted(self.comparison_strategy.columns):
            res[self.name_column(col)] = comp[col]
        return pd.DataFrame(res)

    def dep_annos(self):
        """Return other annotators"""
        res = []
        for generator in [self.samples(), self.other_samples()]:
            for k in generator:
                a = parse_a_or_c_to_anno(k)
                if a is not None:
                    res.append(a)
        return res

    def deps(self, ddf):
        from mbf.genomics.util import freeze

        sample_info = []
        for ac in self.samples():
            group = self.comparisons.sample_column_to_group[ac[1]]
            sample_info.append(
                (group, ac[0].get_cache_name() if ac[0] is not None else "None", ac[1])
            )
        sample_info.sort()
        parameters = freeze(
            [
                (
                    # self.comparison_strategy.__class__.__name__ , handled by column name
                    sample_info,
                    #   self.comp, # his handled by column name
                    self.laplace_offset,
                )
            ]
        )
        res = [ppg.ParameterInvariant(self.get_cache_name(), parameters)]
        res.extend(getattr(self.comparison_strategy, "deps", lambda: [])())
        return res

    def samples(self):
        """Return anno, column for samples used"""
        for x in list(self.comp) + self.other_groups_for_variance:
            for s in self.comparisons.groups_to_samples[x]:
                yield s

    def other_samples(self):
        """Return anno, column for additional samples used for variance"""
        for x in self.other_groups_for_variance:
            for s in self.comparisons.groups_to_samples[x]:
                yield s

    def sample_columns(self, group):
        for s in self.comparisons.groups_to_samples[group]:
            yield s[1]

    def _check_comparison_groups(self, *groups):
        for x in groups:
            if x not in self.comparisons.groups_to_samples:
                raise ValueError(f"Comparison group {x} not found")
            if (
                len(self.comparisons.groups_to_samples[x])
                < self.comparison_strategy.min_sample_count
            ):
                raise ValueError(
                    "Too few samples in %s for %s" % (x, self.comparison_strategy.name)
                )

    def register_qc_volcano(self, genes, filtered=None, filter_func=None):
        """perform a volcano plot"""
        if filtered is None:
            output_filename = genes.result_dir / "volcano.png"
        else:
            output_filename = filtered.result_dir / "volcano.png"

        def plot(output_filename):
            df = (
                dp(genes.df)
                .mutate(
                    significant=filter_func(genes.df)
                    if filter_func is not None
                    else "tbd."
                )
                .pd
            )

            no_sig_lower = (df["significant"] & (df[self["log2FC"]] < 0)).sum()
            no_sig_higher = (df["significant"] & (df[self["log2FC"]] > 0)).sum()

            (
                dp(df)
                .p9()
                .scale_color_many_categories(name="regulated", shift=3)
                .scale_y_continuous(
                    name="p",
                    trans=dp.reverse_transform("log10"),
                    labels=lambda xs: ["%.2g" % x for x in xs],
                )
                .add_vline(xintercept=1, _color="blue")
                .add_vline(xintercept=-1, _color="blue")
                .add_hline(yintercept=0.05, _color="blue")
                .add_rect(  # shade 'simply' significant regions
                    xmin="xmin",
                    xmax="xmax",
                    ymin="ymin",
                    ymax="ymax",
                    _fill="lightgrey",
                    data=pd.DataFrame(
                        {
                            "xmin": [-np.inf, 1],
                            "xmax": [-1, np.inf],
                            "ymin": [0, 0],
                            "ymax": [0.05, 0.05],
                        }
                    ),
                    _alpha=0.8,
                )
                .add_scatter(self["log2FC"], self["p"], color="significant")
                .title(f"# regulated down/ up: {no_sig_lower} / {no_sig_higher}")
                # .coord_trans(x="reverse", y="reverse")  #broken as of 2019-01-31
                .render(output_filename, width=8, height=6, dpi=300)
            )

        return register_qc(
            ppg.FileGeneratingJob(output_filename, plot).depends_on(
                genes.add_annotator(self),
                ppg.FunctionInvariant(
                    str(output_filename) + "_filter_func", filter_func
                ),
            )
        )

    def register_qc_ma_plot(self, genes, filtered, filter_func):
        """perform an MA plot - not a straight annotator.register_qc function,
        but called by .filter
        """
        output_filename = filtered.result_dir / "ma_plot.png"

        def plot(output_filename):
            from statsmodels.nonparametric.smoothers_lowess import lowess

            print(genes.df.columns)
            print(list(self.sample_columns(self.comp[0])))
            print(list(self.sample_columns(self.comp[1])))
            df = genes.df[
                list(self.sample_columns(self.comp[0]))
                + list(self.sample_columns(self.comp[1]))
            ]
            df = df.assign(significant=filter_func(genes.df))
            pdf = []
            loes_pdfs = []
            # Todo: how many times can you over0lopt this?
            for a, b in itertools.combinations(
                [x for x in df.columns if not "significant" == x], 2
            ):
                np_a = np.log2(df[a] + self.laplace_offset)
                np_b = np.log2(df[b] + self.laplace_offset)
                A = (np_a + np_b) / 2
                M = np_a - np_b
                local_pdf = pd.DataFrame(
                    {
                        "A": A,
                        "M": M,
                        "a": self.comparisons.get_plot_name(a),
                        "b": self.comparisons.get_plot_name(b),
                        "significant": df["significant"],
                    }
                ).sort_values("M")
                chosen = np.zeros(len(local_pdf), bool)
                chosen[:500] = True
                chosen[-500:] = True
                chosen[np.random.randint(0, len(chosen), 1000)] = True
                pdf.append(local_pdf)
                fitted = lowess(M, A, is_sorted=False)
                loes_pdfs.append(
                    pd.DataFrame(
                        {
                            "a": self.comparisons.get_plot_name(a),
                            "b": self.comparisons.get_plot_name(b),
                            "A": fitted[:, 0],
                            "M": fitted[:, 1],
                        }
                    )
                )
            pdf = pd.concat(pdf)
            pdf = pdf.assign(ab=[a + ":" + b for (a, b) in zip(pdf["a"], pdf["b"])])
            loes_pdf = pd.concat(loes_pdfs)
            loes_pdf = loes_pdf.assign(
                ab=[a + ":" + b for (a, b) in zip(loes_pdf["a"], loes_pdf["b"])]
            )
            (
                dp(pdf)
                .p9()
                .theme_bw(10)
                .add_hline(yintercept=0, _color="lightblue")
                .add_hline(yintercept=1, _color="lightblue")
                .add_hline(yintercept=-1, _color="lightblue")
                .scale_color_many_categories(name="significant", shift=3)
                .add_point("A", "M", color="significant", _size=1, _alpha=0.3)
                .add_line("A", "M", _color="blue", data=loes_pdf)
                .facet_wrap(["ab"])
                .title(f"MA {filtered.name}\n{self.comparisons.find_variable_name()}")
                .render(output_filename, width=8, height=6)
            )

        return register_qc(
            ppg.FileGeneratingJob(output_filename, plot)
            .depends_on(genes.add_annotator(self))
            .depends_on(self.comparisons.deps)
        )


class ComparisonAnnotatorMulti(ComparisonAnnotator):
    """
    Annotator for multi-factor comparison.

    Based on a main factor and a list of multiple other factor, this
    creates an annotator that annotates DEG analysis results for a multi-factor
    design. Interaction terms may be specified as a list of tuples which may be
    empty.
    if an empty interactions list is provided, the analysis just controls
    for different levels of other_factors and report the main effect.

    Parameters
    ----------
    name : str
        Annotator name, used for cache names and test of uniqueness.
    comparisons : Comparisons
        Comparisons instance containing the groups to be analyzed.
    main_factor : str
        The main factor, e.g. treatment/condition.
    factor_reference : Dict[str, str]
        Dictionary of factor names (key) to base level (value), e.g.
        {"treatment": "DMSO"}.
    groups : List[str]
        Groups to be included in the DE analysis.
    df_factors : DataFrame
        A dataframe containing all groups and factor levels
        relevant for the variance calculation. This may include groups
        beyond the groups of interest. If so, these groups are used for
        estimating dispersion but not reported in the results.
    interactions : List[Tuple[str, str]]
        List if interaction terms. If this is empty, the analysis will
        report the main factor effects controlling for the other factors.
    method : Any
        The DEG method to use, e.g. DESeq2MultiFactor.
    test_difference : bool, optional
        Test for differences in the main effects for different levels
        of other factors, by default True.
    compare_non_reference : bool, optional
        Test for difference of the main effects for different levels of other
        factors compared to non-reference levels, by default False.
    laplace_offset : float, optional
        laplace offset for methods that cannot handle zeros, by default 1/1e6.
    """

    @classmethod
    def _prep_init_params_for_freezing(cls, *args, **kwargs):
        """collect what we need to freeze in order to singletonize this Annotator"""
        for ii, a in enumerate(args):
            print(ii, a)
        key = {}
        for ii in range(0, len(args)):
            key["arg_%i" % ii] = args[ii]
        key["arg_1"] = args[1].name  # can't freeze the ddf in the comparisons argument
        key["arg_7"] = key["arg_7"].__class__.__name__  # comparison_strategy
        key.update(kwargs)
        return key

    def __init__(
        self,
        name: str,
        comparisons: Any,
        main_factor: str,
        factor_reference: Dict[str, str],
        groups: List[str],
        df_factors: DataFrame,
        interactions: List[Tuple[str, str]],
        comparison_strategy: Any,
        test_difference: bool,
        compare_non_reference: bool,
        laplace_offset: float,
    ):
        """Contructor"""
        self.comparisons = comparisons
        if hasattr(comparison_strategy, "__call__"):
            self.comparison_strategy = comparison_strategy()
        else:
            self.comparison_strategy = comparison_strategy
        self.comparison_name = name
        reserved_chars = ":()"
        for factor in factor_reference:
            if any([x in factor for x in reserved_chars]):
                raise ValueError(
                    f"Factor values must not contain any of {list(reserved_chars)}."
                )
            for level in df_factors[factor].unique():
                if any([x in level for x in reserved_chars]):
                    raise ValueError(
                        f"Level values must not contain any of {list(reserved_chars)}."
                    )
        self.columns = []
        self.column_lookup = {}
        self.groups = groups
        prefixes = comparison_strategy.prefixes(
            main_factor,
            factor_reference,
            df_factors,
            interactions,
            test_difference,
            compare_non_reference,
        )
        self.prefixes = prefixes
        for col in comparison_strategy.get_columns(prefixes):
            cn = self.name_column(col)
            self.columns.append(cn)
            self.column_lookup[col] = cn
        self.laplace_offset = laplace_offset
        self.result_dir = self.comparisons.result_dir / f"{self.comparison_name}"
        self.result_dir.mkdir(exist_ok=True, parents=True)
        self.df_factors = df_factors
        self.factor_reference = factor_reference
        self.interactions = interactions
        self.main_factor = main_factor
        self.test_difference = test_difference
        self.compare_non_reference = compare_non_reference
        columns = ["group"] + list(factor_reference.keys())
        df_factors = df_factors[columns]
        self._check_comparison_groups(*self.groups)
        self.cache_name = f"{ComparisonAnnotatorMulti}_{name}"
        if len(self.cache_name) >= 60:
            self.cache_name = (
                "Comp %s" % hashlib.md5(self.cache_name.encode("utf-8")).hexdigest()
            )
        try:
            self.vid = self._build_vid()
        except AttributeError:  # the sample annotators don't have a vid
            pass
        self.other_groups_for_variance = []

    def samples(self):
        """
        Return anno, column for samples used.

        Overrides the parent method, since we now have more than 2 groups to
        be considered.

        Yields
        -------
        Tuple[Annotator, str]
            (Annotator, column_name) for each sample used.
        """
        for group in self.groups:
            for s in self.comparisons.groups_to_samples[group]:
                yield s

    def deps(self, ddf: DelayedDataFrame) -> List[Job]:
        """
        Returns list of dependencies.

        Parameters
        ----------
        ddf : DelayedDataFrame
            The DelayedDataFrame instance to be annotated, e.g. genes.

        Returns
        -------
        List[Job]
            List of jobs this calc_ddf function depends on.
        """
        res = super().deps(ddf)
        res.append(ddf.load())
        for anno in self.dep_annos():
            res.append(ddf.add_annotator(anno))
        return res

    def calc_ddf(self, ddf: DelayedDataFrame) -> DataFrame:
        """
        Calculates a dataframe with new columns to be added to the ddf.

        This overrides the method from the parent class and calls the
        compare function from the comparison method given.

        Parameters
        ----------
        ddf : DelayedDataFrame
            The ddf to be annotated.

        Returns
        -------
        DataFrame
            DataFrame with additional columns to be added to the ddf.df.
        """
        df = ddf.df
        columns_by_group = {}
        for group in self.groups:
            columns_by_group[group] = list(self.sample_columns(group))
        columns_other = []
        for g in self.other_groups_for_variance:
            columns_other.extend(self.sample_columns(g))
        res = self.comparison_strategy.compare(
            df,
            self.main_factor,
            self.factor_reference,
            columns_by_group,
            self.df_factors,
            self.interactions,
            self.test_difference,
            self.compare_non_reference,
            self.laplace_offset,
            self.prefixes,
        )
        rename = {}
        for col in res.columns:
            rename[col] = self.name_column(col)
        res = res.rename(columns=rename)
        res = res.set_index(df.index)
        return res

    def name_column(self, col: str) -> str:
        """
        Name mangler function that adds the annotator name to the new
        columns.

        Comparison name is added as a suffix.

        Parameters
        ----------
        col : [str]
            A column name to be changed.

        Returns
        -------
        [str]
            The new column name.
        """
        return f"{col} (Comp. {self.comparison_name})"


class ComparisonAnnotatorOld(ComparisonAnnotator):
    """
    I needed to adjust the calc fuction of ComparisonAnnotator to account for
    other_groups_fro_variance. This is the old function, I need it to generate the
    original results.
    """

    def calc(self, df):
        columns_a = list(self.sample_columns(self.comp[0]))
        columns_b = list(self.sample_columns(self.comp[1]))
        columns_other = []
        for g in self.other_groups_for_variance:
            columns_other.extend(self.sample_columns(g))
        comp = self.comparison_strategy.compare(
            df, columns_a, columns_b, columns_other, self.laplace_offset
        )
        res = {}
        for col in sorted(self.comparison_strategy.columns):
            res[self.name_column(col)] = comp[col]
        return pd.DataFrame(res)
