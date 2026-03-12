"""Minimal route behavior tests for showcase-critical pages."""

import unittest

from app import create_app


class RouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_cities_route_returns_200(self):
        response = self.client.get("/cities")
        self.assertEqual(response.status_code, 200)

    def test_city_detail_valid_slug_returns_200(self):
        response = self.client.get("/cities/lisbon-portugal")
        self.assertEqual(response.status_code, 200)

    def test_city_detail_invalid_slug_returns_404(self):
        response = self.client.get("/cities/not-a-real-city")
        self.assertEqual(response.status_code, 404)

    def test_methodology_route_returns_200(self):
        response = self.client.get("/methodology")
        self.assertEqual(response.status_code, 200)

    def test_post_requires_auth_and_redirects(self):
        response = self.client.get("/post", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers.get("Location", ""))


if __name__ == "__main__":
    unittest.main()
