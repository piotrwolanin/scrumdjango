from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ObjectDoesNotExist, Max, Sum
from django.shortcuts import redirect
from django.utils.text import Truncator
from scrumboard.models import Sprint, Task
from scrumboard.forms import SprintForm, TaskForm
from datetime import datetime, timedelta
from extra_views import ModelFormSetView
from itertools import repeat


class SprintListView(LoginRequiredMixin, ListView):
    template_name = 'sprints.html'
    model = Sprint
    context_object_name = 'sprints'


class SprintDetailView(LoginRequiredMixin, DetailView):
    template_name = 'sprint-details.html'
    model = Sprint

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(sprint=self.kwargs['pk'])
        usernames = tasks.values_list('user__username', flat=True).distinct()
        task_assignment = [
            (username, tasks.filter(user__username=username)) for username in usernames
        ]
        points_assigned = tasks.aggregate(Sum('points'))['points__sum']
        points_achieved = tasks.filter(progress=2).aggregate(Sum('points'))[
            'points__sum'
        ]
        context['task_assignment'] = task_assignment
        context['points_assigned'] = points_assigned
        context['points_achieved'] = points_achieved
        return context


def sprint_detail_redirect_view(request):
    latest_sprint = get_latest_sprint()
    if latest_sprint is None:
        return redirect('scrumboard:all_sprints')
    return redirect(latest_sprint)


class CreateSprintView(LoginRequiredMixin, CreateView):
    template_name = 'sprint-crud.html'
    form_class = SprintForm

    def get_initial(self):
        init_vals = super().get_initial()
        latest_sprint = get_latest_sprint()
        init_vals['number'] = 1
        try:
            init_vals['number'] += latest_sprint.number
            date_from = latest_sprint.date_to + timedelta(days=1)
            date_to = date_from + timedelta(days=21)
            init_vals['date_from'] = date_from
            init_vals['date_to'] = date_to
        except AttributeError:
            pass
        return init_vals

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a new sprint'
        context['btn_title'] = 'Create'
        context['btn_class'] = 'success'
        return context


class UpdateSprintView(LoginRequiredMixin, UpdateView):
    template_name = 'sprint-crud.html'
    model = Sprint
    form_class = SprintForm
    success_url = reverse_lazy('scrumboard:all_sprints')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sprint_name = Truncator(self.get_object()).chars(35)
        context['title'] = f'Update {sprint_name}'
        context['btn_title'] = 'Update'
        context['btn_class'] = 'info'
        return context


class CopySprintView(LoginRequiredMixin, CreateView):
    template_name = 'sprint-crud.html'
    form_class = SprintForm

    def get_initial(self):
        init_vals = super().get_initial()
        latest_sprint = get_latest_sprint()
        init_vals['number'] = latest_sprint.number + 1
        date_from = latest_sprint.date_to + timedelta(days=1)
        date_to = date_from + timedelta(days=21)
        init_vals['date_from'] = date_from
        init_vals['date_to'] = date_to
        return init_vals

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        old_sprint = Sprint.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Copy sprint {old_sprint.number}?'
        context['btn_title'] = 'Copy'
        context['btn_class'] = 'info'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        new_sprint = self.object
        old_sprint = Sprint.objects.get(pk=self.kwargs['pk'])
        wip = old_sprint.task_set.all().exclude(progress=2)

        for task in wip:
            task.pk = None
            task.sprint_id = new_sprint.pk
            task.save()

        return response


class DeleteSprintView(LoginRequiredMixin, DeleteView):
    template_name = 'sprint-crud.html'
    model = Sprint
    form_class = SprintForm
    success_url = reverse_lazy('scrumboard:all_sprints')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sprint_name = Truncator(self.get_object()).chars(35)
        context['title'] = f'Delete {sprint_name}?'
        context['btn_title'] = 'Delete'
        context['btn_class'] = 'danger'
        return context


class CreateTaskView(LoginRequiredMixin, CreateView):
    template_name = 'task-crud.html'
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a new task'
        context['btn_title'] = 'Create'
        context['btn_class'] = 'success'
        return context

    def get_initial(self):
        init_vals = super().get_initial()
        init_vals['user'] = self.request.user
        return init_vals

    def form_valid(self, form):
        form.instance.sprint = Sprint.objects.get(pk=self.kwargs['sprint'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'scrumboard:sprint_details', kwargs={'pk': self.kwargs['sprint']}
        )


class CreateMultipleTasksView(LoginRequiredMixin, ModelFormSetView):
    template_name = 'scrumboard-formset.html'
    model = Task
    form_class = TaskForm
    factory_kwargs = {'extra': 1, 'min_num': 1, 'max_num': 10}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create multiple tasks'
        context['btn_title'] = 'Create'
        context['btn_class'] = 'success'
        context['sprint_id'] = self.kwargs['sprint']
        return context

    def get_queryset(self, *args, **kwargs):
        return Task.objects.none()

    def get_initial(self):
        init_vals = super().get_initial()
        form_count = self.factory_kwargs['extra'] + 1
        init_vals.extend(
            repeat(
                {'user': self.request.user, 'sprint': self.kwargs['sprint']}, form_count
            )
        )
        return init_vals

    def get_success_url(self):
        return reverse_lazy(
            'scrumboard:sprint_details', kwargs={'pk': self.kwargs['sprint']}
        )


def progress_task(request, sprint, pk):
    task = Task.objects.get(pk=pk)
    task.move_right()
    return redirect(Sprint.objects.get(pk=sprint))


def unprogress_task(request, sprint, pk):
    task = Task.objects.get(pk=pk)
    task.move_left()
    return redirect(Sprint.objects.get(pk=sprint))


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    template_name = 'task-crud.html'
    model = Task
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_name = Truncator(self.get_object()).chars(35)
        context['title'] = f'Update task "{task_name}"'
        context['btn_title'] = 'Update'
        context['btn_class'] = 'info'
        return context

    def get_success_url(self):
        return reverse_lazy(
            'scrumboard:sprint_details', kwargs={'pk': self.kwargs['sprint']}
        )


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    template_name = 'task-crud.html'
    model = Task
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_name = Truncator(self.get_object()).chars(35)
        context['title'] = f'Delete task "{task_name}"?'
        context['btn_title'] = 'Delete'
        context['btn_class'] = 'danger'
        return context

    def get_success_url(self):
        return reverse_lazy(
            'scrumboard:sprint_details', kwargs={'pk': self.kwargs['sprint']}
        )


def get_latest_sprint():
    latest_sprint_num = Sprint.objects.all().aggregate(Max('number'))['number__max']
    try:
        sprint = Sprint.objects.get(number=latest_sprint_num)
    except ObjectDoesNotExist:
        sprint = None
    return sprint
