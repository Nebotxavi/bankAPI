from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import dbConfig
from .storage.storage import DatabaseType, StorageFactory
from .routers import test, products, customers

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(test.router)
app.include_router(products.router)
app.include_router(customers.router)

@app.on_event('startup')
def db_start():
    # TODO: error handling
    app.state.db = StorageFactory.get_storage(DatabaseType[dbConfig.db_type], dbConfig)

@app.get("/health")
async def root():
    return {"status": "OK"}

