from distutils.core import setup

description = """
Python package to read and write NetworkX graphs as GDF (Graph Data Format).
"""

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open("__version__.py") as f:
    version = f.read().strip().split()[-1].strip("\"")

setup(
    name="networkx-gdf",
    version=version,
    description=description.strip(),
    long_description=long_description,
    install_requires=install_requires,
    url="https://pypi.org/project/networkx-gdf/",
    author="Nelson Aloysio Reis de Almeida Passos",
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=["Network", "Graph", "GDF"],
    python_requires=">=3.7",
    py_modules=["networkx_gdf"],
    project_urls={
        "Source": "https://github.com/nelsonaloysio/networkx-gdf",
        "Tracker": "https://github.com/nelsonaloysio/networkx-gdf/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
