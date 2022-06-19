from rest_framework import routers
from .views import CityViewSet, ProgramLanguageViewSet, VacancyViewSet

router = routers.DefaultRouter()
router.register('cities', CityViewSet)
router.register('pl', ProgramLanguageViewSet)
router.register('vacancy', VacancyViewSet)

urlpatterns = router.urls