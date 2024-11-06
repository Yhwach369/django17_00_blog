from django.urls import path

from . import views

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/blog/

urlpatterns = [
    path('', views.home_page, name='home'),
    path('contacts/', views.contacts_page, name='contacts'),
    path('categories/<int:pk>/', views.category_posts, name='category_posts'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.create_post_view, name='create'),
    path('posts/<int:post_id>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:post_id>/edit/', views.UpdatePostView.as_view(), name='post_edit'),
    path('search/', views.search, name='search'),
    path('vote/<int:post_id>/<str:action>/', views.add_vote, name='add_vote'),
]

# {% url 'post_detail' post.pk %}
# Post, method
# get_absolute_url -> отдает полную ссылку до страницы
