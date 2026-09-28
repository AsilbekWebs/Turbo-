from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from catalog.models import Product
from .models import Like, Comment
from .serializer import LikeSerializer, CommentSerializer


class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        product = generics.get_object_or_404(Product, id=id)
        like, created = Like.objects.get_or_create(user=request.user, product=product)
        if not created:
            like.delete()
        return Response(
            {'liked': created, 'likes_count': product.likes.count()},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class MyLikesListView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Like.objects.none()
        return Like.objects.filter(user=self.request.user).select_related('product')


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none()
        return Comment.objects.filter(product_id=self.kwargs['id']).select_related('user')

    def perform_create(self, serializer):
        product = generics.get_object_or_404(Product, id=self.kwargs['id'])
        serializer.save(user=self.request.user, product=product)