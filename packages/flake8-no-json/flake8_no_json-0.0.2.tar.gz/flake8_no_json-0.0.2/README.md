<!---
The MIT License (MIT)

Copyright (c) 2024 blablatdinov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
--->

# flake8-no-json

[![Build Status](https://github.com/blablatdinov/flake8-no-json/workflows/test/badge.svg?branch=master&event=push)](https://github.com/blablatdinov/flake8-no-json/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/blablatdinov/flake8-no-json/branch/master/graph/badge.svg)](https://codecov.io/gh/blablatdinov/flake8-no-json)
[![Python Version](https://img.shields.io/pypi/pyversions/flake8-no-json.svg)](https://pypi.org/project/flake8-no-json/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

## Background

This is a Flake8 plugin that prevents the use of the standard json package in Python code.
The intent is to enforce the use of an alternative JSON handling library, such as ujson,
orjson, or any other specified by your project guidelines.

## Installation

To install `flake8-no-json`, you can use `pip`:

```bash
pip install flake8-no-json
```

## Usage

Once installed, the plugin will automatically be used when running Flake8. There is no additional configuration required.

Run Flake8 as you normally would:

```bash
flake8 your_project/
```

The plugin will raise an error whenever it detects an import of the json package:

```python
import json  # FJ001: Usage of the 'json' package is not allowed.
```

## License

[MIT](https://github.com/blablatdinov/flake8-no-json/blob/master/LICENSE)


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [9899cb192f754a566da703614227e6d63227b933](https://github.com/wemake-services/wemake-python-package/tree/9899cb192f754a566da703614227e6d63227b933). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/9899cb192f754a566da703614227e6d63227b933...master) since then.
