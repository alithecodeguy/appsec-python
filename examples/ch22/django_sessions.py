"""Django session APIs in an isolated fixture; no public login routes."""
import django
from django.conf import settings

settings.configure(
    SECRET_KEY="casebook-ch22-local-only-do-not-deploy",
    INSTALLED_APPS=["django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    SESSION_ENGINE="django.contrib.sessions.backends.db",
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_NAME="__Host-casebook-session",
    SESSION_COOKIE_PATH="/",
    SESSION_COOKIE_DOMAIN=None,
    SESSION_COOKIE_AGE=900,
    SESSION_SAVE_EVERY_REQUEST=False,
    USE_TZ=True,
)
django.setup()

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.management import call_command
from django.http import HttpResponse
from django.test import RequestFactory

call_command("migrate", verbosity=0)
User = get_user_model()
password = "Fictional sessions cross quiet rivers 22!"
mina = User.objects.create_user(username="mina", password=password)
factory = RequestFactory()
sessions = SessionMiddleware(lambda request: HttpResponse("ok"))
authentication = AuthenticationMiddleware(lambda request: HttpResponse("ok"))


def request_for(key=None):
    request = factory.get("/", secure=True)
    if key is not None:
        request.COOKIES[settings.SESSION_COOKIE_NAME] = key
    sessions.process_request(request)
    authentication.process_request(request)
    return request


request = request_for()
request.session["locale"] = "en"
request.session.save()
anonymous_key = request.session.session_key
user = authenticate(username="mina", password=password)
assert user is not None
login(request, user)
response = sessions.process_response(request, HttpResponse("ok"))
authenticated_key = request.session.session_key
print("Django:", django.get_version())
print("session rotated:", authenticated_key != anonymous_key)
print("old session removed:", not SessionStore(session_key=anonymous_key).exists(anonymous_key))
print("new session authenticated:", request_for(authenticated_key).user.is_authenticated)
cookie = response.cookies[settings.SESSION_COOKIE_NAME]
print("cookie flags:", bool(cookie["secure"]), bool(cookie["httponly"]), cookie["samesite"])

# Simulate the password change that chapter 21 requires after recovery.
# Do not preserve the old session with update_session_auth_hash in this reset policy.
mina.set_password("Replacement fictional session password 22!")
mina.save()
print("old session refused after password change:", not request_for(authenticated_key).user.is_authenticated)
new_request = request_for()
user = authenticate(username="mina", password="Replacement fictional session password 22!")
assert user is not None
login(new_request, user)
sessions.process_response(new_request, HttpResponse("ok"))
logout_key = new_request.session.session_key
logout(new_request)
print("logout removed server session:", not SessionStore(session_key=logout_key).exists(logout_key))
print("logged-out session refused:", not request_for(logout_key).user.is_authenticated)
