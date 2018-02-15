SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="nulinspiratie",
    password="paperscraperpassword",
    hostname="paperscraperdb.cbyxywvwfrgo.us-east-2.rds.amazonaws.com",
    databasename="paperscraperdb",
)

SQLALCHEMY_POOL_RECYCLE = 299
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True