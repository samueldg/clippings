# Clippings

Python module to manipulate Amazon Kindle clippings files.

It allows you to:

- Parse your existing clippings file into a strctured representation;
- Generate clippings file programmatically.

## Installation

```bash
python setup.py install
```

## Usage

```bash
# Parse a clippings file
python -m clippings.parser -o dict ./clippings.txt 

# or from stdin:
cat clippings.txt | python -m clippings.parser -
```
