from rest_framework import routers

from .views import ChatroomViewSet, ChatroomUserViewSet

router = routers.DefaultRouter()
router.register(r'chatrooms', ChatroomViewSet)
router.register(r'users', ChatroomUserViewSet)

urlpatterns = router.urls