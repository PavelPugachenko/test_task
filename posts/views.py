from rest_framework import viewsets

from .models import Comment, Post, User
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin, IsOwnerOrReadOnly
from .serializers import CommentSerializer, PostSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        elif self.action == "list":
            return [permissions.IsAdminUser()]
        elif self.action in ["update", "partial_update"]:
            return [IsOwnerOrAdmin()]
        elif self.action == "destroy":
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.action == "list":
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        elif self.action in ["update", "partial_update"]:
            return [IsOwnerOrAdmin()]
        elif self.action == "destroy":
            return [IsOwnerOrAdmin()]
        return []


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        elif self.action in ["update", "partial_update"]:
            return [IsOwnerOrAdmin()]
        elif self.action == "destroy":
            return [IsOwnerOrAdmin()]
        return []

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_pk"])
