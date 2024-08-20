from typing import List, Dict, Any, Tuple
from mbf.qualitycontrol import register_qc, qc_disabled
from dppd import dppd
from mbf.genomics.util import parse_a_or_c, freeze
from mbf.genomics import DelayedDataFrame
from pandas import DataFrame
from .annotator import (
    ComparisonAnnotator,
    ComparisonAnnotatorOld,
    ComparisonAnnotatorMulti,
)
import functools
import pandas as pd
import pypipegraph as ppg
import dppd_plotnine  # noqa: F401
import itertools

dp, X = dppd()


class Comparisons:
    """A ddf + comparison groups,
    ready for actually doing comparisons

    Paramaters:

        groups_to_samples: { keyX: [columnA, annoB, (annoC, column_name), (annoC, 2),
                                keyY: ..., ...}
            keyX: one of the keys of groups_to_samples
            keyY: one of the keys of groups_to_samples
    """

    def __init__(self, ddf, groups_to_samples, name=None):
        if not isinstance(ddf, DelayedDataFrame):
            raise ValueError("Ddf must be a DelayedDataFrame")
        self.ddf = ddf
        self.groups_to_samples = self._check_input_dict(groups_to_samples)
        self.sample_column_to_group = self._sample_columns_to_group()
        self.samples = functools.reduce(
            list.__add__, [x[1] for x in sorted(self.groups_to_samples.items())]
        )
        if name is None:
            self.name = "comparison__" + "_".join(sorted(self.groups_to_samples.keys()))
        else:
            self.name = "comparison__" + name
        self.result_dir = self.ddf.result_dir / self.name
        self.result_dir.mkdir(exist_ok=True, parents=True)
        if ppg.inside_ppg():
            ppg.assert_uniqueness_of_object(self)
            if not hasattr(ppg.util.global_pipegraph, "_mbf_comparisons_name_dedup"):
                ppg.util.global_pipegraph._mbf_comparisons_name_dedup = set()
            for name in self.groups_to_samples:
                if name in ppg.util.global_pipegraph._mbf_comparisons_name_dedup:
                    raise ValueError(
                        f"Comparisons group {name} defined in multiple Comparisons - not supported"
                    )
        self.register_qc()

    def a_vs_b_old(
        self,
        a,
        b,
        method,
        laplace_offset=1 / 1e6,
        include_other_samples_for_variance=True,
    ):
        if a not in self.groups_to_samples:
            raise KeyError(a)
        if b not in self.groups_to_samples:
            raise KeyError(b)
        if not hasattr(method, "compare"):
            raise TypeError(f"{method} had no method compare")
        if include_other_samples_for_variance:
            other_groups = []
            for group_name in self.groups_to_samples:
                if group_name != a and group_name != b:
                    other_groups.append(group_name)
        else:
            other_groups = []
        res = ComparisonAnnotatorOld(self, a, b, method, laplace_offset, other_groups)
        self.ddf += res
        return res

    def a_vs_b(
        self,
        a,
        b,
        method,
        laplace_offset=1 / 1e6,
        include_other_samples_for_variance=True,
    ):
        # this is the right way to do it
        if a not in self.groups_to_samples:
            raise KeyError(a)
        if b not in self.groups_to_samples:
            raise KeyError(b)
        if not hasattr(method, "compare"):
            raise TypeError(f"{method} had no method compare")
        if include_other_samples_for_variance:
            other_groups = []
            for group_name in self.groups_to_samples:
                if group_name != a and group_name != b:
                    other_groups.append(group_name)
        else:
            other_groups = []

        res = ComparisonAnnotator(self, a, b, method, laplace_offset, other_groups)
        self.ddf += res
        return res

    def multi(
        self,
        name: str,
        main_factor: str,
        factor_reference: Dict[str, str],
        df_factors: DataFrame,
        interactions: List[Tuple[str, str]],
        method: Any,
        test_difference: bool = True,
        compare_non_reference: bool = False,
        laplace_offset: float = 1 / 1e6,
    ) -> ComparisonAnnotatorMulti:
        """
        Initializes and returns an annotator for multi-factor analysis.

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
        main_factor : str
            The main factor, usually condition or treatment.
        factor_reference : Dict[str, str]
            Dictionary of factor names (key) to base level (value), e.g.
            {"treatment": "DMSO"}.
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

        Returns
        -------
        ComparisonAnnotatorMulti
            Multi-factor comparison annotator.

        Raises
        ------
        ValueError
            If the df_factors does not contain a group column.
        ValueError
            If a factor is not found in df_factors.
        ValueError
            If a level is specified in the dictionaryx that is not present in df_factors.
        ValueError
            If less than 2 factors are given.
        KeyError
            If a specified group in not in the comparisons.
        TypeError
            if the given compare method does not have a compare function.
        """
        if "group" not in df_factors.columns:
            raise ValueError(
                "Column 'group' not in df_factors, please provide a group column containing all groups affecting the counts."
            )
        for factor in factor_reference:
            if factor not in df_factors.columns:
                raise ValueError(f"Factor {factor} not in df_factors.")
            # for level in factor_levels_ordered[factor]:
            #     if level not in df_factors.values:
            #         raise ValueError(f"Unknown factor level {level} for factor {factor}.")
        if len(factor_reference) < 2:
            raise ValueError(
                f"You need at least 2 factors for a multi-factor design', factors given were {list(factor_reference.keys())}."
            )
        groups = list(df_factors["group"].values)
        for group in groups:
            if group not in self.groups_to_samples:
                raise KeyError(group)
        if not hasattr(method, "compare"):
            raise TypeError(f"{method} had no method compare")
        res = ComparisonAnnotatorMulti(
            name,
            self,
            main_factor,
            factor_reference,
            groups,
            df_factors,
            interactions,
            method,
            test_difference,
            compare_non_reference,
            laplace_offset,
        )
        return res

    def all_vs_b(self, b, method, laplace_offset=1 / 1e6):
        res = {}
        for a in self.groups_to_samples:
            if a != b:
                res[a] = self.a_vs_b(a, b, method, laplace_offset)
        return res

    def all_vs_all(self, method, laplace_offset=1 / 1e6):
        res = {}
        for a, b in itertools.combinations(self.groups_to_samples, 2):
            res[a, b] = self.a_vs_b(a, b, method, laplace_offset)
        return res

    def _check_input_dict(self, groups_to_samples):
        if not isinstance(groups_to_samples, dict):
            raise ValueError("groups_to_samples must be a dict")
        for k, v in groups_to_samples.items():
            if not isinstance(k, str):
                raise ValueError("keys must be str, was %s %s" % (k, type(k)))
            v = [parse_a_or_c(x) for x in v]
            groups_to_samples[k] = v

        return groups_to_samples

    def _sample_columns_to_group(self):
        result = {}
        for group, samples in self.groups_to_samples.items():
            for ac in samples:
                c = ac[1]
                if c in result:
                    raise ValueError(
                        f"Sample in multiple groups - not supported {ac}, {group}, {result[c]}"
                    )
                result[c] = group
        return result

    def register_qc(self):
        if not qc_disabled():
            self.register_qc_distribution()
            self.register_qc_pca()
            self.register_qc_correlation()

    def find_variable_name(self):
        for anno, column in self.samples:
            if anno is not None and hasattr(anno, "unit"):
                return anno.unit
        return "value"

    def get_plot_name(self, column):
        for ac in self.samples:
            if ac[1] == column:
                if ac[0] is not None:
                    return getattr(ac[0], "plot_name", column)
                else:
                    return column
        raise KeyError(column)

    def get_df(self):
        return self.ddf.df[[column for anno, column in self.samples]]

    def register_qc_distribution(self):
        output_filename = self.result_dir / "distribution.png"

        def plot(output_filename):
            df = self.get_df()
            sample_count = df.shape[1]
            sample_names = [self.get_plot_name(x) for x in df.columns]
            sample_groups = [self.sample_column_to_group[x] for x in df.columns]
            df.columns = pd.MultiIndex.from_tuples(
                zip(sample_names, sample_groups), names=("sample", "group")
            )
            order = [
                x[0]
                for x in sorted(zip(sample_names, sample_groups), key=lambda v: v[1])
            ]
            return (
                dp(df)
                .melt(value_name="y")
                .categorize("sample", order)
                .p9()
                .theme_bw()
                .annotation_stripes()
                # .geom_violin(dp.aes("sample", "y"), width=0.5)
                .add_boxplot(x="sample", y="y", _width=0.1, _fill=None, color="group")
                .scale_color_many_categories()
                .scale_y_continuous(trans="log10", name=self.find_variable_name())
                .turn_x_axis_labels()
                .hide_x_axis_title()
                .render(
                    output_filename,
                    height=5,
                    width=1 + 0.25 * sample_count,
                    limitsize=False,
                )
            )

        return register_qc(
            ppg.FileGeneratingJob(output_filename, plot).depends_on(self.deps())
        )

    def deps(self):
        input_columns = []
        for k in sorted(self.groups_to_samples):
            for ac in self.groups_to_samples[k]:
                input_columns.append(ac[1])

        return [
            self.ddf.add_annotator(ac[0]) for ac in self.samples if ac[0] is not None
        ] + [
            self.ddf.load(),
            ppg.ParameterInvariant(self.name, freeze(input_columns)),
        ]  # you might be working with an anno less ddf afterall

    def register_qc_pca(self):
        output_filename = self.result_dir / "pca.png"

        def plot():
            import sklearn.decomposition as decom

            pca = decom.PCA(n_components=2, whiten=False)
            data = self.get_df()
            # min max scaling 0..1 per gene
            data = data.sub(data.min(axis=1), axis=0)
            data = data.div(data.max(axis=1), axis=0)

            data = data[~pd.isnull(data).any(axis=1)]  # can' do pca on NAN values
            pca.fit(data.T)
            xy = pca.transform(data.T)
            title = "PCA %s (%s)\nExplained variance: x %.2f%%, y %.2f%%" % (
                self.ddf.name,
                self.find_variable_name(),
                pca.explained_variance_ratio_[0] * 100,
                pca.explained_variance_ratio_[1] * 100,
            )
            plot_df = pd.DataFrame(
                {
                    "x": xy[:, 0],
                    "y": xy[:, 1],
                    "label": [self.get_plot_name(c) for (a, c) in self.samples],
                    "group": [
                        self.sample_column_to_group[c] for (a, c) in self.samples
                    ],
                }
            )
            p = dp(plot_df).p9().theme_bw().add_scatter("x", "y", color="group")
            if data.shape[1] < 15:
                p = p.add_text(
                    "x",
                    "y",
                    "label",
                    _alpha=0.5,
                    # _adjust_text={
                    # "expand_points": (2, 2),
                    # "arrowprops": {"arrowstyle": "->", "color": "darkgrey"},
                    # },
                )
            p = (
                p.scale_color_many_categories()
                .title(title)
                .render(output_filename, width=8, height=6, dpi=72)
            )
            plot_df.to_csv(output_filename.with_suffix(".tsv"), sep="\t")

        return register_qc(
            ppg.MultiFileGeneratingJob(
                [output_filename, output_filename.with_suffix(".tsv")], plot
            )
            .depends_on(self.deps())
            .depends_on(
                ppg.ParameterInvariant(
                    str(output_filename) + "_plot_params",
                    {
                        "label": sorted(
                            [self.get_plot_name(c) for (a, c) in self.samples]
                        ),
                        "group": sorted(
                            [self.sample_column_to_group[c] for (a, c) in self.samples]
                        ),
                    },
                )
            )
        )

    def register_qc_correlation(self):
        output_filename = self.result_dir / "pearson_correlation.png"

        def plot(output_filename):
            data = self.get_df()
            data = data.sub(data.min(axis=1), axis=0)
            data = data.div(data.max(axis=1), axis=0)
            # data -= data.min()  # min max scaling 0..1 per gene
            # data /= data.max()
            data = data[
                ~pd.isnull(data).any(axis=1)
            ]  # can' do correlation on NAN values
            sample_names = [self.get_plot_name(x) for x in data.columns]
            sample_groups = [self.sample_column_to_group[x] for x in data.columns]
            data.columns = sample_names

            order_pdf = pd.DataFrame(
                {"sample": sample_names, "group": sample_groups}
            ).sort_values(["group", "sample"])
            ordered_names = ["group"] + list(order_pdf["sample"])
            sample_count = data.shape[1]
            pdf = (
                data.corr().transpose().assign(group=0).transpose()
            )  # value doesn't matter, this just reserves space on the plot
            pdf = pd.melt(pdf.reset_index(), "index")
            (
                dp(pdf)
                .categorize("index", ordered_names)
                .categorize("variable", ordered_names)
                .p9()
                .add_tile("index", "variable", fill="value")
                .scale_fill_gradient2(
                    "blue", "white", "red", limits=[-1, 1], midpoint=0
                )
                .add_scatter(
                    _x=1, y="sample", color="group", _shape="s", data=order_pdf, _size=3
                )
                .scale_color_many_categories()
                .hide_x_axis_title()
                .hide_y_axis_title()
                .turn_x_axis_labels()
                .render(
                    output_filename,
                    width=(1 + 0.15 * sample_count) * 2,
                    height=0.15 * sample_count * 3.2,
                )
            )

        return register_qc(
            ppg.FileGeneratingJob(output_filename, plot).depends_on(self.deps())
        )
