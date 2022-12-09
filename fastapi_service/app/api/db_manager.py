from databases import Database
from sqlalchemy import Table

from app.api.models import RecordIn


async def add_record(database: Database, table: Table, payload: RecordIn):
    """Add record to the table"""
    record = payload.dict()
    query = table.insert().values(**record)
    record_id = await database.execute(query=query)
    return record_id


async def get_all_records(database: Database, table: Table):
    """Return all records from the table"""
    query = table.select()
    return await database.fetch_all(query=query)


async def get_record(database: Database, table: Table, id: int):
    """Get record by id form the table"""
    query = table.select(table.c.id == id)
    return await database.fetch_one(query=query)


async def delete_record(database: Database, table: Table, id: int):
    """Delete record by id from the table"""
    query = table.delete().where(table.c.id == id)
    return await database.execute(query=query)
