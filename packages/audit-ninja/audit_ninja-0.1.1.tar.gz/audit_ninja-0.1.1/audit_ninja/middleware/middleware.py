from audit_ninja.managers import CustomManager
from django.db import models

class CustomManagerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Apply custom manager to all models
        for model in models.get_models():
            print(model)
            if not hasattr(model, 'objects'):
                continue
            if not isinstance(model.objects, CustomManager):
                model.objects = CustomManager(model=model)

        response = self.get_response(request)
        return response
