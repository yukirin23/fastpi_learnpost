from app.calculation import add


def test_add():
    print("testing add function")
    sum = add(5, 3)
    assert sum == 8
