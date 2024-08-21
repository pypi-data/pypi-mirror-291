from django.contrib.auth import get_user_model, signals
from django.db import transaction
from django.utils.module_loading import import_string
from audit_ninja.constants import *
from audit_ninja.middleware.audit_ninja import get_current_request
from audit_ninja.settings import (
    LOGGING_BACKEND,
    REMOTE_ADDR_HEADER,
    WATCH_AUTH_EVENTS,
)
from audit_ninja.utils import should_propagate_exceptions

audit_logger = import_string(LOGGING_BACKEND)()


def user_logged_in(sender, request, user, **kwargs):
    try:
        with transaction.atomic():
            audit_logger.login(
                {
                    "login_type": LOGIN,
                    "username": getattr(user, user.USERNAME_FIELD),
                    "user_id": getattr(user, "id", None),
                    "remote_ip": request.META.get(REMOTE_ADDR_HEADER, ""),
                }
            )
    except Exception:
        if should_propagate_exceptions():
            raise


def user_logged_out(sender, request, user, **kwargs):
    try:
        with transaction.atomic():
            audit_logger.login(
                {
                    "login_type": LOGOUT,
                    "username": getattr(user, user.USERNAME_FIELD),
                    "user_id": getattr(user, "id", None),
                    "remote_ip": request.META.get(REMOTE_ADDR_HEADER, ""),
                }
            )
    except Exception:
        if should_propagate_exceptions():
            raise


def user_login_failed(sender, credentials, **kwargs):
    try:
        with transaction.atomic():
            request = get_current_request()
            user_model = get_user_model()
            audit_logger.login(
                {
                    "login_type": FAILED,
                    "username": credentials[user_model.USERNAME_FIELD],
                    "remote_ip": request.META.get(REMOTE_ADDR_HEADER, ""),
                }
            )
    except Exception:
        if should_propagate_exceptions():
            raise


if WATCH_AUTH_EVENTS:
    signals.user_logged_in.connect(
        user_logged_in, dispatch_uid="audit_ninja_signals_logged_in"
    )
    signals.user_logged_out.connect(
        user_logged_out, dispatch_uid="audit_ninja_signals_logged_out"
    )
    signals.user_login_failed.connect(
        user_login_failed, dispatch_uid="audit_ninja_signals_login_failed"
    )
