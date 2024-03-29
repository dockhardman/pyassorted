import pytest

from pyassorted.collections.sqlitedict import SqliteDict


@pytest.mark.asyncio
async def test_sqlite_dict():
    key = "a"
    cache = SqliteDict()
    assert len(cache) == 0

    cache[key] = 1

    # Get Operations
    assert len(cache) == 1
    assert cache[key] == 1
    assert cache.get(key) == 1
    assert cache.get("NO_KEY") == None
    assert cache.get("NO_KEY", "DEFAULT") == "DEFAULT"

    # Pop Operations
    _value = cache.pop(key)
    assert _value == 1
    assert len(cache) == 0
    cache[key] = _value

    # Contains Operations
    assert key in cache
    assert "NO_KEY" not in cache

    # Set Operations
    cache.set(key, 2.0)
    assert cache.get(key) == 2.0

    # Asynchronous Operations
    await cache.async_set(key, 3)
    assert (await cache.async_get(key)) == 3

    # Catching Errors
    try:
        cache["NO_KEY"]
        assert False
    except KeyError:
        pass
    try:
        cache[{"GG"}] = 5
        assert False
    except TypeError:
        pass

    # Delete Operations
    del cache[key]
    assert key not in cache


def test_sqlite_iteration():
    d = {"a": 1, "b": 2, "c": 3}
    cache = SqliteDict()

    for k, v in d.items():
        cache[k] = v

    assert len(cache) == len(d)

    for k, v in cache:
        assert d[k] == v
