import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__) + '/..')
engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'), convert_unicode=True, echo=False)

Base = declarative_base()
Base.metadata.reflect(engine)

Session = sessionmaker(bind=engine)
session = Session()