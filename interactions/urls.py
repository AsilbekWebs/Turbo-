from django.urls import path
from .views import LikeToggleView, MyLikesListView, CommentListCreateView

urlpatterns = [
    path('products/<int:id>/like/', LikeToggleView.as_view(), name='product-like'),
    path('products/<int:id>/comments/', CommentListCreateView.as_view(), name='product-comments'),
    path('likes/', MyLikesListView.as_view(), name='my-likes'),
]