"""Точка входа."""
import uvicorn
from db.db import pgsql
from db.routes.Authentication.route import route as route_one
from db.routes.Accaunt.route import route as route_two
from fastapi import FastAPI

app = FastAPI()
app.include_router(
    route_one, prefix='/api/Authentication',
    tags=['Authentication'],
    )

app.include_router(route_two, prefix='/api/Accounts', tags=['Accounts'])


if __name__ == '__main__':
    pgsql.create_all_tables()
    uvicorn.run(app, port=8081)
