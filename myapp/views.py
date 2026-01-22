from .serializers import TaskSerializer
from .models import Task
from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample, extend_schema_view

# Create your views here.

class CreateTask(generics.ListCreateAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer


@extend_schema_view(

    put=extend_schema(
        summary="Update Task",
        description="fully update the task. status choices - **'pending', 'started', 'done'**"
    ),

    patch=extend_schema(
        summary="Update a specific Task field or all fields by Id",
        description="status choices - **'pending', 'started', 'done'**"
    ),
)

class UpdateTaskStatus(generics.UpdateAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    lookup_field='pk'
    

@extend_schema_view(
    delete=extend_schema(
        summary="Delete Task by Id",
        description="This action is irreversible.",
        responses={
            200: inline_serializer(
                name='TaskDelResponse',
                fields={"message": serializers.CharField()}
            )
        },
        examples=[
            OpenApiExample(
                'Valid Example',
                summary='Delete task',
                description='Deletes an existing task specified by id.',
                value={"message": "Task successfully deleted."},
                response_only=True
            )
        ]
    ),
)
class DestroyTask(generics.DestroyAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    lookup_field='pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response(
            {"message": "Task successfully deleted."},
            status=status.HTTP_200_OK
        )

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
