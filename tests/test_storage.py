from src.storage import Storage


def test_add_two_records(tmp_path):
    file_path = tmp_path / "weather.json"    
    storage = Storage(str(file_path))

    registro_1 = {
        "date": "2026-04-27T14:30",
        "city": "Toledo",
        "temp": 25,
        "hum": 60,
        "wind": 15,
        "source": "test"
    }

    registro_2 = {
        "date": "2026-04-27T15:00",
        "city": "Albacete",
        "temp": 28,
        "hum": 55,
        "wind": 10,
        "source": "test"
    }

    storage.add_record(registro_1)
    storage.add_record(registro_2)

    data = storage.load_data()

    assert len(data) == 2
    assert data[0]["city"] == "Toledo"
    assert data[1]["city"] == "Albacete"


def test_ignore_duplicate_record(tmp_path):
    file_path = tmp_path / "weather.json"
    storage = Storage(str(file_path))

    registro = {
        "date": "2026-04-27T14:30",
        "city": "Toledo",
        "temp": 25,
        "hum": 60,
        "wind": 15,
        "source": "test"
    }

    storage.add_record(registro)
    storage.add_record(registro)

    data = storage.load_data()

    assert len(data) == 1


def test_add_new_record_after_duplicates(tmp_path):
    file_path = tmp_path / "weather.json"
    storage = Storage(str(file_path))

    registro_1 = {
        "date": "2026-04-27T14:30",
        "city": "Toledo",
        "temp": 25,
        "hum": 60,
        "wind": 15,
        "source": "test"
    }

    registro_2 = {
        "date": "2026-04-27T14:30",
        "city": "Toledo",
        "temp": 25,
        "hum": 60,
        "wind": 15,
        "source": "test"
    }

    registro_3 = {
        "date": "2026-04-27T16:00",
        "city": "Cuenca",
        "temp": 30,
        "hum": 50,
        "wind": 12,
        "source": "test"
    }

    storage.add_record(registro_1)
    storage.add_record(registro_2)
    storage.add_record(registro_3)

    data = storage.load_data()

    assert len(data) == 2
    assert data[0]["city"] == "Toledo"
    assert data[1]["city"] == "Cuenca"