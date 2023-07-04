from app.utils.utils import Crypt, IdGenerator


def test_id_generator():
    id = IdGenerator.get_id()

    assert id
    assert type(id) == int
    assert len(str(id)) == 15


def test_crypt():
    password = "testing_password_888"

    hashed_password = Crypt.hash(password)

    assert Crypt.verify(password, hashed_password)
    assert hashed_password != password
