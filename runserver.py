from server.weixin import main
from util.logger import logger

import logging
_logger = logging.getLogger(__name__)

while True:
    try:
        main()
    except Exception as e:
        _logger.exception(e)
