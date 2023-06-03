from fastapi import FastAPI, Depends
from .config import dbConfig

from .storage.storage import DatabaseType, StorageFactory, StorageAccess

app = FastAPI()

@app.on_event('startup')
def db_start():
    # TODO: error handling
    app.state.db = StorageFactory.get_storage(DatabaseType[dbConfig.db_type], dbConfig)

@app.get("/health")
async def root():
    return {"status": "OK"}

@app.get('/test')
def test(client = Depends(StorageAccess.get_db)):
    return client.test_database()