from .models import Member
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, get_object_or_404
from .serializers import MemberSerializer
from rest_framework.permissions import IsAuthenticated


class MemberApiView(ListCreateAPIView, UpdateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_queryset(self):
        return Member.objects.filter(user=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except:
            return Response("This user has already set his/her profile", status=status.HTTP_403_FORBIDDEN)  
    
    def get_object(self):
        # if you want pass post_id and user_id in url:
        user =  get_object_or_404(Member, user=self.request.user) 
        user.avatar.delete()
        return user
        
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)