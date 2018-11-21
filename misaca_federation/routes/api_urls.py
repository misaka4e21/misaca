from rest_framework import routers
from misaca_federation.controllers.twitter_api.status_viewset import StatusViewSet
from misaca_federation.controllers.twitter_api.account_viewset import AccountViewSet

router = routers.SimpleRouter()
#router.register(r'users', UserViewSet)
#router.register(r'accounts', AccountViewSet)

router.register(r'accounts', AccountViewSet)
router.register(r'statuses', StatusViewSet)
urlpatterns = router.urls
