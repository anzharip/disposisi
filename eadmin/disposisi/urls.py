from django.urls import path

from .views import MemoSimpleListView, MemoSimpleDetailView, MemoSimpleCreateView, MemoSimpleUpdateView, \
    memo_simple_update_state

app_name = 'disposisi'
urlpatterns = [
    path('memosimple/', MemoSimpleListView.as_view(), name='memo-simple-list'),
    path('memosimple/<int:pk>/', MemoSimpleDetailView.as_view(), name='memo-simple-detail'),
    path('memosimple/create', MemoSimpleCreateView.as_view(), name='memo-simple-create'),
    path('memosimple/<int:pk>/update', MemoSimpleUpdateView.as_view(), name='memo-simple-update'),
    path('memosimple/<int:pk>/updateState', memo_simple_update_state, name='memo-simple-update-state')
]
