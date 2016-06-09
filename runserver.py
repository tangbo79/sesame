from server import app
from util.logger import logger
app.run(host='0.0.0.0', port=80, debug=True)
