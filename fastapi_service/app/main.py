from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.api.auth_manager import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.api.routes import record_routes
from app.api.db import metadata, get_db, engine, get_record_table, dummy_record_db, fake_users_db
from app.api.models import Token

app = FastAPI()

app.include_router(record_routes)


@app.on_event("startup")
async def startup():
    metadata.drop_all(engine)
    metadata.create_all(engine)
    await get_db().connect()
    for rec in dummy_record_db:
        query = get_record_table().insert().values(**rec)
        await get_db().execute(query)


@app.on_event("shutdown")
async def shutdown():
    await get_db().disconnect()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
