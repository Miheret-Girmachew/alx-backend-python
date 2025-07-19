
from django.urls import path
from .views import delete_user, threaded_conversation_view

urlpatterns = [
    path('user/delete/', delete_user, name='delete_user_account'),
    # New URL for fetching a threaded conversation between two users
    path('conversation/<int:user1_id>/<int:user2_id>/', threaded_conversation_view, name='threaded_conversation'),
]