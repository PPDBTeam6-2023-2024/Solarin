# Config

## Overview
How we will be doing configuration in our backend

## Technologies used
- [confz](https://github.com/Zuehlke/ConfZ)
- [pydantic](https://docs.pydantic.dev/latest/)

## Description
Our configuration is done using the python library confz. This is an easy to use library. You can define a configuration using pydantic types. And the input configuration will be validated. 

```python
from confz import BaseConfig, FileSource
from pydantic import SecretStr, AnyUrl

class DBConfig(BaseConfig):
    user: str
    password: SecretStr

class APIConfig(BaseConfig):
    host: AnyUrl
    port: int
    db: DBConfig
```

You can load a config from many different source types:
- FileSource (jaml, json, toml)
- EnvSource (env variables and .env files)
- CLArgSource (command line arguments)
- DataSource (constant config data)

## Issues

## Additional Information
