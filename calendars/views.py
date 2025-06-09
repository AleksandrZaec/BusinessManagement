from calendar import monthrange
from datetime import datetime

from django.utils.dateparse import parse_date
from rest_framework.response import Response
from rest_framework.views import APIView

from meetings.models import Meeting
from meetings.serializers import MeetingSerializer
from tasks.models import Task
from tasks.serializers import TaskSerializer


class CalendarAPIView(APIView):
    """API view to display user's tasks and meetings in calendar format."""

    def get(self, request):
        user = request.user
        view_type = request.query_params.get("view", "day")

        if view_type == "day":
            date_str = request.query_params.get("date")
            if not date_str:
                return Response(
                    {"error": "Не указана дата для вывода календаря."}, status=400
                )

            date = parse_date(date_str)
            if not date:
                return Response(
                    {"error": "Неверный формат даты."}, status=400
                )

            meetings = Meeting.objects.filter(participants=user, date=date)
            tasks = Task.objects.filter(task_performer=user, deadline=date)

            return Response(
                {
                    "date": date_str,
                    "meetings": MeetingSerializer(meetings, many=True).data,
                    "tasks": TaskSerializer(tasks, many=True).data,
                }
            )

        elif view_type == "month":
            month_str = request.query_params.get("month")
            if not month_str:
                return Response(
                    {"error": "Не указан месяц для вывода календаря."}, status=400
                )

            try:
                year, month = map(int, month_str.split("-"))
                start_date = datetime(year, month, 1).date()
                end_date = datetime(year, month, monthrange(year, month)[1]).date()
            except (ValueError, IndexError):
                return Response({"error": "Неверный формат даты."}, status=400)

            meetings = Meeting.objects.filter(
                participants=user, date__range=(start_date, end_date)
            )
            tasks = Task.objects.filter(
                task_performer=user, deadline__range=(start_date, end_date)
            )

            calendar_data = {}
            for day in range(1, monthrange(year, month)[1] + 1):
                day_date = datetime(year, month, day).date()
                calendar_data[str(day_date)] = {
                    "meetings": MeetingSerializer(
                        meetings.filter(date=day_date), many=True
                    ).data,
                    "tasks": TaskSerializer(
                        tasks.filter(deadline=day_date), many=True
                    ).data,
                }

            return Response({"month": month_str, "calendar": calendar_data})

        return Response({"error": "Введены неверные параметры."}, status=400)
