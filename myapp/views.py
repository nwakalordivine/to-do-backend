from .serializers import TaskSerializer
from .models import Task
from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample

# Create your views here.

class CreateTask(generics.ListCreateAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer

class UpdateTaskStatus(generics.UpdateAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    lookup_field='pk'
    

class DestroyTask(generics.DestroyAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    lookup_field='pk'


class NumberOfTask(APIView):

    @extend_schema(
        summary="Get Task Statistics",
        description="Returns the total count of tasks and a breakdown by status (pending, started, completed).",
        responses={
            200: inline_serializer(
                name='TaskStatsResponse',
                fields={
                    'No_of_tasks': serializers.IntegerField(),
                    'pending_tasks': serializers.IntegerField(),
                    'started': serializers.IntegerField(),
                    'completed': serializers.IntegerField(),
                }
            )
        },
        examples=[
            OpenApiExample(
                'Valid Example',
                summary='Comprehensive task overview',
                description='Returns the filtered total for the tasks.',
                value={
                    "No_of_tasks": 6,
                    "pending_tasks": 3,
                    "started": 2,
                    "completed": 1
                },
                response_only=True
            )
        ]
    )

    def get(self, request):
        data = Task.objects.aggregate(
            total=Count("id"),
            pending_tasks=Count("id", filter=Q(status="pending")),
            started=Count("id", filter=Q(status="started")),
            completed=Count("id", filter=Q(status="done"))
        )
        return Response({
            "No_of_tasks": data["total"],
            "pending_tasks": data["pending_tasks"],
            "started": data["started"],
            "completed": data["completed"]
        }, status=status.HTTP_200_OK)
