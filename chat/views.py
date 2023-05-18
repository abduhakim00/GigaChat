from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import MemberSerializer, UserSerializer
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


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def Chat1on1(request, id):
    if User.objects.filter(id=id).exists():
        other_user = User.objects.filter(id=id).get()
        return render(request, 'chat/oneonone.html', {'user': request.user.username, 'other':id, 'other_name': other_user.username})
    else:
        return Response("No such user", status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def lookUp(request):
    user = request.GET.get('username')
    if user != '':
        q = User.objects.filter(username=user)
        if q.exists():
            serializer = UserSerializer(User.objects.filter(username=user).get())
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('No such user', status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response('search info not given!', status=status.HTTP_400_BAD_REQUEST)