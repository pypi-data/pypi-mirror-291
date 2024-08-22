from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("./fxkk/*.pyx", annotate=True, build_dir="build"),
    options={"build_ext": {"build_lib": "./fxkk"}},
)
