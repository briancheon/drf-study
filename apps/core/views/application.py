from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.models import Application
from apps.core.serializers.application import ApplicationSerializer, ApplicationDetailSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["retrieve", "recruitments"]:
            return ApplicationDetailSerializer
        return ApplicationSerializer

    def get_queryset(self):
        queryset = super().get_queryset().select_related("applicant").prefetch_related("application_field_set__field")
        return queryset

    @action(detail=False, methods=["get"], url_path="recruitments/(?P<recruitment_id>[^/.]+)")
    def recruitments(self, request, recruitment_id=None):
        """
        모집글에 대한 신청글 조회
        """
        applications = self.get_queryset().filter(recruitment_id=recruitment_id)
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)
