from io import StringIO

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import Resolver404, resolve

from notes.models import Note, Workspace


class ServiceTests(TestCase):
    fixtures = ["demo.json"]

    def test_seed_has_two_workspaces_and_private_notes(self):
        self.assertEqual(
            list(Workspace.objects.order_by("id").values_list("id", "name")),
            [(1, "Alpha"), (2, "Beta")],
        )
        self.assertEqual(
            list(Note.objects.order_by("id").values_list("id", "workspace_id")),
            [(101, 1), (202, 2)],
        )

    def test_anonymous_health_is_public_and_contains_no_note_data(self):
        # No login, cookies or fixture identity is supplied.
        with self.assertNumQueries(0):
            response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_health_rejects_post(self):
        response = self.client.post("/health/", data={})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response["Allow"], "GET")

    def test_anonymous_cannot_read_note_content(self):
        # Prove the private data exists before checking HTTP denial.
        notes = list(Note.objects.all())
        self.assertEqual(len(notes), 2)
        private_values = [value for note in notes for value in (note.title, note.body)]
        for path in (
            "/notes/", "/notes/101/", "/notes/202/",
            "/workspaces/1/notes/101/", "/workspaces/2/notes/202/",
            "/admin/",
        ):
            with self.subTest(path=path):
                with self.assertRaises(Resolver404):
                    resolve(path)
                with self.assertNumQueries(0):
                    response = self.client.get(path)
                self.assertEqual(response.status_code, 404)
                for value in private_values:
                    self.assertNotIn(value.encode("utf-8"), response.content)

    def test_workspace_filter_requires_both_identifiers(self):
        self.assertTrue(Note.objects.filter(workspace_id=1, pk=101).exists())
        self.assertFalse(Note.objects.filter(workspace_id=2, pk=101).exists())
        self.assertTrue(Note.objects.filter(workspace_id=2, pk=202).exists())

    def test_unicode_note_round_trip_and_private_default(self):
        note = Note(id=103, workspace_id=1, title="برنامه انتشار", body="Alpha encoding fixture")
        note.full_clean()
        note.save(force_insert=True)
        stored = Note.objects.get(workspace_id=1, pk=103)
        self.assertEqual((stored.title, stored.body), (note.title, note.body))
        response = self.client.get("/notes/103/")
        self.assertEqual(response.status_code, 404)
        self.assertNotIn(stored.title.encode("utf-8"), response.content)
        self.assertNotIn(stored.body.encode("utf-8"), response.content)

    def test_validation_rejects_an_empty_title_before_write(self):
        before = list(Note.objects.order_by("id").values())
        note = Note(id=103, workspace_id=1, title="", body="Rejected fixture")
        with self.assertRaises(ValidationError):
            note.full_clean()
        self.assertEqual(list(Note.objects.order_by("id").values()), before)

    def test_workspace_with_notes_cannot_be_deleted(self):
        with self.assertRaises(ProtectedError):
            Workspace.objects.get(pk=1).delete()
        self.assertTrue(Workspace.objects.filter(pk=1).exists())
        self.assertTrue(Note.objects.filter(workspace_id=1, pk=101).exists())

    def test_reloading_seed_preserves_fixture_state(self):
        before = list(Note.objects.order_by("id").values())
        call_command("loaddata", "demo", stdout=StringIO())
        self.assertEqual(Workspace.objects.count(), 2)
        self.assertEqual(list(Note.objects.order_by("id").values()), before)
