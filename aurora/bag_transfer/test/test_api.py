import json
from unittest.mock import patch

from bag_transfer.models import Archives, Organization, User
from django.test import TransactionTestCase
from django.urls import reverse


class APITest(TransactionTestCase):
    fixtures = ["complete.json"]

    def setUp(self):
        self.user = User.objects.get(username="admin")
        self.client.force_login(self.user)

    def assert_status_code(self, url, status_code):
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code, "Wrong HTTP status code, expecting {}".format(status_code))

    @patch("bag_transfer.lib.cleanup.CleanupRoutine.run")
    def test_update_transfer(self, mock_cleanup):
        """Asserts bad data can be updated."""
        new_values = {
            "process_status": Archives.ACCESSIONING_STARTED,
            "archivesspace_identifier": "/repositories/2/archival_objects/3",
            "archivesspace_parent_identifier": "/repositories/2/archival_objects/4"
        }

        for archive in Archives.objects.all():
            archive_data = self.client.get(
                reverse("archives-detail", kwargs={"pk": archive.pk}), format="json").json()
            for field in new_values:
                archive_data[field] = new_values[field]

            updated = self.client.put(
                reverse("archives-detail", kwargs={"pk": archive.pk}),
                data=json.dumps(archive_data),
                content_type="application/json")
            for field in new_values:
                self.assertEqual(updated.data[field], new_values[field], "{} not updated".format(field))
            mock_cleanup.assert_called_once()
            mock_cleanup.reset_mock()

    def test_schema_response(self):
        self.assert_status_code(reverse("schema"), 200)

    def test_health_check_response(self):
        self.assert_status_code(reverse("api_health_ping"), 200)

    def test_action_endpoints(self):
        """Asserts custom action endpoints return expected status code."""
        org = Organization.objects.get(name="Donor Organization").pk
        self.assert_status_code(reverse("organization-bagit-profile", kwargs={"pk": org}), 200)
        self.assert_status_code(reverse("organization-rights-statements", kwargs={"pk": org}), 200)
        self.assert_status_code(reverse("user-current"), 200)

    def test_list_views(self):
        """Asserts list endpoints return expected response."""
        self.assert_status_code(reverse("accession-list"), 200)
        self.assert_status_code(reverse("baglog-list"), 200)
        self.assert_status_code(reverse("organization-list"), 200)
        self.assert_status_code(reverse("user-list"), 200)
