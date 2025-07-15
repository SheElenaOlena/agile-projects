from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import QuerySet


from apps.tasks.models import Tag
# from apps.tasks.serializers import TagSerializer
from apps.tasks.serializers.tag_serializers import TagSerializer


class TagListAPIView(APIView):
    """ получения всех объектов Tag """

    def get_object(self) -> QuerySet:
        return Tag.objects.all()

    def get(self, request: Request) -> Response:
        """получения списка всех тегов методом get"""
        tags = self.get_object()

        if not tags.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT,  # ✅ корректный статус
            )
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Создание нового тега методом POST"""
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)