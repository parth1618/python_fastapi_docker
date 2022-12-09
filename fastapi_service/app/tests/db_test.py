import databases
import sqlalchemy

metadata_test = sqlalchemy.MetaData()


def get_url_test():
    url = "sqlite:///./inMem_records_test.db"
    return url


engine_test = sqlalchemy.create_engine(
    get_url_test(), connect_args={"check_same_thread": False}
)


def get_db_test():
    database = databases.Database(get_url_test())
    return database


records_db = sqlalchemy.Table(
    "records_test",
    metadata_test,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("salary", sqlalchemy.String),
    sqlalchemy.Column("department", sqlalchemy.String),
    sqlalchemy.Column("sub_department", sqlalchemy.String),
    sqlalchemy.Column("currency", sqlalchemy.String, default="USD"),
    sqlalchemy.Column("on_contract", sqlalchemy.String, nullable=True),
)


def get_record_table_test():
    return records_db
