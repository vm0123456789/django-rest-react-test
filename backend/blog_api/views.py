from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import viewsets
from rest_framework.response import Response


class PostUserWritePermission(BasePermission):
    # only author of the post can edit it
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            # SAFE_METHODS - GET, OPTIONS, HEAD
            return True
        return obj.author == request.user

# ================================== ModelViewSet ====================================


class PostList(viewsets.ModelViewSet):
    permission_classes = [PostUserWritePermission]
    serializer_class = PostSerializer
    queryset = Post.postobjects.all()

    def get_object(self, queryset=None, **kwargs):
        # use slug to define individual item instead of id
        item = self.kwargs.get('pk')
        return generics.get_object_or_404(Post, slug=item)

    # Define Custom Queryset
    def get_queryset(self):
        return Post.objects.all()

# ================================== ViewSet =====================================


# class PostList(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Post.postobjects.all()

#     def list(self, request):
#         serializer_class = PostSerializer(self.queryset, many=True)
#         return Response(serializer_class.data)

#     def retrieve(self, request, pk=None):
#         post = generics.get_object_or_404(self.queryset, pk=pk)
#         serializer_class = PostSerializer(post)
#         return Response(serializer_class.data)

#     # def list(self, request):
#     #     pass

#     # def create(self, request):
#     #     pass

#     # def retrieve(self, request, pk=None):
#     #     pass

#     # def update(self, request, pk=None):
#     #     pass

#     # def partial_update(self, request, pk=None):
#     #     pass

#     # def destroy(self, request, pk=None):
#     #     pass

# ================================== APIViews =====================================

# class PostList(generics.ListCreateAPIView):
#     # permission_classes = [IsAdminUser]
#     # permission classes = [DjangoModelPermissions]
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = Post.postobjects.all()
#     # postobjects - flagged as 'published'
#     serializer_class = PostSerializer

# class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
#     permission_classes = [PostUserWritePermission]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


""" Concrete View Classes
# CreateAPIView
Used for create-only endpoints.
# ListAPIView
Used for read-only endpoints to represent a collection of model instances.
# RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
# DestroyAPIView
Used for delete-only endpoints for a single model instance.
# UpdateAPIView
Used for update-only endpoints for a single model instance.
# ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
# RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
# RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""
