from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path=path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))