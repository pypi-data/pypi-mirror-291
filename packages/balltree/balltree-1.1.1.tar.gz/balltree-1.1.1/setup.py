import platform
import numpy as np
from setuptools import Extension, setup

if platform.system() == "Windows":
    platform_flags = ["/Ox", "/fp:fast"]
else:
    platform_flags = ["-O3", "-ffast-math"]

balltree = Extension(
    name="balltree.balltree",
    sources=[
        "balltree/balltree.c",
        "src/pointbuffers.c",
        "src/histogram.c",
        "src/queue.c",
        "src/ballnode.c",
        "src/ballnode_stats.c",
        "src/ballnode_query.c",
        "src/balltree.c",
        "src/balltree_serialize.c",
    ],
    include_dirs=["include", np.get_include()],
    extra_compile_args=[
        "-Wall",
        *platform_flags,
        "-DSET_PYERR_STRING",  # required to propagate C errors to python
    ],
)

if __name__ == "__main__":
    setup(
        ext_modules=[balltree],
    )
