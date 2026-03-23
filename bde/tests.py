from django.test import SimpleTestCase, override_settings

from bde.generate_robots import get_robots_content


class SEOInfrastructureTests(SimpleTestCase):
    def test_sitemap_is_available(self):
        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/members/")
        self.assertContains(response, "/events/")

    @override_settings(DEBUG=True)
    def test_robots_declares_sitemap(self):
        robots = get_robots_content()

        self.assertIn("Sitemap: /sitemap.xml", robots)
