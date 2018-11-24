from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.text import Truncator
from backlog.models import Item
from backlog.forms import ItemForm
from scrumboard.models import Task


class BacklogListView(LoginRequiredMixin, ListView):
    template_name = 'backlog-items.html'
    model = Item
    context_object_name = 'backlog'


class ItemEditView(LoginRequiredMixin, object):
    template_name = 'backlog-form.html'
    form_class = ItemForm


class CreateItemView(ItemEditView, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add a new backlog item'
        context['btn_title'] = 'Create'
        context['btn_class'] = 'success'
        return context


class AssignItemView(LoginRequiredMixin, CreateView):
    template_name = 'backlog-form.html'
    model = Task
    fields = '__all__'

    def get_initial(self):
        init_vals = super().get_initial()
        item = Item.objects.get(pk=self.kwargs['pk'])
        init_vals['text'] = item.text
        init_vals['points'] = item.points
        return init_vals

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = Item.objects.get(pk=self.kwargs['pk'])
        item_name = item.text
        context['title'] = f'Assign item "{item_name}" to a sprint'
        context['btn_title'] = 'Assign'
        context['btn_class'] = 'orange'
        return context

    def form_valid(self, form):
        Item.objects.get(pk=self.kwargs['pk']).delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('backlog:items')


class UpdateItemView(ItemEditView, UpdateView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_name = Truncator(self.get_object()).chars(35)
        context['title'] = f'Update "{item_name}" backlog item'
        context['btn_title'] = 'Update'
        context['btn_class'] = 'info'
        return context


class DeleteItemView(ItemEditView, DeleteView):
    model = Item
    success_url = reverse_lazy('backlog:items')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_name = Truncator(self.get_object()).chars(35)
        context['title'] = f'Delete "{item_name}" from the backlog?'
        context['btn_title'] = 'Delete'
        context['btn_class'] = 'danger'
        return context
