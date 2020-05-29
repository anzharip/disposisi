from django.urls import path

from .views import MemoSimpleListView, MemoSimpleDetailView, MemoSimpleCreateView, MemoSimpleUpdateView, \
    memo_simple_update_state, MemoSimpleUpdateStateAPIView, UserInfoView, GroupListAPIView, GroupDetailAPIView, \
    MemoSimpleListCreateAPIView, MemoSimpleRetrieveUpdateDestroyAPIView

app_name = 'disposisi'
urlpatterns = [
    path('memosimple/', MemoSimpleListView.as_view(), name='memo-simple-list'),
    path('memosimple/<int:pk>/', MemoSimpleDetailView.as_view(), name='memo-simple-detail'),
    path('memosimple/create', MemoSimpleCreateView.as_view(), name='memo-simple-create'),
    path('memosimple/<int:pk>/update', MemoSimpleUpdateView.as_view(), name='memo-simple-update'),
    path('memosimple/<int:pk>/updateState', memo_simple_update_state, name='memo-simple-update-state'),
    path('api/memosimple/', MemoSimpleListCreateAPIView.as_view(), name='memosimple-api-list-create'),
    path('api/memosimple/<int:pk>/', MemoSimpleRetrieveUpdateDestroyAPIView.as_view(),
         name="memosimple-api-retrieve-update-destroy"),
    path('api/memosimple/<int:pk>/updateState', MemoSimpleUpdateStateAPIView.as_view(),
         name="memosimple-api-update-state"),
    path('api/user/', UserInfoView.as_view()),
    path('api/group/', GroupListAPIView.as_view()),
    path('api/group/<int:pk>', GroupDetailAPIView.as_view()),

]
