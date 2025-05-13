from .serializers import RegisterSerializer
from django.shortcuts import get_object_or_404
import base64
import logging

logger = logging.getLogger(__name__)
from django.http import HttpResponse
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UploadedFileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import UploadedFile
from .serializers import UploadedFileListSerializer


MAX_FILES_PER_USER = 25
MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username
        })

class UploadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if UploadedFile.objects.filter(user=user).count() >= MAX_FILES_PER_USER:
            logger.debug(" File count limit exceeded")
            return Response(
                {"detail": f"Maximum number of files reached ({MAX_FILES_PER_USER})."},
                status=status.HTTP_400_BAD_REQUEST
            )

        upload = request.FILES.get("file")
        if not upload:
            logger.debug(" No file uploaded")
            return Response({"detail": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f" Uploaded file size = {upload.size} bytes (limit = {MAX_FILE_SIZE_BYTES} bytes)")

        if upload.size > MAX_FILE_SIZE_BYTES:
            logger.debug(" FILE SIZE TOO BIG — rejecting")
            return Response(
                {"detail": f"File too large (max {MAX_FILE_SIZE_MB} MB)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # даже если мы ничего не передаём — всё равно вызовем сериализатор
        serializer = UploadedFileSerializer(data={"file": upload}, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            logger.debug(" File saved successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug(" Serializer error", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyFilesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadedFileListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = UploadedFile.objects.filter(user=user)

        # 🔍 Фильтрация по поисковому запросу
        search_query = self.request.query_params.get("search")
        if search_query:
            queryset = queryset.filter(filename__icontains=search_query)

        # 🧩 Фильтрация по расширению (например, ?ext=pdf)
        ext = self.request.query_params.get("ext")
        if ext:
            queryset = queryset.filter(filename__iendswith=f".{ext.lower()}")

        return queryset.order_by("-uploaded_at")

class FilePreviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        file = get_object_or_404(UploadedFile, pk=pk, user=request.user)

        # Только для текстовых файлов
        if file.content_type not in ["text/plain", "text/x-python"]:
            return Response({"error": "Preview not supported for this file type."}, status=400)

        try:
            content_str = file.content.decode("utf-8")
        except UnicodeDecodeError:
            content_str = "[Unable to decode file content]"

        return Response({
            "filename": file.filename,
            "content": content_str
        })

class FileRawView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        file = get_object_or_404(UploadedFile, pk=pk, user=request.user)

        # Преобразуем бинарные данные в base64
        encoded = base64.b64encode(file.content).decode("utf-8")

        return Response({
            "filename": file.filename,
            "content_type": file.content_type,
            "base64": encoded
        })

class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        file = get_object_or_404(UploadedFile, pk=pk, user=request.user)
        response = HttpResponse(file.content, content_type=file.content_type)
        response['Content-Disposition'] = f'attachment; filename="{file.filename}"'
        return response

class FileDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        file = get_object_or_404(UploadedFile, pk=pk, user=request.user)
        file.delete()
        return Response({"message": "File deleted"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def file_extensions_view(request):
    extensions = (
        UploadedFile.objects
        .filter(user=request.user)
        .values_list("filename", flat=True)
    )

    ext_set = set()
    for name in extensions:
        if "." in name:
            ext = name.rsplit(".", 1)[-1].lower()
            ext_set.add(ext)

    return Response(sorted(ext_set))