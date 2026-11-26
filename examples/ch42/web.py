"""Optional Django test adapter. Session integration seam; no public worker/maintenance routes."""
import json
import os
from pathlib import Path
import sqlite3
import time

import django
from django.conf import settings

from examples.ch23.authorization_service import AccessDenied
from examples.ch27.export_crypto import CannotOpen
from examples.ch42 import capstone as service
from examples.ch42.fixtures import dummy_keyrings

BASE = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("CASEBOOK_CH42_DB", BASE/"capstone.sqlite3"))
KEYRINGS = dummy_keyrings()  # Process-local dummy keys: test adapter, not persistent custody.
clock = lambda:int(time.time())


class PrivateResponses:
    def __init__(self,get_response): self.get_response = get_response
    def __call__(self,request):
        response = self.get_response(request)
        response["Cache-Control"] = "no-store"
        response["X-Content-Type-Options"] = "nosniff"
        return response


settings.configure(
    SECRET_KEY="public-ch42-fixture-only-never-deploy",
    DEBUG=False, ALLOWED_HOSTS=["testserver","localhost","127.0.0.1"], ROOT_URLCONF=__name__,
    INSTALLED_APPS=["django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions"],
    DATABASES={"default":{"ENGINE":"django.db.backends.sqlite3",
        "NAME":os.environ.get("CASEBOOK_CH42_AUTH_DB", str(BASE/"auth.sqlite3"))}},
    MIDDLEWARE=[f"{__name__}.PrivateResponses","django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware"],
    SESSION_ENGINE="django.contrib.sessions.backends.db",
    SESSION_COOKIE_NAME="__Host-casebook-session", SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax", SESSION_COOKIE_PATH="/",
    SESSION_COOKIE_DOMAIN=None, CSRF_COOKIE_SECURE=True, CSRF_COOKIE_HTTPONLY=True,
    CSRF_COOKIE_SAMESITE="Lax", CSRF_TRUSTED_ORIGINS=[],
    CSRF_FAILURE_VIEW=f"{__name__}.csrf_failure", DATA_UPLOAD_MAX_MEMORY_SIZE=4096,
    USE_TZ=True, DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
)
django.setup()

from django.core.exceptions import RequestDataTooBig
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.urls import path


def failure(status,code):
    return JsonResponse({"error":{"code":code}},status=status)


def csrf_failure(request,reason=""):
    return failure(403,"csrf_failed")


def identity(request):
    if not request.user.is_authenticated or not request.user.is_active:
        raise AccessDenied(403,"access_denied")
    return request.user.pk  # Authenticated Django fixture IDs bind explicitly to domain users.


def json_body(request):
    if request.content_type != "application/json" or len(request.body) > 4096:
        raise service.Problem(400,"invalid_request")
    def pairs(items):
        result = {}
        for key,value in items:
            if key in result: raise ValueError("duplicate key")
            result[key] = value
        return result
    def constant(value): raise ValueError("invalid JSON constant")
    try:
        return json.loads(request.body.decode("utf-8"),object_pairs_hook=pairs,parse_constant=constant)
    except (ValueError,UnicodeDecodeError,RecursionError) as exc:
        raise service.Problem(400,"invalid_request") from exc


def endpoint(request,workspace_id=None,job_id=None,operation="request"):
    method = "POST" if operation in ("request","expire") else "GET"
    if request.method != method:
        response = failure(405,"method_not_allowed")
        response["Allow"] = method
        return response
    try:
        user_id = identity(request)
        if operation == "csrf": return JsonResponse({"token":get_token(request)})
        common = dict(user_id=user_id,workspace_id=workspace_id,clock=clock)
        if operation == "request":
            result = service.request_export(DATABASE,**common,body=json_body(request),
                                             client_key=request.headers.get("Idempotency-Key"))
            return JsonResponse(result,status=202)
        common["job_id"] = job_id
        if operation == "status": return JsonResponse(service.status(DATABASE,**common))
        if operation == "expire":
            if json_body(request) != {}: raise service.Problem(400,"invalid_request")
            service.expire(DATABASE,**common)
            return HttpResponse(status=204)
        payload = service.collect(DATABASE,**common,keyrings=KEYRINGS)
        response = HttpResponse(payload,content_type="application/json")
        response["Content-Disposition"] = f'attachment; filename="export-{job_id}.json"'
        return response
    except (AccessDenied,service.Problem) as exc:
        return failure(exc.status,exc.code)
    except (sqlite3.Error,CannotOpen):
        return failure(503,"export_service_unavailable")
    except RequestDataTooBig:
        return failure(400,"invalid_request")


urlpatterns = [
    path("api/csrf/",endpoint,{"operation":"csrf"}),
    path("api/v1/workspaces/<int:workspace_id>/exports/",endpoint),
    path("api/v1/workspaces/<int:workspace_id>/exports/<int:job_id>/",endpoint,{"operation":"status"}),
    path("api/v1/workspaces/<int:workspace_id>/exports/<int:job_id>/content/",endpoint,{"operation":"content"}),
    path("api/v1/workspaces/<int:workspace_id>/exports/<int:job_id>/expire/",endpoint,{"operation":"expire"}),
]
