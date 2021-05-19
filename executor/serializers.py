from rest_framework import serializers

from users.models import User
from .models import Executor, File


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['url', 'file', ]


class ExecutorSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        super(ExecutorSerializer, self).__init__(*args, **kwargs)
        self.fields['tester'].queryset = User.objects.filter(id=user.pk)

    class Meta:
        model = Executor
        fields = ['url', 'tester', 'environment_id', 'file', 'test_log', 'test_status']

    def to_representation(self,  instance):  # to get actual value on an m2m field instead of url in this case
        rep = super().to_representation(instance)
        request = self.context['request']
        rep['file'] = FileSerializer(instance.file.all(), many=True, context={'request': request}).data
        return rep


# a way to serialize Executor for json operation
class TaskSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField(source='get_file')
    tester = serializers.SerializerMethodField(source='get_tester')
    created_at = serializers.SerializerMethodField(source='get_created_at')

    class Meta:
        model = Executor
        fields = ['id', 'tester', 'environment_id', 'created_at', 'file', 'test_log', 'test_status']

    @staticmethod
    def get_file(obj):
        return Executor.objects.last().__str__()

    @staticmethod
    def get_tester(obj):
        return obj.tester.username

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%Y-%m-%d %I:%M:%S%z")
