# from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView
# from .views import AuthenticationViewSet, PICViewSet, UserViewSet

# urlpatterns = [
#     path("auth/login", AuthenticationViewSet.as_view({"post": "login"}), name="login"),
#     path(
#         "auth/logout", AuthenticationViewSet.as_view({"post": "logout"}, name="logout")
#     ),
#     path(
#         "auth/users",
#         AuthenticationViewSet.as_view({"get": "user_info"}),
#         name="user-info",
#     ),
#     path("auth/role", AuthenticationViewSet.as_view({"get": "get_role"}), name="role"),
#     path(
#         "auth/token/verify/",
#         AuthenticationViewSet.as_view({"post": "verify_token"}),
#         name="token_verify",
#     ),
#     path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
#     path(
#         "users/<int:pk>",
#         UserViewSet.as_view({"delete": "destroy"}),
#         name="user-detail",
#     ),
#     path(
#         "users/penanggung-jawab",
#         PICViewSet.as_view({"get": "pic_list", "post": "create"}),
#         name="pic-list",
#     ),
#     path(
#         "users/penanggung-jawab/<int:pk>",
#         PICViewSet.as_view({"put": "update"}),
#         name="pic-detail",
#     ),
#     path(
#         "users/penanggung-jawab/stats",
#         PICViewSet.as_view({"get": "pic_stats"}, name="pic-stats"),
#     ),
#     path(
#         "users/penanggung-jawab/instansi",
#         PICViewSet.as_view({"get": "get_pic_institution"}),
#         name="pic-institution",
#     ),
# ]
