import pytest
from pathlib import Path


def _mock_get_page(url):
    import hashlib
    import mbf.externals

    p = (
        Path("/tmp")
        / ".testing_download_cache"
        / hashlib.md5(url.encode("utf-8")).hexdigest()
    )
    p.parent.mkdir(exist_ok=True)
    if not p.exists():
        p.write_text(mbf.externals.util.get_page(url))
    return p.read_text()


def _mock_download_file_and_gunzip(url, filename):
    import shutil
    import hashlib
    import mbf.externals

    p = (
        Path("/tmp")
        / ".testing_download_cache"
        / hashlib.md5(url.encode("utf-8")).hexdigest()
    )
    p.parent.mkdir(exist_ok=True)
    if not p.exists():
        mbf.externals.util.download_file_and_gunzip(url, p)
    return shutil.copyfile(p, filename)


@pytest.fixture
def mock_download():
    import mbf.genomes

    org_get_page = mbf.genomes.ensembl.get_page
    org_download_file_and_gunzip = mbf.genomes.base.download_file_and_gunzip
    mbf.genomes.ensembl.get_page = _mock_get_page
    mbf.genomes.base.download_file_and_gunzip = _mock_download_file_and_gunzip
    yield
    mbf.genomes.ensembl.get_page = org_get_page
    mbf.genomes.base.download_file_and_gunzip = org_download_file_and_gunzip


first_shared_prebuild = True


@pytest.fixture()
def shared_prebuild():
    global first_shared_prebuild
    p = Path("/tmp/prebuild")
    if first_shared_prebuild:
        if p.exists():
            import shutil

            shutil.rmtree(p)
        p.mkdir()
        first_shared_prebuild = False
    from mbf.externals import PrebuildManager

    return PrebuildManager(p)


all = [shared_prebuild, mock_download]
