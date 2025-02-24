from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://neondb_owner:npg_tWemv6bUJI0l@ep-polished-sun-a9ovl1x6-pooler.gwc.azure.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URLModel(Base):
    __tablename__ = "urls"

    short_code = Column(String(6), primary_key=True)
    original_url = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)