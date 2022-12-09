from databases import Database
from sqlalchemy import Table
from fastapi import Depends, HTTPException, APIRouter
from typing import List

from starlette import status

from app.api import db_manager
from app.api.auth_manager import get_current_user
from app.api.db import get_db, get_record_table
from app.api.models import Record, RecordIn, Summary, DepartmentSummary, SubDepartmentSummary, \
    DepartmentSummaryNested

record_routes = APIRouter(dependencies=[Depends(get_current_user)])


@record_routes.get('/', response_model=List[Record])
async def get_records(database: Database = Depends(get_db), table: Table = Depends(get_record_table)):
    return await db_manager.get_all_records(database, table)


@record_routes.post('/add', status_code=201)
async def add_record(payload: RecordIn, database: Database = Depends(get_db), table: Table = Depends(get_record_table)):
    record_id = await db_manager.add_record(database, table, payload)
    response = {
        'id': record_id,
        **payload.dict()
    }
    return response


@record_routes.delete('/remove/{id}', response_model=None)
async def delete_record(id: str, database: Database = Depends(get_db), table: Table = Depends(get_record_table)):
    record = await db_manager.get_record(database, table, int(id))
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    await db_manager.delete_record(database, table, int(id))
    response = {
        'id': id
    }
    return response


@record_routes.get('/summary', response_model=Summary)
async def get_summary(database: Database = Depends(get_db), table: Table = Depends(get_record_table)):
    records = await db_manager.get_all_records(database, table)
    salary_list = list(map(lambda d: int(d['salary']), records))
    return Summary.parse_obj(dict(mean=str(round(sum(salary_list) / len(salary_list), 2) if salary_list else 0),
                                  min=str(min(salary_list) if salary_list else 0),
                                  max=str(max(salary_list) if salary_list else 0)))


@record_routes.get('/on_contract/summary', response_model=Summary)
async def get_on_contract_summary(database: Database = Depends(get_db), table: Table = Depends(get_record_table)):
    records = await db_manager.get_all_records(database, table)
    salary_list = list(map(lambda d: int(d['salary']),
                           list(filter(lambda e: str(e.on_contract).lower() == 'true', records))))
    return Summary.parse_obj(dict(mean=str(round(sum(salary_list) / len(salary_list), 2) if salary_list else 0),
                                  min=str(min(salary_list) if salary_list else 0),
                                  max=str(max(salary_list) if salary_list else 0)))


@record_routes.get('/department/summary', response_model=List[DepartmentSummary])
async def get_department_summary(database: Database = Depends(get_db), table: Table = Depends(get_record_table)):
    records = await db_manager.get_all_records(database, table)

    departments = list(set([rec['department'] for rec in records]))
    response = []

    for dept in departments:
        salary_list = list(map(lambda d: int(d['salary']), list(
            filter(lambda e: e['department'] == dept, records))))
        response.append(DepartmentSummary.parse_obj(
            dict(department=dept,
                 summary=Summary.parse_obj(dict(mean=str(round(sum(salary_list) / len(salary_list), 2) if salary_list else 0),
                                                min=str(min(salary_list) if salary_list else 0),
                                                max=str(max(salary_list) if salary_list else 0))))))
    return response


@record_routes.get('/department/summary/nested', response_model=List[DepartmentSummaryNested])
async def get_department_summary_nested(database: Database = Depends(get_db), table: Table = Depends(get_record_table)):
    records = await db_manager.get_all_records(database, table)

    departments = list(set([rec['department'] for rec in records]))
    response = []

    for dept in departments:
        sub_departments = list(set([rec['sub_department'] for rec in records if rec['department'] == dept]))
        sub_department_summary_list = []
        for sub_dept in sub_departments:
            salary_list = list(map(lambda d: int(d['salary']), list(
                filter(lambda e: e['sub_department'] == sub_dept, records))))
            sub_department_summary_list.append(SubDepartmentSummary.parse_obj(
                dict(sub_department=sub_dept,
                     summary=Summary.parse_obj(dict(mean=str(round(sum(salary_list) / len(salary_list), 2) if salary_list else 0),
                                                    min=str(min(salary_list) if salary_list else 0),
                                                    max=str(max(salary_list) if salary_list else 0))))))
        response.append(DepartmentSummaryNested.parse_obj(
            dict(department=dept, summary=sub_department_summary_list)))
    return response
