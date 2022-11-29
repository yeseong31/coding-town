from dotenv import load_dotenv

from config.default import *

load_dotenv(verbose=True)

SECRET_KEY = os.getenv('SECRET_KEY')
