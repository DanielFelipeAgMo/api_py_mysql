from distutils.command.config import config
from distutils.debug import DEBUG


class DevelopmentConfig(): # creamos una clase para el desarrollo
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'tdea'
    MYSQL_PASSWORD = '1234'
    MYSQL_DB = 'api-flask'

# Cramos un diccionario para el renderizado del archivo 
config={
    'development': DevelopmentConfig
}