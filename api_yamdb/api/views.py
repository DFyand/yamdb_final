from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from reviews.models import Title, Genre, Category, Review, CustomUser
from .filters import TitleFilter
from .serializers import (
    TitleSerializer, TitleListSerializer, CategorySerializer, GenreSerializer,
    ReviewSerializer, Commentserializer, CustomUserSerializer, RegistrationSer,
    UserUpdateSerializer, TokenSerializer
)
from rest_framework import viewsets, filters, mixins

from .utils import send_msg
from random import randint
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import (
    TitlesCategoriesGenresPermission, ReviewsAndCommentsPermission,
    IsAdminPermission
)


class DestroyListCreateViewSet(
    mixins.DestroyModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = [TitlesCategoriesGenresPermission]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = Title.objects.all().annotate(rating=Avg('reviews__score'))
        return qs.order_by('-id')


class CategoryViewSet(DestroyListCreateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [TitlesCategoriesGenresPermission]


class GenreViewSet(DestroyListCreateViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [TitlesCategoriesGenresPermission]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewsAndCommentsPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = Commentserializer
    permission_classes = [ReviewsAndCommentsPermission]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class RegistrationView(APIView):
    serializer_class = RegistrationSer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(username=username, email=email)
            send_msg(user.email, user.username, user.confirmation_code)
            return Response(request.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['confirmation_code'] = randint(0, 9999)
            serializer.save()
            send_msg(serializer.validated_data.get("email"),
                     serializer.validated_data.get("username"),
                     serializer.validated_data.get("confirmation_code"),
                     )
            return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = CustomUser.objects.filter(username=data['username']).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = CustomUser.objects.filter(
            username=data['username'],
            confirmation_code=data['confirmation_code']).first()
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = [IsAdminPermission, ]
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAuthenticated, ),
    )
    def show_self_user(self, request):
        if request.method == 'GET':
            serializer = CustomUserSerializer(request.user)
            return Response(data=serializer.data, status=200)
        if request.method == 'PATCH':
            serializer = UserUpdateSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data="Unexpected Parameters", status=400)
