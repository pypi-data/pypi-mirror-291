import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
# Suppress SQLAlchemy debug messages
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Set environment variables
os.environ['SQLALCHEMY_SILENCE_UBER_WARNING'] = '1'


def detail_error(e=None):
    print("\n\n\n####ERROR:\n\n\n", flush=True)
    print(str(e), flush=True)
    import os
    import sys

    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno, flush=True)
    print("\n\n\n####ERROR###########\n\n\n", flush=True)


