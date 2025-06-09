from rest_framework.routers import DefaultRouter
from evaluations.apps import EvaluationsConfig
from evaluations.views import EvaluationViewSet

app_name = EvaluationsConfig.name

router = DefaultRouter()
router.register(r"", EvaluationViewSet, basename="evaluation")

urlpatterns = router.urls
