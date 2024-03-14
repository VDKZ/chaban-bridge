# Django
from rest_framework import serializers

# Application
from jobs.enums import ExecutionStatus, JobFrequency, JobType

# Local
from .models import Execution, Job


class ExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Execution
        fields = ["id", "status", "result", "created_at", "updated_at"]

    def validate(self, validated_data: dict) -> dict:
        status = validated_data["status"]
        if status not in ExecutionStatus.values:
            raise serializers.ValidationError("Execution status is not valid")
        return validated_data


class JobSerializer(serializers.ModelSerializer):
    executions = ExecutionSerializer(required=False, many=True)

    class Meta:
        model = Job
        fields = ["id", "name", "type", "frequency", "executions"]

    def validate(self, validated_data: dict) -> dict:
        type = validated_data["type"]
        frequency = validated_data["frequency"]
        if type not in JobType.values:
            raise serializers.ValidationError("Job type is not valid")
        if frequency not in JobFrequency.values:
            raise serializers.ValidationError("Job frequency is not valid")
        return validated_data
