from rest_framework import routers
from misaca_federation.controllers.activitypub.actor_viewset import ActorViewSet as APActorViewSet

router = routers.SimpleRouter(trailing_slash=False)
#router.register(r'users', UserViewSet)
#router.register(r'accounts', AccountViewSet)

router.register(r'users', APActorViewSet)
urlpatterns = router.urls
