from setuptools import Extension, setup

fast_base64_module = Extension(
    "fast_base64", sources=["fast_base64.c"], extra_compile_args=["-O3"]
)  # Enable high optimization

setup(
    name="fast_base64",
    version="1.0",
    description="Fast Base64 encoding and decoding",
    ext_modules=[fast_base64_module],
)
