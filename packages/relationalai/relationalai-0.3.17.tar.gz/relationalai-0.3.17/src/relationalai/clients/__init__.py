# note: user must do `import relationalai.clients.azure` to get `azure` submodule
from . import config, snowflake, test, client

__all__ = ['snowflake', 'test', 'config', 'client']
