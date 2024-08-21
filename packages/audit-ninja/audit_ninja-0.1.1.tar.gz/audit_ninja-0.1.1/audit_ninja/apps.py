from django.apps import AppConfig

class AuditNinjaConfig(AppConfig):
    name = "audit_ninja"
    verbose_name = "Audit Ninja Application"
    default_auto_field = "django.db.models.AutoField"

    print("READYYYYY")
    def ready(self):
        from audit_ninja.signals import (  # noqa: F401
            auth_signals,
            model_signals,
            request_signals,
        )

