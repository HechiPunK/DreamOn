class Config:
    SECRET_KEY = 'f1d04db22f0472ddacead9a62b48e71c'

class DevelopmentConfig(Config):  
    DEBUG = True
    MYSQL_HOST ='localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD =''
    MYSQL_DB ='sueños'

config = {
    'development': DevelopmentConfig
}