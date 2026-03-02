from django.test import TestCase

from showcase.models import Partner


class PartnerModelTest(TestCase):
    def setUp(self):
        self.partner_first = Partner.objects.create(
            name="Partner A",
            description="Description A",
            icon="partners/icon_a.png",
            url="https://a.example.com",
            enable=True,
            order=1,
        )
        self.partner_second = Partner.objects.create(
            name="Partner B",
            description="Description B",
            icon="partners/icon_b.png",
            enable=True,
            order=2,
        )
        self.partner_disabled = Partner.objects.create(
            name="Partner C",
            description="Description C",
            icon="partners/icon_c.png",
            enable=False,
            order=0,
        )

    def tearDown(self):
        Partner.objects.all().delete()

    def test_str_returns_partner_name(self):
        self.assertEqual(str(self.partner_first), self.partner_first.name)

    def test_icon_url_property(self):
        self.assertEqual(self.partner_first.icon_url, "/uploads/partners/icon_a.png")

    def test_default_values(self):
        partner = Partner.objects.create(
            name="Partner Default",
            icon="partners/icon_default.png",
        )

        self.assertFalse(partner.enable)
        self.assertEqual(partner.order, 0)
        self.assertIsNone(partner.url)
        self.assertEqual(partner.description, "")

    def test_model_ordering(self):
        ordered_partners = list(Partner.objects.all())
        self.assertEqual(
            ordered_partners,
            [self.partner_disabled, self.partner_first, self.partner_second],
        )


class ShowcaseViewsTest(TestCase):
    def setUp(self):
        self.partner_enabled_1 = Partner.objects.create(
            name="Enabled A",
            description="Description A",
            icon="partners/enabled_a.png",
            url="https://enabled-a.example.com",
            enable=True,
            order=2,
        )
        self.partner_enabled_2 = Partner.objects.create(
            name="Enabled B",
            description="Description B",
            icon="partners/enabled_b.png",
            url="https://enabled-b.example.com",
            enable=True,
            order=1,
        )
        self.partner_disabled = Partner.objects.create(
            name="Disabled",
            description="Description C",
            icon="partners/disabled.png",
            enable=False,
            order=0,
        )

    def tearDown(self):
        Partner.objects.all().delete()

    def _assert_common_data(self, response):
        self.assertIn("partners_qs", response.context)
        self.assertIn("partners_json", response.context)
        self.assertIn("current_year", response.context)

        partners_qs = response.context["partners_qs"]
        self.assertEqual(
            list(partners_qs), [self.partner_enabled_2, self.partner_enabled_1]
        )

        partners_json = response.context["partners_json"]
        self.assertIn("Enabled A", partners_json)
        self.assertIn("Enabled B", partners_json)
        self.assertNotIn("Disabled", partners_json)

    def test_static_showcase_views_status_template_and_common_data(self):
        routes = [
            ("/", "home/main.html"),
            ("/contacts/", "contacts/main.html"),
            ("/membership/", "membership/main.html"),
            ("/partners/", "partners/main.html"),
            ("/events/", "events/main.html"),
            ("/services/", "services/main.html"),
        ]

        for url, template_name in routes:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)
                self._assert_common_data(response)

    def test_dynamic_showcase_views_status_template_and_common_data(self):
        routes = [
            ("/events/integration/", "events/integration/main.html"),
            ("/events/r2d/", "events/r2d/main.html"),
            ("/events/sdf/", "events/sdf/main.html"),
            ("/services/campus/", "services/campus/main.html"),
            ("/services/clubs/", "services/clubs/main.html"),
            ("/services/communication/", "services/communication/main.html"),
            ("/services/foyer/", "services/foyer/main.html"),
            ("/services/loan/", "services/loan/main.html"),
            ("/services/tickets/", "services/tickets/main.html"),
            ("/services/treasury/", "services/treasury/main.html"),
            ("/services/zeshop/", "services/zeshop/main.html"),
        ]

        for url, template_name in routes:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)
                self._assert_common_data(response)
