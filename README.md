# pyramid-timing

Timing tween for measure request process time as pyramid plugin.
Write to log `request processing time`, `request method` and `response status code` on `DEBUG` level.

### Installation

```shell
pip install pyramidtiming
```

or

```shell
git clone https://VDigitall@gitlab.quintagroup.com/VDigitall/pyramid-timing-tween.git
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
