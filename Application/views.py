from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from Application.models import ToDoListItem


class TaskDoneView(TemplateView):
    template_name = 'Application/task_done.html'


class RegisterUser(FormView):
    template_name = 'Application/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterUser, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('to-do-list')
        return super(RegisterUser, self).get(*args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'Application/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('to-do-list')


class ToDoListView(LoginRequiredMixin, ListView):
    model = ToDoListItem
    context_object_name = 'todo_list'
    template_name = 'Application/todo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_list'] = context['todo_list'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['todo_list'] = context['todo_list'].filter(title__startswith=search_input)

        else:
            print("No items found.")

        context['search_input'] = search_input

        return context


class ToDoListItemDetailsView(LoginRequiredMixin, DetailView):
    model = ToDoListItem
    context_object_name = 'item_details'
    template_name = 'Application/item_details.html'


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = ToDoListItem
    context_object_name = 'todo_list'
    template_name = 'Application/item_details_form.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('to-do-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ItemCreateView, self).form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDoListItem
    context_object_name = 'todo_list'
    template_name = 'Application/item_details_form.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('to-do-list')


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoListItem
    context_object_name = 'todo_list'
    template_name = 'Application/item_confirm_delete.html'
    success_url = reverse_lazy('to-do-list')



