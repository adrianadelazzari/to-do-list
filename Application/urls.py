from django.urls import path
from .views import ToDoListView, ToDoListItemDetailsView, ItemCreateView, ItemUpdateView, ItemDeleteView, \
    CustomLoginView, RegisterUser, TaskDoneView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('', TaskDoneView.as_view(), name='task_done'),
    path('to-do-list/', ToDoListView.as_view(), name='to-do-list'),
    path('item-details/<int:pk>', ToDoListItemDetailsView.as_view(), name='item-details'),
    path('item-create/', ItemCreateView.as_view(), name='item-create'),
    path('item-update/<int:pk>', ItemUpdateView.as_view(), name='item-update'),
    path('item-delete/<int:pk>', ItemDeleteView.as_view(), name='item-delete'),
]
