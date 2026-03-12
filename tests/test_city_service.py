"""Minimal tests for city discovery service behavior."""

import unittest

from app.services.city_service import CityDiscoveryParams, get_all_cities


class CityServiceTests(unittest.TestCase):
    def test_filters_by_region_and_threshold(self):
        params = CityDiscoveryParams(region="Europe", min_inclusivity=8.5)
        cities = get_all_cities(params)

        self.assertEqual(len(cities), 1)
        self.assertEqual(cities[0].slug, "berlin-germany")

    def test_sorts_by_name_ascending(self):
        params = CityDiscoveryParams(sort="name")
        cities = get_all_cities(params)

        self.assertEqual([city.name for city in cities], ["Berlin", "Lisbon", "Mexico City"])

    def test_search_matches_country_or_city_name(self):
        params = CityDiscoveryParams(q="mexico")
        cities = get_all_cities(params)

        self.assertEqual(len(cities), 1)
        self.assertEqual(cities[0].slug, "mexico-city-mexico")


if __name__ == "__main__":
    unittest.main()
