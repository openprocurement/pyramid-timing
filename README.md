[![Build Status](https://travis-ci.org/openprocurement/pyramid-timing.svg?branch=master)](https://travis-ci.org/openprocurement/pyramid-timing)
[![Coverage Status](https://coveralls.io/repos/github/openprocurement/pyramid-timing/badge.svg)](https://coveralls.io/github/openprocurement/pyramid-timing)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# pyramid-timing

Timing tween for measure request process time as pyramid plugin.
Write to log `request processing time`, `request method` and `response status code` on `DEBUG` level.

### Installation

```shell
pip install pyramidtiming
```

or

```shell
git clone https://github.com/openprocurement/pyramid-timing.git
cd pyramid-timing
pip install .
```

### How to use

In application settings add options `do_timing = true`

```python
from pyramid.config import Configurator
from pyramidtiming.tween import includeme as include_tween
config = Configurator()
config.settings.do_timing = True
include_tween(config)
```
