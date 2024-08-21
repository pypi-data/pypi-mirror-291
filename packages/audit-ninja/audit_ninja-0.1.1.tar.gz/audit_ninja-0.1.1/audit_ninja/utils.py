import json
import datetime as dt
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import smart_str
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import NOT_PROVIDED, DateTimeField

def get_field_value(obj, field):
    """Get the value of a given model instance field.

    :param obj: The model instance.
    :type obj: Model
    :param field: The field you want to find the value of.
    :type field: Any
    :return: The value of the field as a string.
    :rtype: str
    """
    if isinstance(field, DateTimeField):
        # DateTimeFields are timezone-aware, so we need to convert the field
        # to its naive form before we can accurately compare them for changes.
        try:
            value = field.to_python(getattr(obj, field.name, None))
            if value is not None and settings.USE_TZ and not timezone.is_naive(value):
                value = timezone.make_naive(value, timezone=dt.timezone.utc)
        except ObjectDoesNotExist:
            value = field.default if field.default is not NOT_PROVIDED else None
    else:
        try:
            value = smart_str(getattr(obj, field.name, None))
        except ObjectDoesNotExist:
            value = field.default if field.default is not NOT_PROVIDED else None

    return value


def model_delta(old_model, new_model):
    """Provide delta/difference between two models.

    :param old: The old state of the model instance.
    :type old: Model
    :param new: The new state of the model instance.
    :type new: Model
    :return: A dictionary with the names of the changed fields as keys and a
             two tuple of the old and new field values
             as value.
    :rtype: dict
    """
    delta = {}
    fields = new_model._meta.fields
    for field in fields:
        old_value = get_field_value(old_model, field)
        new_value = get_field_value(new_model, field)
        if old_value != new_value:
            delta[field.name] = [smart_str(old_value), smart_str(new_value)]

    if len(delta) == 0:
        delta = None

    return delta


def get_m2m_field_name(model, instance):
    """Find M2M field name on instance.

    Called from m2m_changed signal
    :param model: m2m_changed signal model.
    :type model: Model
    :param instance:m2m_changed signal instance.
    :type new: Model
    :return: ManyToManyField name of instance related to model.
    :rtype: str
    """
    for x in model._meta.related_objects:
        if x.related_model().__class__ == instance.__class__:
            return x.remote_field.name
    return None


def should_propagate_exceptions():
    """Whether Django Easy Audit should propagate signal handler exceptions.

    :rtype: bool
    """
    return getattr(settings, "DJANGO_AUDIT_NINJA_PROPAGATE_EXCEPTIONS", False)


def get_user_dict(user, headers = None):
    '''
    # "id": itr["id"],
    # "name": itr["name"],
    # "mobile_number": itr["mobile_number"],
    # "email_id": itr["email_id"],
    # "employee_id": itr["employee_id"],
    # "businessrole_id": itr["businessrole_id"],
    # "businessrole_name": itr["businessrole__name"]

    # "user_id": itr["user_id"],
    # "user_username": itr["user__username"],
    # "user_is_active": itr["user__is_active"]

    # "business_id": itr["business_id"],
    # "business_name": itr["business__name"],
    # "business_logo": itr["business__logo"],
    # "business_type_name": itr["business__type__name"],
    # "business_mobile_number": itr["business__mobile_number"],
    # "business_email_id": itr["business__email_id"],
    # "department_id": itr["department_id"],
    # "department_name": itr["department__name"]
    '''
                        
    if not user and headers:
        if isinstance(headers,str):
            headers = json.loads(headers)
        if headers.get('User-Data'):
            headers = headers.get('User-Data')
            if isinstance(headers,str):
                headers = json.loads(headers)
        user_profile_data = headers.get("user_profile_data", {})
        business_data = headers.get("business_data", {})
        user_data = headers.get("user_data", {})

        return {
            'id': user_profile_data.get("id", None),
            'name': user_profile_data.get("name", None),
            'email_id': user_profile_data.get("email_id", None),
            'employee_id': user_profile_data.get("employee_id", None),
            'mobile_number': user_profile_data.get("mobile_number", None),
            'businessrole_id': user_profile_data.get("businessrole_id", None),
            'businessrole_name': user_profile_data.get("businessrole_name", None),
            'user_id': user_data.get("user_id", None),
            'username': user_data.get("user_username", None),
            'is_active': user_data.get("user_is_active", None),
            'last_login': user_data.get("last_login", None),
            'date_joined': user_data.get("date_joined", None),
            "business_id": business_data.get("business_id"),
            "business_name": business_data.get("business_name"),
            "business_type_name": business_data.get("business_type_name"),
            "business_mobile_number": business_data.get("business_mobile_number"),
            "business_email_id": business_data.get("business_email_id"),
            "department_id": business_data.get("department_id"),
            "department_name": business_data.get("department_name")
            }

    return {
        'id': getattr(user, "id", None),
        'username': getattr(user, "username", None),
        'first_name': getattr(user, "first_name", None),
        'last_name': getattr(user, "last_name", None),
        'email': getattr(user, "email", None),
        'is_active': getattr(user, "is_active", None),
        'is_staff': getattr(user, "is_staff", None),
        'is_superuser': getattr(user, "iis_superuserd", None),
        'last_login': getattr(user, "last_login", None),
        'date_joined': getattr(user, "date_joined", None),
    }
    