"""Точка входа."""
import uvicorn
from db.db import pgsql
from db.routes.Authentication.route import route as route_one
from fastapi import FastAPI

app = FastAPI()
app.include_router(route_one, prefix='/api/Authentication')


if __name__ == '__main__':
    pgsql.create_all_tables()
    uvicorn.run(app, port=8081)
