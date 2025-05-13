from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, UploadFileView
from .views import MeView
from .views import MyFilesView
from .views import FilePreviewView
from .views import FileRawView
from .views import FileDownloadView, FileDeleteView
from .views import ProfileView
from .views import file_extensions_view

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", RegisterView.as_view(), name="register"),
    path("upload/", UploadFileView.as_view(), name="upload_file"),
    path("me/", MeView.as_view(), name="me"),
    path("my-files/", MyFilesView.as_view(), name="my_files"),
    path("file/<int:pk>/preview/", FilePreviewView.as_view(), name="file_preview"),
    path("file/<int:pk>/raw/", FileRawView.as_view(), name="file_raw"),
    path("file/<int:pk>/download/", FileDownloadView.as_view(), name="file_download"),
    path("file/<int:pk>/", FileDeleteView.as_view(), name="file_delete"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("my-file-extensions/", file_extensions_view, name="file_extensions"),
]

