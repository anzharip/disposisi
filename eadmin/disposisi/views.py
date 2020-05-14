from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django_fsm import TransitionNotAllowed

from .serializers import MemoSimpleSerializer
from .models import MemoSimple


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


def memo_simple_update_state(request, pk):
    memo_simple = get_object_or_404(MemoSimple, pk=pk)


# TODO Pagination to limit results
class MemoSimpleListAPIView(generics.ListCreateAPIView):
    queryset = MemoSimple.objects.all()
    serializer_class = MemoSimpleSerializer


class MemoSimpleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MemoSimple.objects.all()
    serializer_class = MemoSimpleSerializer


# TODO Implement this endpoint dynamically
# TODO Implement the frontend, serve it from django, but it could be SPA
class MemoSimpleUpdateStateAPIView(APIView):

    def put(self, request, pk):
        memo_simple = get_object_or_404(MemoSimple, pk=pk)
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
