# SETUP TO PYTHON LOGGING

import sys
import logging

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET
LEVEL_STREAM = logging.INFO
LEVEL_FILE = logging.DEBUG
LEVEL_LOGGER = logging.DEBUG

fmt = logging.Formatter('(%(asctime)s) %(levelname)s: %(message)s')

handler_stream = logging.StreamHandler(sys.stdout)
handler_stream.setLevel(LEVEL_STREAM)
handler_stream.setFormatter(fmt)

logger.setLevel(LEVEL_LOGGER)
logger.addHandler(handler_stream)
