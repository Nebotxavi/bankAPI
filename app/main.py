from fastapi import FastAPI, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from .config import dbConfig
from .storage.storage import DatabaseType, StorageFactory, StorageAccess
from .models.API_models.test import Test

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event('startup')
def db_start():
    # TODO: error handling
    app.state.db = StorageFactory.get_storage(DatabaseType[dbConfig.db_type], dbConfig)

@app.get("/health")
async def root():
    return {"status": "OK"}

@app.get('/test', response_model=List[Test])
def test(client = Depends(StorageAccess.get_db)):
    # Error handling
    tests = client.test_database()
    list(map(lambda test: test.update({"message": f"Message for name: {test['name']}"}) , tests))

    return tests