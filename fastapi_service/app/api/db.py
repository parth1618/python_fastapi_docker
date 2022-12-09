import databases
import sqlalchemy


def get_url():
    url = "sqlite:///./inMem_records.db"
    return url


engine = sqlalchemy.create_engine(
    get_url(), connect_args={"check_same_thread": False}
)


def get_db():
    database = databases.Database(get_url())
    return database


metadata = sqlalchemy.MetaData()

records_db = sqlalchemy.Table(
    "records",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("salary", sqlalchemy.String),
    sqlalchemy.Column("department", sqlalchemy.String),
    sqlalchemy.Column("sub_department", sqlalchemy.String),
    sqlalchemy.Column("currency", sqlalchemy.String, default="USD"),
    sqlalchemy.Column("on_contract", sqlalchemy.String, nullable=True),
)


def get_record_table():
    return records_db


fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin",
    }
}

dummy_record_db = [
    {
        "name": "Abhishek",
        "salary": "145000",
        "currency": "USD",
        "department": "Engineering",
        "sub_department": "Platform"
    },
    {
        "name": "Anurag",
        "salary": "90000",
        "currency": "USD",
        "department": "Banking",
        "on_contract": "true",
        "sub_department": "Loan"
    },
    {
        "name": "Himani",
        "salary": "240000",
        "currency": "USD",
        "department": "Engineering",
        "sub_department": "Platform"
    },
    {
        "name": "Yatendra",
        "salary": "30",
        "currency": "USD",
        "department": "Operations",
        "sub_department": "CustomerOnboarding"
    },
    {
        "name": "Ragini",
        "salary": "30",
        "currency": "USD",
        "department": "Engineering",
        "sub_department": "Platform"
    },
    {
        "name": "Nikhil",
        "salary": "110000",
        "currency": "USD",
        "on_contract": "true",
        "department": "Engineering",
        "sub_department": "Platform"
    },
    {
        "name": "Guljit",
        "salary": "30",
        "currency": "USD",
        "department": "Administration",
        "sub_department": "Agriculture"
    },
    {
        "name": "Himanshu",
        "salary": "70000",
        "currency": "EUR",
        "department": "Operations",
        "sub_department": "CustomerOnboarding"
    },
    {
        "name": "Anupam",
        "salary": "200000000",
        "currency": "INR",
        "department": "Engineering",
        "sub_department": "Platform"
    }
]
