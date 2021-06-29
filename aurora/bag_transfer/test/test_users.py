import random
from unittest.mock import patch

from bag_transfer.models import Organization, User
from django.test import TransactionTestCase
from django.urls import reverse


class UserTestCase(TransactionTestCase):
    fixtures = ["complete.json"]

    def setUp(self):
        self.client.force_login(User.objects.get(username="admin"))

    def assert_status_code(self, method, url, data, status_code):
        response = getattr(self.client, method)(url, data)
        self.assertEqual(response.status_code, status_code)
        return response

    def test_user_model_methods(self):
        """Test user model methods."""
        self.has_privs()
        self.in_group()
        self.is_archivist()
        self.is_user_active()
        self.permissions_by_group()
        self.save_test()

    def has_privs(self):
        for username, assert_true, assert_false, privs in [
                ("donor", [], ["is_archivist", "can_appraise", "is_manager"], None),
                ("manager", ["is_archivist", "can_appraise", "is_manager"], [], "MANAGING"),
                ("accessioner", ["is_archivist"], ["can_appraise", "is_manager"], "ACCESSIONER"),
                ("appraiser", ["is_archivist", "can_appraise"], ["is_manager"], "APPRAISER")]:
            user = User.objects.get(username=username)
            for meth in assert_true:
                self.assertTrue(
                    getattr(user, meth)(),
                    "User {} is unable to perform function {}".format(user, meth))
            for meth in assert_false:
                self.assertFalse(
                    getattr(user, meth)(),
                    "User {} should not be able to perform function {}".format(
                        user, meth))
            if privs:
                self.assertTrue(user.has_privs(privs))
            else:
                for priv in ["MANAGING", "ACCESSIONER", "APPRAISER"]:
                    self.assertFalse(user.has_privs(priv))

    def in_group(self):
        group = random.choice(["appraisal_archivists", "managing_archivists", "accessioning_archivists"])
        user = random.choice(User.objects.filter(groups__name=group))
        self.assertTrue(user.in_group(group))
        self.assertFalse(user.in_group("foo"))

    def is_archivist(self):
        archivist = random.choice(User.objects.filter(is_staff=True))
        non_archivist = random.choice(User.objects.filter(is_staff=False))
        self.assertTrue(archivist.is_archivist())
        self.assertFalse(non_archivist.is_archivist())

    def is_user_active(self):
        user = random.choice(User.objects.filter(is_active=True))
        self.assertEqual(user.is_user_active(user, user.organization), user)
        self.assertEqual(user.is_user_active(user, 1000), None)
        user.is_active = False
        user.save()
        self.assertEqual(user.is_user_active(user, user.organization), None)

    def permissions_by_group(self):
        user = User.objects.get(username="admin")
        self.assertTrue(user.permissions_by_group(User.APPRAISER_GROUPS))
        user = random.choice(User.objects.filter(groups__name="appraisal_archivists"))
        self.assertTrue(user.permissions_by_group(User.APPRAISER_GROUPS))
        self.assertFalse(user.permissions_by_group(User.ACCESSIONER_GROUPS))

    @patch("bag_transfer.lib.RAC_CMD.del_from_org")
    @patch("bag_transfer.lib.RAC_CMD.add2grp")
    @patch("bag_transfer.lib.RAC_CMD.add_user")
    def save_test(self, mock_add_user, mock_add2grp, mock_del):
        """Asserts behaviors for new and updated users."""
        mock_add_user.return_value = True
        user = random.choice(User.objects.all())
        old_org = user.organization
        user.organization = random.choice(Organization.objects.all().exclude(id=old_org.pk))
        user.save()
        mock_del.assert_called_once()
        mock_add2grp.assert_called_once()

        User.objects.create_user(
            username="jdoe",
            is_active=True,
            first_name="John",
            last_name="Doe",
            email="test@example.org",
            organization=random.choice(Organization.objects.all()))
        mock_add_user.assert_called_once()
        self.assertEqual(mock_add2grp.call_count, 2)

    def test_user_views(self):
        """Ensures correct HTTP status codes are received for views."""
        for view in ["users:detail", "users:edit"]:
            self.assert_status_code(
                "get", reverse(view, kwargs={"pk": random.choice(User.objects.filter(archives__isnull=False)).pk}), None, 200)
        for view in ["users:add", "users:list", "users:password-change"]:
            self.assert_status_code("get", reverse(view), None, 200)

        user_data = {
            "is_active": True,
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.org",
            "organization": random.choice(Organization.objects.all()).pk
        }
        self.assert_status_code("post", reverse("users:add"), user_data, 200)
        user_data["active"] = False
        self.assert_status_code(
            "post", reverse("users:edit", kwargs={"pk": random.choice(User.objects.all()).pk}), user_data, 200)

        # ensure logged out users are redirected to splash page
        self.client.logout()
        response = self.assert_status_code("get", reverse("splash"), None, 302)
        self.assertTrue(response.url.startswith(reverse("login")))
