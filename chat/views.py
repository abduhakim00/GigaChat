from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from .serializers import MemberSerializer
from .models import Member


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
        
    
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def homePage(request):
    return render(request, 'chat/index.html')