from pydantic import BaseModel
from typing import Optional, List


class Record(BaseModel):
    id: int
    name: str
    salary: str
    currency: Optional[str] = "USD"
    department: str
    sub_department: str
    on_contract: Optional[str] = None


class RecordIn(BaseModel):
    name: str
    salary: str
    currency: Optional[str] = "USD"
    department: str
    sub_department: str
    on_contract: Optional[str] = None


class Summary(BaseModel):
    mean: str
    min: str
    max: str


class DepartmentSummary(BaseModel):
    department: str
    summary: Summary


class SubDepartmentSummary(BaseModel):
    sub_department: str
    summary: Summary


class DepartmentSummaryNested(BaseModel):
    department: str
    summary: List[SubDepartmentSummary]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    username: str
    password: str
