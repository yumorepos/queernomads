from app import create_app


def test_core_routes_render():
    app = create_app({"TESTING": True, "DATABASE": "test_qn.db"})
    client = app.test_client()

    for route in ["/", "/cities", "/compare", "/methodology", "/community"]:
        resp = client.get(route)
        assert resp.status_code == 200


def test_cities_preset_and_filtering():
    app = create_app({"TESTING": True, "DATABASE": "test_qn.db"})
    client = app.test_client()

    resp = client.get("/cities?preset=best_for_community&region=Europe&sort=name_asc")
    assert resp.status_code == 200
    assert b"Active ranking mode" in resp.data
    assert b"Best for community" in resp.data


def test_compare_skips_invalid_and_duplicate_inputs():
    app = create_app({"TESTING": True, "DATABASE": "test_qn.db"})
    client = app.test_client()

    resp = client.get("/compare?city=lisbon&city=lisbon&city=invalid-city")
    assert resp.status_code == 200
    assert b"skipped" in resp.data or b"Duplicate" in resp.data
