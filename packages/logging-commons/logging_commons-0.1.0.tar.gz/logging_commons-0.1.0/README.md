# Python Logging Tools

## Usage

### Logging Config

```python
config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "system.logging_helper.JsonFormatter",
            "format_dict": {
                "level": "levelname",
                "timestamp": "asctime",
                "logger_name": "name",
                "module": "module",
                "line": "lineno",
                "message": "message",
                "context": "mdc",
            },
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}
```

Example Output

```json

```

### MDC Usage

## Special Thanks:

- [Bogdan Mircea](https://stackoverflow.com/users/11971654/bogdan-mircea) for the `JsonFormatter` code given in [Stackoverflow](https://stackoverflow.com/a/70223539)