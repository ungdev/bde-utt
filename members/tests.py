from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from .models import Team, UserTeam
from members.models import UserProfile


class MembersBoardViewsTest(TestCase):
    def setUp(self):
        self.board = Team.objects.create(name="Bureau")
        self.team = Team.objects.create(name="TestTeam")
        self.user = User.objects.create(
            username="testuser",
            first_name="testfirstname",
            last_name="testlastname",
        )
        self.ut_board = UserTeam.objects.create(
            user=self.user,
            team=self.board,
            role="PRESIDENT",
        )
        self.ut_testteam = UserTeam.objects.create(
            user=self.user,
            team=self.team,
            role="MEMBER",
        )
        self.up = UserProfile.objects.create(
            user=self.user,
            picture="fake_picture.jpg",
            description="test_description",
        )

    def tearDown(self):
        UserProfile.objects.all().delete()
        UserTeam.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

    def test_status_and_template(self):
        response = self.client.get("/members/board/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "board.html")

    def test_common_data(self):
        response = self.client.get("/members/board/")
        self.assertIn("partners_qs", response.context)
        self.assertIn("partners_json", response.context)

    def test_members_context(self):
        response = self.client.get("/members/board/")

        self.assertIn("members", response.context)

        members = response.context["members"]
        self.assertIsInstance(members, list)
        self.assertTrue(
            any(
                m["first_name"] == self.ut_board.user.first_name
                and m["last_name"] == self.ut_board.user.last_name
                for m in members
            )
        )

        member = next(
            m
            for m in members
            if m["first_name"] == self.ut_board.user.first_name
            and m["last_name"] == self.ut_board.user.last_name
        )

        self.assertIsInstance(member["role_display"], str)
        self.assertTrue(member["role_display"] == self.ut_board.role_display)

        self.assertIsInstance(member["profile"], UserProfile)

        self.assertIsInstance(member["first_name"], str)
        self.assertIsInstance(member["last_name"], str)

        self.assertTrue(member["first_name"] == self.user.first_name)
        self.assertTrue(member["last_name"] == self.user.last_name)

        self.assertIsInstance(member["other_teams"], QuerySet[UserTeam, UserTeam])


class MembersMembersViewTest(TestCase):
    def setUp(self):
        self.board = Team.objects.create(name="Bureau")
        self.team = Team.objects.create(name="TestTeam")
        self.user = User.objects.create(
            username="testuser",
            first_name="testfirstname",
            last_name="testlastname",
        )
        self.ut_testteam = UserTeam.objects.create(
            user=self.user,
            team=self.team,
            role="MEMBER",
        )
        self.up = UserProfile.objects.create(
            user=self.user,
            picture="fake_picture.jpg",
            description="test_description",
        )

    def tearDown(self):
        UserProfile.objects.all().delete()
        UserTeam.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

    def test_status_and_template(self):
        response = self.client.get("/members/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members.html")

    def test_common_data(self):
        response = self.client.get("/members/")
        self.assertIn("partners_qs", response.context)
        self.assertIn("partners_json", response.context)

    def test_teams_context(self):
        response = self.client.get("/members/")

        self.assertIn("teams", response.context)

        teams = response.context["teams"]
        self.assertIsInstance(teams, list)
        self.assertTrue(any(t["name"] == self.ut_testteam.team.name for t in teams))

        test_team = next(t for t in teams if t["name"] == self.ut_testteam.team.name)

        self.assertIsInstance(test_team["members"], list)
        for m in test_team["members"]:
            self.assertIsInstance(m["role_display"], str)
            self.assertTrue(m["role_display"] == self.ut_testteam.role_display)

            self.assertIsInstance(m["profile"], UserProfile)

            self.assertIsInstance(m["first_name"], str)
            self.assertIsInstance(m["last_name"], str)

            self.assertTrue(m["first_name"] == self.user.first_name)
            self.assertTrue(m["last_name"] == self.user.last_name)
