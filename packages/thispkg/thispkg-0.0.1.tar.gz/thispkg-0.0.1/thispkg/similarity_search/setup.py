from setuptools import setup, Extension  # type: ignore
import numpy as np

similarity_module = Extension(
    "similarity_search",
    sources=["similarity_search.c"],
    include_dirs=[np.get_include()],
    extra_compile_args=["-O3"],
)

setup(
    name="similarity_search",
    version="1.0",
    description="Similarity search module",
    ext_modules=[similarity_module],
    install_requires=["numpy>=2.0"],
)
