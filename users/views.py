from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]