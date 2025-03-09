import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.config.config_loader import get_config


def create_db_session() -> sessionmaker:
    """Create and return a database session factory."""
    config = get_config()["db"]
    database_url = f"postgresql://{config['url']}:{config['port']}/{config['db_name']}"
    try:
        engine = create_engine(
            database_url,
            pool_pre_ping=True,  # This will test connections before using them
            pool_recycle=3600,   # Recycle connections after an hour
            pool_size=10,        # Adjust based on your needs
            max_overflow=20,      # Allow temporary additional connections
            connect_args={
                "connect_timeout": 5,
            },
        )
        print(f"Succesfully connected to: {database_url}")
        logging.info(f"Succesfully connected to: {database_url}")
        return sessionmaker(bind=engine)
    except Exception as e:
        logging.error(f"Failed to connect to database: {str(e)}")
        raise
