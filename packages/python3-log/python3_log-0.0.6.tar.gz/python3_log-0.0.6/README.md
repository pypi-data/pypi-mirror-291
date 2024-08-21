# log


## useage
### use directly without any config

* install with pip
```bash
pip install python3-log
```
* useage directly

```python
from log import log

log.info("info log")
log.error("error log")
```
in this case, default console log level and file log level are info and
log path is current path when os is windows while /etc/log/log/ when os
is linux.

### config by yourself
* install with sh
```bash
bash install.sh
```

before use, you can edit config file /etc/log/config.ini in linux while
lib path in windows. Then use it as below:
```python
from log import log

log.info("info log")
log.error("error log")
```