from setuptools import setup

name = "types-flake8-bugbear"
description = "Typing stubs for flake8-bugbear"
long_description = '''
## Typing stubs for flake8-bugbear

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`flake8-bugbear`](https://github.com/PyCQA/flake8-bugbear) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`flake8-bugbear`.

This version of `types-flake8-bugbear` aims to provide accurate annotations
for `flake8-bugbear==24.8.19`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/flake8-bugbear. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`7865a78de1929ee54797baca0fe07ac33567739f`](https://github.com/python/typeshed/commit/7865a78de1929ee54797baca0fe07ac33567739f) and was tested
with mypy 1.11.1, pyright 1.1.377, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="24.8.19.20240822",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/flake8-bugbear.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['bugbear-stubs'],
      package_data={'bugbear-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
