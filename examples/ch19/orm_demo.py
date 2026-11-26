"""Run with: python manage.py shell < orm_demo.py (synthetic database only)."""
from django.db import transaction

from notes.models import Note, Workspace


print("workspaces:", list(Workspace.objects.order_by("id").values_list("id", "name")))
print("Alpha seed:", list(
    Note.objects.filter(workspace_id=1, pk=101).values_list("id", "title")
))
print("wrong workspace:", list(
    Note.objects.filter(workspace_id=2, pk=101).values_list("id", "title")
))

with transaction.atomic():
    note = Note(id=103, workspace_id=1, title="برنامه انتشار", body="Alpha encoding fixture")
    note.full_clean()
    note.save(force_insert=True)

stored = Note.objects.get(workspace_id=1, pk=103)
print("stored:", stored.id, stored.workspace_id, stored.title, stored.body)
