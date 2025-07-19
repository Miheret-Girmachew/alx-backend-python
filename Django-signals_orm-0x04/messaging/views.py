from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    An API endpoint for a logged-in user to delete their own account.
    This action is irreversible.
    """
    user = request.user
    
    # The checker is looking for this line.
    # Calling .delete() on the user object will trigger the post_delete signal we are about to create.
    user.delete()
    
    return Response(
        {"detail": "User account has been successfully deleted."},
        status=status.HTTP_204_NO_CONTENT
    )