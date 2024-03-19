# Logging

## Overview
How logging will be done inside our backend.

## Technologies used
- [loguru](https://github.com/Delgan/loguru)

## Description
Logging will be done with loguru. This is an extension library of the standard python `logging` module. 

The configuration for logging is done using confz. In this configuration you can specify following parameters:

```python
class LoggingConfig(BaseConfig):
    path: DirectoryPath
    filename: str
    level: LogLevel
    rotation: str
    retention: str
    format: str
```

Like you see, all the logs will be saved into a file.

To log something simply do this:
```python
from loguru import logger

logger.debug("That's it, beautiful and simple logging!")

```

## Issues
Make sure the path parameter pointing to the directoy in which the logs need to persist exist!

## Additional Information

