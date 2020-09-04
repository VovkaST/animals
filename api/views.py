from rest_framework.response import Response
from rest_framework.views import APIView

from shelter.models import Animals
from .serializers import AnimalsViewSerializer, AnimalsEditSerializer


class APIAnimals(APIView):

    def json_response(self, message, success=True, status=None):
        """
        Формирование ответа в формате JSON

        :param str message: Сообщение о результате обработки запроса
        :param bool success: Булевое значение успешности запроса
        :param int status: Код состояния HTTP
        :return: Объект Response
        """
        response = {
            'success': success,
            'message': message,
        }
        return Response(response, status=status)

    def get(self, request, *args, **kwargs):
        """ Просмотр всех записей """
        records = Animals.objects.filter(is_deleted=False)
        serializer = AnimalsViewSerializer(records, many=True)
        return Response({'animals': serializer.data})

    def post(self, request, *args, **kwargs):
        """ Создание записи """
        if not request.user.is_authenticated:
            return self.json_response(message='Access denied!', success=False, status=401)
        records = request.data.get('animals')
        serializer = AnimalsEditSerializer(data=records)
        if serializer.is_valid(raise_exception=False):
            created = serializer.save()
            return self.json_response(message='Record with id={} was successfully created'.format(created.id))
        else:
            return self.json_response(message=serializer.errors, success=False)

    def put(self, request, pk, *args, **kwargs):
        """ Изменение записи по id """
        if not request.user.is_authenticated:
            return self.json_response(message='Access denied!', success=False, status=401)
        try:
            record = Animals.objects.get(id=pk, is_deleted=False)
            data = request.data.get('animals')
            serializer = AnimalsEditSerializer(instance=record, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.json_response(message='Record with id={} was successfully updated'.format(pk))
            else:
                return self.json_response(message=serializer.errors, success=False)
        except Animals.DoesNotExist:
            return self.json_response(message='Record with id={} does not exist'.format(pk), success=False)

    def delete(self, request, pk, *args, **kwargs):
        """ Удаление записи по id """
        if not request.user.is_authenticated:
            return self.json_response(message='Access denied!', success=False, status=401)
        elif request.user.username.lower() != 'admin':
            return self.json_response(message='Permission denied!', success=False, status=403)
        try:
            animal = Animals.objects.get(id=pk, is_deleted=False)
            animal.soft_delete()
            return self.json_response(message='Record with id={} was successfully deleted'.format(pk))
        except Animals.DoesNotExist:
            return self.json_response(message='Record with id={} does not exist'.format(pk), success=False)
