from django.urls import path
from .views import delete_user

urlpatterns = [
    # This URL will handle the user deletion requests.
    path('user/delete/', delete_user, name='delete_user_account'),
]