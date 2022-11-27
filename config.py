import os.path
import sys

import mariadb
from dotenv import load_dotenv

# https://velog.io/@yvvyoon/python-env-dotenv
load_dotenv(verbose=True)

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = os.getenv('SECRET_KEY')


def conn_mariadb():
    """Connecting to MariaDB Server"""
    try:
        conn = mariadb.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            database=os.getenv('DB_NAME')
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
