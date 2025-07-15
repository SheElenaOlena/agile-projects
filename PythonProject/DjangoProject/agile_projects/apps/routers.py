from django.urls import path, include

from apps.tasks.views.tag_views import TagListAPIView

urlpatterns = [
            path('tasks/', include('apps.tasks.urls'))
              ]
