import os
import subprocess
from setuptools import Extension
from Cython.Build import cythonize

# Define extensions outside of the build function
extensions = [
    Extension(
        "thispkg.base.quipubase",
        ["thispkg/base/quipubase.pyx"],
        extra_compile_args=["-O3"]
    ),
    Extension(
        "thispkg.base64.fast_base64",
        ["thispkg/base64/fast_base64.c"],
        extra_compile_args=["-O3"]
    ),
    Extension(
        "thispkg.ouid.ouid",
        ["thispkg/ouid/ouid.c"],
        extra_compile_args=["-O3"]
    ),
    Extension(
        "thispkg.similarity_search.similarity_search",
        ["thispkg/similarity_search/similarity_search.c"],
        extra_compile_args=["-O3"]
    ),
]

def build(setup_kwargs):
    # Compile the extensions
    ext_modules = cythonize(extensions)

    # Update build parameters
    setup_kwargs.update({
        'ext_modules': ext_modules,
        'include_dirs': [],  # Add any necessary include directories
        'libraries': [],     # Add any necessary libraries
    })

# This part is for development purposes, not used by Poetry during build
if __name__ == "__main__":
    for ext in extensions:
        subprocess.run(["python", "setup.py", "build_ext", "--inplace"], cwd=os.path.dirname(ext.sources[0]))