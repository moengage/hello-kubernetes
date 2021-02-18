import logging


class Log(object):
    logger = None

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    CRITICAL = logging.CRITICAL

    class _sanitize(object):
        def __init__(self, function):
            self._function = function

        def __call__(self, klass, *args):
            content = ''
            for arg in args:
                content = ' '.join([content, str(arg)])
            self._function(klass, content)

    @classmethod
    def _initilize_logger(cls, level):
        stdout_handler = logging.StreamHandler(sys.stdout)
        handlers = [stdout_handler]
        logging.basicConfig(
            level=level,
            format='%(levelname)s - %(message)s',
            handlers=handlers
        )

    @classmethod
    def get_logger(cls, level=logging.ERROR):
        if not cls.logger:
            cls._initilize_logger(level)
            cls.logger = logging.getLogger(__name__)
        return cls.logger

    @classmethod
    @_sanitize
    def debug(cls, *args):
        cls.logger.debug(*args)

    @classmethod
    @_sanitize
    def info(cls, *args):
        cls.logger.info(*args)

    @classmethod
    @_sanitize
    def warning(cls, *args):
        cls.logger.warning(*args)

    @classmethod
    @_sanitize
    def error(cls, *args):
        cls.logger.error(*args)

    @classmethod
    @_sanitize
    def critical(cls, *args):
        cls.logger.critical(*args)


