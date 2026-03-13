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


def test_city_detail_for_existing_and_new_city_slugs():
    app = create_app({"TESTING": True, "DATABASE": "test_qn.db"})
    client = app.test_client()

    for slug in ["lisbon", "berlin", "barcelona", "taipei"]:
        resp = client.get(f"/cities/{slug}")
        assert resp.status_code == 200


def test_prefilled_compare_demo_route():
    app = create_app({"TESTING": True, "DATABASE": "test_qn.db"})
    client = app.test_client()

    resp = client.get("/compare?city=berlin&city=lisbon")
    assert resp.status_code == 200
    assert b"Berlin" in resp.data
    assert b"Lisbon" in resp.data
