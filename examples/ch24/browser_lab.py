"""Isolated synthetic Django browser lab; run as a module from the repository root."""
import os
from pathlib import Path
import sys

import django
from django.conf import settings
from django.utils.csp import CSP


BASE_DIR = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("CASEBOOK_CH24_DB", BASE_DIR / "browser.sqlite3"))
LOCAL_HTTP = os.environ.get("CASEBOOK_LOCAL_HTTP") == "1"


class NoStoreMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Cache-Control"] = "no-store"
        return response


settings.configure(
    SECRET_KEY="casebook-ch24-synthetic-local-only-do-not-deploy",
    DEBUG=False,
    ALLOWED_HOSTS=["127.0.0.1", "localhost", "testserver"],
    ROOT_URLCONF=__name__,
    INSTALLED_APPS=["django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": str(DATABASE)}},
    MIDDLEWARE=[
        f"{__name__}.NoStoreMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.middleware.csp.ContentSecurityPolicyMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ],
    TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True,
                "OPTIONS": {"context_processors": [
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                ]}}],
    SESSION_ENGINE="django.contrib.sessions.backends.db",
    SESSION_COOKIE_NAME="casebook-local-session" if LOCAL_HTTP else "__Host-casebook-session",
    SESSION_COOKIE_SECURE=not LOCAL_HTTP,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_PATH="/",
    SESSION_COOKIE_DOMAIN=None,
    SESSION_COOKIE_AGE=900,
    CSRF_COOKIE_SECURE=not LOCAL_HTTP,
    CSRF_COOKIE_HTTPONLY=True,
    CSRF_COOKIE_SAMESITE="Lax",
    CSRF_TRUSTED_ORIGINS=[],
    SECURE_REFERRER_POLICY="same-origin",
    SECURE_CONTENT_TYPE_NOSNIFF=True,
    X_FRAME_OPTIONS="DENY",
    SECURE_CSP={"default-src": [CSP.NONE], "script-src": [CSP.NONE],
                "object-src": [CSP.NONE], "base-uri": [CSP.NONE],
                "form-action": [CSP.SELF], "frame-ancestors": [CSP.NONE]},
    DATA_UPLOAD_MAX_MEMORY_SIZE=4096,
    LOGIN_REDIRECT_URL="/",
    LOGOUT_REDIRECT_URL="/accounts/login/",
    USE_TZ=True,
)
django.setup()

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.core.management import call_command, execute_from_command_line
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import path
from django.views.decorators.http import require_GET, require_POST

from examples.ch23.authorization_service import (
    AccessDenied, positive_id, require_member, seed, unit, visible_rows,
)

PASSWORD = "Fictional browser notes cross quiet rivers 24!"  # Public fixture, never a real credential.


class TitleForm(forms.Form):
    title = forms.CharField(max_length=200, strip=False)
    expected_version = forms.IntegerField(min_value=1, max_value=2**63 - 1)

    def clean_title(self):
        title = self.cleaned_data["title"]
        if not title.strip() or any(ord(c) < 32 or 127 <= ord(c) <= 159
                                    or 0xD800 <= ord(c) <= 0xDFFF for c in title):
            raise forms.ValidationError("Enter a valid title.")
        return title


def identity(request):
    if not request.user.is_authenticated or not request.user.is_active:
        raise PermissionDenied
    return request.user.pk


def scoped_note(db, user_id, workspace_id, note_id):
    if not positive_id(note_id):
        raise Http404
    try:
        require_member(db, user_id, workspace_id)
        rows = visible_rows(db, user_id=user_id, workspace_id=workspace_id,
                            note_ids=[note_id], limit=1)
        if not rows:
            raise AccessDenied()
    except AccessDenied as exc:
        raise Http404 from exc
    # Read extra state only after the scoped note check, in this same short transaction.
    state = db.execute("SELECT state,version FROM notes WHERE workspace_id=? AND id=?",
                       (workspace_id, note_id)).fetchone()
    return {**rows[0], "state": state["state"], "version": state["version"]}


@require_GET
def note_page(request, workspace_id, note_id):
    user_id = identity(request)
    with unit(DATABASE) as db:
        note = scoped_note(db, user_id, workspace_id, note_id)
    return render(request, "notes/detail.html", {"note": note})


@require_POST
def change_title(request, workspace_id, note_id):
    user_id = identity(request)
    if (set(request.POST) - {"title", "expected_version", "csrfmiddlewaretoken"}
            or any(len(values) != 1 for _, values in request.POST.lists())):
        return HttpResponse("Invalid form.", status=400)
    form = TitleForm(request.POST)
    if not form.is_valid():
        return HttpResponse("Invalid form.", status=400)
    with unit(DATABASE, write=True) as db:
        note = scoped_note(db, user_id, workspace_id, note_id)
        if (note["state"] != "open" or note["version"] != form.cleaned_data["expected_version"]
                or note["version"] == 2**63 - 1):
            return HttpResponse("Conflict.", status=409)
        db.execute("""UPDATE notes SET title=?, version=version+1, updated_by=?
                      WHERE workspace_id=? AND id=?""",
                   (form.cleaned_data["title"], user_id, workspace_id, note_id))
    response = HttpResponse(status=303)
    response["Location"] = f"/workspaces/{workspace_id}/notes/{note_id}/"
    return response


@require_GET
def home(request):
    identity(request)
    return HttpResponse("Signed in. Open your fixture workspace note.", content_type="text/plain")


@require_GET
def csp_probe(request):
    # Benign synthetic marker: the enforced policy should block this inline script.
    return HttpResponse("<!doctype html><html><head><title>CSP fixture</title></head><body>"
                        "<p>CSP fixture</p><script>document.documentElement.dataset.cspProbe='ran';"
                        "</script></body></html>")


urlpatterns = [
    path("", home),
    path("csp-probe/", csp_probe),
    path("accounts/login/", LoginView.as_view(template_name="registration/login.html")),
    path("accounts/logout/", LogoutView.as_view()),
    path("workspaces/<int:workspace_id>/notes/<int:note_id>/", note_page, name="note"),
    path("workspaces/<int:workspace_id>/notes/<int:note_id>/title/", change_title, name="title"),
]


def title_fixture():
    with unit(DATABASE, write=True) as db:
        db.execute("UPDATE notes SET title=? WHERE id=101", ("A & B",))


def initialize():
    if DATABASE.exists():
        raise RuntimeError("Use a fresh synthetic database path; initialization never overwrites.")
    call_command("migrate", verbosity=0)
    seed(DATABASE)
    User = get_user_model()
    for user_id, username in ((1, "mina"), (2, "ravi"), (3, "lee")):
        User.objects.create_user(id=user_id, username=username, password=PASSWORD)
    title_fixture()


if __name__ == "__main__":
    if sys.argv[1:] == ["init"]:
        initialize()
        print("Synthetic browser fixtures initialized.")
    else:
        execute_from_command_line(sys.argv)
