from django.urls import path
from .views import delete_user, threaded_conversation_view, unread_messages_view

urlpatterns = [
    path('user/delete/', delete_user, name='delete_user_account'),
    path('conversation/<int:user1_id>/<int:user2_id>/', threaded_conversation_view, name='threaded_conversation'),
    # --- ADD THE NEW URL ---
    path('messages/unread/', unread_messages_view, name='unread_messages'),
]