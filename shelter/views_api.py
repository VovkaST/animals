from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Animals
from .serializers import AnimalsViewSerializer, AnimalsEditSerializer


class APIAnimals(APIView):
    def get(self, request, *args, **kwargs):
        """ Просмотр всех записей """
        records = Animals.objects.all()
        serializer = AnimalsViewSerializer(records, many=True)
        return Response({'animals': serializer.data})

    def post(self, request, *args, **kwargs):
        """ Создание записи """
        if not request.user.is_authenticated:
            return Response({'error': 'Access denied!'}, status=401)
        records = request.data.get('animals')
        serializer = AnimalsEditSerializer(data=records)
        if serializer.is_valid(raise_exception=False):
            news_created = serializer.save()
            return Response({'success': 'Record with id={} was successfully created'.format(news_created)})
        else:
            return Response({'error': serializer.errors})

    def put(self, request, pk, *args, **kwargs):
        """ Изменение записи по id """
        if not request.user.is_authenticated:
            return Response({'error': 'Access denied!'}, status=401)
        record = get_object_or_404(Animals.objects.all(), pk=pk)
        data = request.data.get('animals')
        serializer = AnimalsEditSerializer(instance=record, data=data, partial=True)
        if serializer.is_valid():
            news_saved = serializer.save()
            return Response({'success': 'Record with id={} was successfully updated'.format(news_saved)})
        else:
            return Response({'error': serializer.errors})

    def delete(self, request, pk, *args, **kwargs):
        """ Удаление записи по id """
        if not request.user.is_authenticated:
            return Response({'error': 'Access denied!'}, status=401)
        record = get_object_or_404(Animals.objects.all(), pk=pk)
        record.delete()
        return Response({'success': 'Record with id={} was successfully deleted'.format(pk)})
