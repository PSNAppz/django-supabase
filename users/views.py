from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from djoser.views import UserViewSet as BaseUserViewSet

from .models import User

class UserViewSet(BaseUserViewSet):
    """
    API viewset for user
    """
    @action(methods=['POST'], detail=False, url_path='user_exist', url_name='user_exist', permission_classes=[])
    def user_exist(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number',None)
        try:
            user = User.objects.get(phone_number=phone_number)
            return Response({"status": True, "code":"user-exist", "message": "User already exists"},status=200)
        except User.DoesNotExist:
            return Response({"status": False, "code":"user-not-exist","message": "User does not exists"},status=200)
    
    # Create an endpoint to delete user if authenticated
    @action(methods=['POST'], detail=False, url_path='delete_user', url_name='delete_user', permission_classes=[IsAuthenticated])
    def delete_user(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return Response({"status": False, "code":"user-delete-failed", "message": "Admin user cannot be deleted"},status=200)
        user.delete()
        return Response({"status": True, "code":"user-deleted", "message": "User deleted successfully"},status=200)


