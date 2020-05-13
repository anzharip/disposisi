from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import MemoSimple


# Create your views here.
class MemoSimpleListView(generic.ListView):
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
