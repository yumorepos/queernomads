from app import create_app


def test_core_routes_render():
    app = create_app({"TESTING": True, "DATABASE": "test_qn.db"})
    client = app.test_client()

    for route in ["/", "/cities", "/compare", "/methodology", "/community"]:
        resp = client.get(route)
        assert resp.status_code == 200
