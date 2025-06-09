from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from meetings.models import Meeting
from meetings.serializers import MeetingSerializer


class MeetingViewSet(ModelViewSet):
    """
    ViewSet for creating, retrieving, updating, deleting meetings
    and listing meetings of the current user.
    """
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=False, methods=['get'], url_path='my-meetings')
    def my_meetings(self, request):
        """List all meetings where the current user is a participant."""
        user_meetings = Meeting.objects.filter(participants=request.user)
        serializer = self.get_serializer(user_meetings, many=True)
        return Response(serializer.data)
