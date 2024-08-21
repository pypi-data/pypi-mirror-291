from setuptools import setup, Extension
from Cython.Build import cythonize

# Define the Cython extension
extensions = [
    Extension("basicindex.basic_index", ["basicindex/basic_index.pyx"])
]

# Setup script
setup(
    name="basicindex",
    version="1.1.3",
    description="A Python package for handling basic indexing operations.",
    packages=["basicindex"],
    ext_modules=cythonize(extensions),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
