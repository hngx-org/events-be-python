from datetime import datetime
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError


from .models import Comment
from .serializers import CommentSerializer
from events.models import Events
from users.authentication import AuthenticationMiddleware, IsAuthenticatedUser


# Create your views here.
@api_view(["POST"])
# @authentication_classes(AuthenticationMiddleware)
#@permission_classes(IsAuthenticatedUser)
def create_comment(request, event_id, *args, **kwargs):
    try:
        event = Events.objects.get(pk=event_id)
    except (Events.DoesNotExist, ValidationError):
        return Response({"detail": "Event ID is incorrect"}, status=404)
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
