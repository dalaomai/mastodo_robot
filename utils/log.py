import logging
import logging.config

from settings.logger import LOGGING

logging.config.dictConfig(LOGGING)
