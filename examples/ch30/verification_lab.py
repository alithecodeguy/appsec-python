from django.http import Http404, JsonResponse
from django.urls import path
from django.views.decorators.http import require_GET

from examples.ch24 import browser_lab as browser
from examples.ch23.authorization_service import AccessDenied, list_for_user


@require_GET
def note_list(request, workspace_id):
    user_id = browser.identity(request)
    try:
        rows = list_for_user(browser.DATABASE, user_id=user_id,
                             workspace_id=workspace_id, limit=50)
    except AccessDenied as exc:
        raise Http404 from exc
    return JsonResponse({"workspace_id": workspace_id, "notes": rows},
                        json_dumps_params={"ensure_ascii": False})


urlpatterns = [
    path("workspaces/<int:workspace_id>/notes/", note_list, name="note-list"),
    *browser.urlpatterns,
]
