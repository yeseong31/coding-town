from dotenv import load_dotenv

from config.default import *

load_dotenv(verbose=True)

SECRET_KEY = os.getenv('SECRET_KEY')

# https://docs.sqlalchemy.org/en/13/core/type_basics.html
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'app.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
