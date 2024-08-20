from setuptools import Extension, setup

ouid_module = Extension(
    "ouid", sources=["ouid.c"], extra_compile_args=["-O3"]
)  # Enable high optimization

setup(
    name="ouid",
    version="1.0",
    description="Unique ID generation for classes with UUID-like format",
    ext_modules=[ouid_module],
)
