from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, CommentViewSet
from tasks.apps import TasksConfig

app_name = TasksConfig.name

router = DefaultRouter()
router.register(r"", TaskViewSet, basename="task")
router.register(r"", CommentViewSet, basename="comment")

urlpatterns = router.urls
