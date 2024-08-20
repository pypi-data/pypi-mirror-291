from . import fastq2, post_process
from .lanes import Sample, AlignedSample, sanity_check
from .exceptions import PairingError
from . import strategies
from .strategies import *  # noqa:F403,F401

try:
    from . import tenx
except ImportError as e:
    if "scanpy" in str(e):
        tenx = False
    else:
        raise


__all__ = [
    "Sample",
    "fastq2",
    "PairingError",
    "AlignedSample",
    "post_process",
    "tenx",
    "sanity_check",
]
__all__.extend([x for x in dir(strategies) if x.startswith("FASTQs")])

__version__ = "0.5"
