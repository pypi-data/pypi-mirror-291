from setuptools import setup

name = "types-flake8-2020"
description = "Typing stubs for flake8-2020"
long_description = '''
## Typing stubs for flake8-2020

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`flake8-2020`](https://github.com/asottile/flake8-2020) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`flake8-2020`.

This version of `types-flake8-2020` aims to provide accurate annotations
for `flake8-2020==1.8.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/flake8-2020. All fixes for
types and metadata should be contributed there.

*Note:* `types-flake8-2020` is unmaintained and won't be updated.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`eb8e9ddd912a1ffa36f56b2ac150a5ce757f6347`](https://github.com/python/typeshed/commit/eb8e9ddd912a1ffa36f56b2ac150a5ce757f6347) and was tested
with mypy 1.11.1, pyright 1.1.376, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="1.8.0.20240818",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/flake8-2020.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['flake8_2020-stubs'],
      package_data={'flake8_2020-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
