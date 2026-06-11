from sqlalchemy import create_engine
from config.config import *


def get_engine():
    connection_string = (
        f"mysql+pymysql://"
        f"{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(
        connection_string,
        pool_pre_ping=True
    )

    return engine