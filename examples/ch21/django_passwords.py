"""Isolated Django password API example; all passwords below are public fixtures."""
import django
from django.conf import settings


settings.configure(
    SECRET_KEY="casebook-ch21-local-only-do-not-deploy",
    INSTALLED_APPS=["django.contrib.auth", "django.contrib.contenttypes"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    AUTH_PASSWORD_VALIDATORS=[
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
         "OPTIONS": {"min_length": 15}},
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ],
    USE_TZ=True,
)
django.setup()

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.password_validation import validate_password
from django.core.management import call_command


# An in-memory demonstration database, unrelated to chapter 19's service file.
call_command("migrate", verbosity=0)
User = get_user_model()
mina = User(username="mina", email="mina@example.test")
password = "Fictional lanterns cross quiet rivers 21!"
validate_password(password, user=mina)
mina.set_password(password)
mina.save()
print("Django:", django.get_version())
print("correct password:", mina.check_password(password))
print("wrong password:", mina.check_password("wrong public fixture"))
first_encoding = mina.password
mina.set_password(password)
mina.save()
print("same password, different encoding:", first_encoding != mina.password)
hasher = identify_hasher(mina.password)
print("algorithm:", hasher.algorithm)
print("work factor:", hasher.decode(mina.password)["iterations"])
print("successful sign-in:", authenticate(username="mina", password=password) is not None)
mina.is_active = False
mina.save(update_fields=["is_active"])
print("disabled account denied:", authenticate(username="mina", password=password) is None)
