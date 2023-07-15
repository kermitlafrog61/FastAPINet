import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from decouple import config


DATABASE_URL = "postgresql://{user}:{password}@{host}:{port}/{db}".format(
    user=config("POSTGRES_USER"),
    password=config("POSTGRES_PASSWORD"),
    host='db',
    port=5432,
    db=config("POSTGRES_DB"),
)


engine = sqlalchemy.create_engine(DATABASE_URL)
metadata = sqlalchemy.MetaData(engine)
Base = declarative_base(bind=engine, metadata=metadata)
SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
