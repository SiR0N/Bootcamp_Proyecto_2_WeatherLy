from src.storage import Storage

def test_store_alert(tmp_path):
    file_path = tmp_path / "alerts.json"
    storage = Storage(str(file_path))

    alerta = {
        "date": "2026-04-27T14:30",
        "city": "Toledo",
        "type": "high_temp"
    }

    storage.add_record(alerta)

    data = storage.load_data()

    assert len(data) == 1
    assert data[0]["type"] == "high_temp"
    assert data[0]["city"] == "Toledo"