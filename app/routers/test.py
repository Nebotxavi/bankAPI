from fastapi import APIRouter, Depends

from ..models.general import Test
from ..storage.storage import StorageAccess

# TODO: To be removed

router = APIRouter(
    prefix="/test",
    tags=['Test']
)


@router.get('/', response_model=list[Test])
def test(client=Depends(StorageAccess.get_db)):
    # TODO: Error handling
    tests = client.test_database()
    list(map(lambda test: test.update(
        {"message": f"Message for name: {test['name']}"}), tests))

    return tests
