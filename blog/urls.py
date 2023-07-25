from django.urls import path
from .views import *

urlpatterns = [
    path("", ListPostView.as_view(), name="home"),
    path("register-user/", RegisterUser.as_view(), name="register_user"),
    path("login-user/", LoginUser.as_view(), name="login_user"),
    path("update-user/<int:pk>/", UpdateUser.as_view(), name="update_user"),
    path("logout-user/", user_logout, name="logout_user"),
    path("delete-user/<int:pk>/", DeleteUser.as_view(), name="delete_user"),
    path("create-category/", CreateCategory.as_view(), name="create_category"),
    path("list-category/", ListCategory.as_view(), name="list_category"),
    path("update-category/<int:pk>/", UpdateCategory.as_view(), name="update_category"),
    path("delete-category/<int:pk>/", DeleteCategory.as_view(), name="delete_category"),
    path("create-post/", CreatePost.as_view(), name="create_post"),
    path("detail-post-view/<int:pk>/", DetailPostView.as_view(), name="detail_post_view"),
    path("update-post/<int:pk>/", UpdatePost.as_view(), name="update_post"),
    path("delte-post/<int:pk>/", DeletePost.as_view(), name="delete_post"),
    path("post-category/<int:pk>/", PostByCategory.as_view(), name="post_category"),
    path("search-post/", search_post, name="search_post"),
]
