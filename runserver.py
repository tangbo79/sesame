from server import app
from util.logger import logger

import logging
_logger = logging.getLogger(__name__)

while True:
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    except Exception as e:
        _logger.exception(e)
