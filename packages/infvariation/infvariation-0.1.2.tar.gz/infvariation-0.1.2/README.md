# infvariation
The library is easy to use and can be integrated into larger projects or used as a standalone tool for data variation tasks.

# infVariation currently provides three main functions:

    ** typosquatting: **  This function generates variations of URLs to simulate common typing errors, helping to identify potential vulnerabilities. The input is a URL, and the output is alternative versions of that URL.

    ** leet: ** This function converts text into a modified form by replacing letters with numbers and other symbols, creating a "leet" (1337) version of the original text.

    ** generate_variations: ** This function generates various text variations by applying different modification patterns.

# Installation

## pip installation

```bash
$ pip install infvariation==0.1.2
```
```bash
$ uv pip install infvariation==0.1.2
```

# Example usage as a library:

from infvariation import Variation
 
genvar = Variation()

print("-----------")

print(genvar.typosquatting('mydomain.com'))

print("-----------")

print(genvar.generate_leet('mydomain'))

print("-----------")

print(genvar.generate_variations('mydomain'))


