from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, CommentViewSet
from tasks.apps import TasksConfig

app_name = TasksConfig.name

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = router.urls
