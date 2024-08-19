from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy
import os


ext_modules = [
    Extension(
            name="fast_gae.fast_gae",
            sources=["fast_gae/fast_gae.pyx"],
            define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
            include_dirs=[numpy.get_include()],
        )
]

debug = os.getenv('DEBUG', '0') == '1'
annotate = os.getenv('ANNOTATE', '0') == '1'
build_dir = 'build'
if debug:
    build_dir = 'build_debug'

os.makedirs(build_dir, exist_ok=True)

setup(
    name='fast_gae',
    packages=find_packages(),
    ext_modules=cythonize(
        ext_modules,
        build_dir=build_dir,
        compiler_directives={
            "profile": True,
            "language_level": "3",
            "embedsignature": debug,
            "annotation_typing": debug,
            "cdivision": debug,
            "boundscheck": debug,
            "wraparound": debug,
            "initializedcheck": debug,
            "nonecheck": debug,
            "overflowcheck": debug,
            "overflowcheck.fold": debug,
            "linetrace": debug,
            "c_string_encoding": "utf-8",
            "c_string_type": "str",

        },
        annotate=debug or annotate,
    ),
    description='',
    url='https://github.com/Metta-AI/fast_gae',
    install_requires=[
        'numpy',
        'cython==3.0.11',
    ],
)
