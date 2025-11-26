from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "busqueda",
        ["busqueda.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++"
    )
]

setup(
    name="busqueda",
    ext_modules=ext_modules
)