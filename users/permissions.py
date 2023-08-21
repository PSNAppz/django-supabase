from rest_framework.exceptions import APIException
from rest_framework import permissions, status
from .models import UserAuthTime


class TooManyDevicesLoggedIn(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "You've been auto logged-out here as you have logged into another device"
    default_code = 'too_many_devices'


class DeactiveAccountException(APIException):
    status_code = 420
    default_detail = "Your account has been blocked. Please contact Support for assistance"
    default_code = 'permission_denied'


class DeviceIdException(APIException):
    status_code = 450
    default_detail = "Device Id is required"
    default_code = 'key_error'


class LimitUserDevices(permissions.BasePermission):
    """
    """
    def has_permission(self, request, view):
        max_user_count = 1
        user = request.user
        device_id = request.META.get('HTTP_DEVICEID', None)
        # Device id key validation
        if device_id is None and user.is_superuser == False:
            raise DeviceIdException()
        # User session validation
        if user is not None and user.is_superuser == False:
            # if request.auth is None:
            #     if request.session:
            #         auth_key = request.session.session_key
            # else:
            #     try:
            #         auth_key = str(request.auth['auth_time'])
            #     except:
            #         auth_key = str(request.auth)

            if not bool(request.user and request.user.is_authenticated):
                return False
            if not UserAuthTime.objects.filter(user=user, auth_key=device_id).exists():
                if UserAuthTime.objects.filter(user=user).count() < max_user_count:
                    user_auth = UserAuthTime.objects.create(
                        user=user,
                        auth_key=device_id
                    )
            user_auth_keys = UserAuthTime.objects.filter(user=user).order_by('id').distinct()[:max_user_count]
            if device_id not in [i.auth_key for i in user_auth_keys]:
                raise TooManyDevicesLoggedIn()
        return True


class DeactivateUserPermission(permissions.BasePermission):
    """
    """
    def has_permission(self, request, view):
        if not request.user.is_active:
            raise DeactiveAccountException()
        return True
