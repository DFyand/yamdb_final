from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TitleViewSet, CategoryViewSet, GenreViewSet, ReviewViewSet, CommentViewSet,
    UsersViewSet, RegistrationView, TokenView
)


app_name = 'api'

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('users', UsersViewSet)
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews\/(?P<review_id>\d+)\/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationView.as_view(),
         name='signup'),
    path('v1/auth/token/', TokenView.as_view(),
         name='token'),
]
