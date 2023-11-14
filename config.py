class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://osama:123456@127.0.0.1:3306/recipemanagement'
    SQLALCHEMY_TRACK_MODIFICATIONS = False