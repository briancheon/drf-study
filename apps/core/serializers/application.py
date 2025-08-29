from django.db import transaction
from rest_framework import serializers

from apps.core.models import Application, ApplicationField, Field, Recruitment
from apps.core.serializers.field import FieldSerializer
from apps.core.serializers.user import UserSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    fields = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Application
        fields = ["id", "recruitment", "content", "fields"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        fields_data = validated_data.pop("fields", [])
        applicant = self.context["request"].user
        recruitment_id = validated_data.get("recruitment").id

        if Application.objects.filter(applicant=applicant, recruitment_id=recruitment_id).exists():
            raise serializers.ValidationError("You have already applied for this recruitment.")

        with transaction.atomic():
            application = Application.objects.create(applicant=applicant, **validated_data)
            for field_id in fields_data:
                field = Field.objects.get(id=field_id)
                ApplicationField.objects.create(application=application, field=field)
        return application

    def update(self, instance, validated_data):
        fields_data = validated_data.pop("fields", None)

        with transaction.atomic():
            instance.content = validated_data.get("content", instance.content)
            instance.save()

            if fields_data is not None:
                instance.application_field_set.all().delete()
                for field_id in fields_data:
                    field = Field.objects.get(id=field_id)
                    ApplicationField.objects.create(application=instance, field=field)

        return instance


class ApplicationDetailSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)
    fields = FieldSerializer(many=True, read_only=True, source="application_field_set")

    class Meta:
        model = Application
        fields = [
            "id",
            "applicant",
            "recruitment",
            "content",
            "fields",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["fields"] = [field["name"] for field in representation["fields"]]
        return representation