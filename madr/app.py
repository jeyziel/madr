from fastapi import FastAPI

from madr.routers import romancists

app = FastAPI()

app.include_router(romancists.router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
