def test_health(test_app_with_db):
    response = test_app_with_db.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "environment": "dev",
        "testing": True,
        "db": "ok",
    }
