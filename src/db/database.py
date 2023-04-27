'''
Database Manager
'''
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generator
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from src.schemas import settings


#instantiated base class for declarative models
Base = declarative_base()


class SingletonDBManager(type):
    '''
    Singleton database manager mixin
    '''
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DataBaseErrorHandling(Exception):
    '''
    Database Error handling for custom raise
    '''
    pass


@dataclass
class DataBaseManager(metaclass=SingletonDBManager):
    '''
    Manages database operations
    '''
    _engine = None

    def __enter__(self):
        """opening contextmanager by enter magic method

        Returns:
            self._session(): while open instantiated class with context manager
            session is open to use
        """
        self._session = self.session()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """closing contextmanager by exit magic method

        Returns:
            self._session.close: while close instantiated class with context manager
            session will close
        """
        self._session.close()

    def engine(self):
        """
        SQLAlchemy engine instance.

        Returns:
            sqlalchemy.engine.Engine: A SQLAlchemy engine instance.

        Raises:
            DataBaseErrorHandling: throw error while creating engine.

        """
        try:
            if self._engine is None:
                self._engine = create_engine(settings.DATABASE_URL,echo=settings.DATABASE_ECHO)
            return self._engine
        except Exception as e:
            raise DataBaseErrorHandling(f"Error creating sync engine: {e}") from e

    def session(self):
        """
        Returns a sessionmaker instance with specified options.

        Returns:
            sqlalchemy.orm.session.sessionmaker: A sessionmaker instance.

        """
        return sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=self.engine())()


db_manager = DataBaseManager()


@contextmanager
def get_session():
    '''
    Async Context manager to get async session
    '''
    db = db_manager.session()
    try:
        yield db
    finally:
        db.close()


def get_db() -> Generator:
    '''
    generator to get session
    '''
    with get_session() as db:
        yield db


def init_db():
    '''
    Initializes the database with Base.metadata
    '''
    engine = db_manager.engine()
    if settings.DROP_TABLE == True:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
