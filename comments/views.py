from datetime import datetime

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .models import Comment
from .serializers import CommentSerializer
from events.models import Events
from users.authentication import AuthenticationMiddleware, IsAuthenticatedUser


# Create your views here.
@api_view(["POST"])
@authentication_classes(AuthenticationMiddleware)
@permission_classes(IsAuthenticatedUser)
def create_comment(request, event_id, *args, **kwargs):
    event = get_object_or_404(Events, pk=event_id)
    current_time = datetime.utcnow()
    request.data['created_at'] = current_time.date()
    request.data['updated_at'] = current_time.date()
    request.data['event_id'] = event.id
    request.data['created_by'] = request.user.id
    comment = CommentSerializer(data=request.data)
    if comment.is_valid(raise_exception=True):
        comment.save()
        data = {
            "comment": request["comment"],
            "event_id": event_id,
        }
        return Response(data)
