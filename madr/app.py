from fastapi import FastAPI

from madr.routers import romancists, books, users

app = FastAPI()

app.include_router(romancists.router)
app.include_router(books.router)
app.include_router(users.router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
