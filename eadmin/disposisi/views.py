from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django_fsm import TransitionNotAllowed

from .serializers import MemoSimpleSerializer, UserSerializer
from .models import MemoSimple


def _is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


def _has_group_permission(user, required_groups):
    return any([_is_in_group(user, group_name) for group_name in required_groups])


class IsGroupOperasional(permissions.BasePermission):
    """
    """

    required_groups = ['operasional']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission


# Create your views here.
class MemoSimpleListView(LoginRequiredMixin, generic.ListView):
    model = MemoSimple


class MemoSimpleDetailView(generic.DetailView):
    model = MemoSimple


class MemoSimpleCreateView(generic.CreateView):
    model = MemoSimple
    fields = ['subject', 'information', 'sender']


class MemoSimpleUpdateView(generic.UpdateView):
    model = MemoSimple
    fields = ['subject', 'information', 'sender']
    template_name_suffix = '_update_form'


class UserInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = self.request.user.id
        user_info = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user_info)
        return Response(serializer.data)


def memo_simple_update_state(request, pk):
    memo_simple = get_object_or_404(MemoSimple, pk=pk)


# TODO Pagination to limit results
class MemoSimpleListAPIView(generics.ListCreateAPIView):
    queryset = MemoSimple.objects.all()
    serializer_class = MemoSimpleSerializer


class MemoSimpleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = MemoSimple.objects.all()
    serializer_class = MemoSimpleSerializer


# TODO Implement this endpoint dynamically
# TODO Implement the frontend, serve it from django, but it could be SPA
class MemoSimpleUpdateStateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupOperasional,)

    def put(self, request, pk):
        memo_simple = get_object_or_404(MemoSimple, pk=pk)
        try:
            if request.data['transition'] == '0':
                try:
                    memo_simple.status_perekaman_surat_to_status_distribusi_kabag()
                except TransitionNotAllowed as e:
                    return Response({'message': 'Transition is not allowed'}, status=status.HTTP_400_BAD_REQUEST)
                memo_simple.save()
                serializer = MemoSimpleSerializer(memo_simple)
                return Response(serializer.data)
            if request.data['transition'] == '1':
                try:
                    memo_simple.status_distribusi_kabag_to_status_disposisi_kasubag()
                except TransitionNotAllowed as e:
                    return Response({'message': 'Transition is not allowed'}, status=status.HTTP_400_BAD_REQUEST)
                memo_simple.save()
                serializer = MemoSimpleSerializer(memo_simple)
                return Response(serializer.data)
            if request.data['transition'] == '2':
                try:
                    memo_simple.status_disposisi_kasubag_to_status_disposisi_pelaksana()
                except TransitionNotAllowed as e:
                    return Response({'message': 'Transition is not allowed'}, status=status.HTTP_400_BAD_REQUEST)
                memo_simple.save()
                serializer = MemoSimpleSerializer(memo_simple)
                return Response(serializer.data)
            else:
                return Response({'message': 'transition is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'message': 'transition is required'}, status=status.HTTP_400_BAD_REQUEST)
