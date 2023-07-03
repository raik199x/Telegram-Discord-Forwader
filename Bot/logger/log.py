import logging
import colorlog
import urllib3


# Create a color formatter
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime).19s [%(levelname)s] %(message)s',
    log_colors={
        'DEBUG': 'reset',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    },
    secondary_log_colors={
        'message': {
            'DEBUG': 'blue',
            'INFO': 'reset',
            'WARNING': 'reset',
            'ERROR': 'reset',
            'CRITICAL': 'reset',
        }
    }
)

# Create a color log handler
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Configure the logger
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Disable debug messages from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger().setLevel(logging.INFO)
