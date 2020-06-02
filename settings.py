#! python
#
# Settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '{module} ({levelname}) {asctime}: {message}',
            'style': '{',
        },
        'simple': {
            'datefmt': '%H:%M:%S',
            'format': '{module} | {levelname} {asctime}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'loudark': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'loudark.proxy': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}
