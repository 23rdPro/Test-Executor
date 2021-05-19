from random import choice
import factory

from executor.models import File


class FileFactory(factory.django.DjangoModelFactory):
    file = factory.LazyAttribute(lambda x: choice(File.PATHS)[0])

    class Meta:
        model = File
        django_get_or_create = ('file', )
