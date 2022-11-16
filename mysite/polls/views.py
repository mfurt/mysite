from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView

from .models import Question, Choice, Vote
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'polls/login.html'
    model = User
    success_url = '/'

    def get_redirect_url(self):
        if self.request.user.is_superuser:
            return '/admin'
        return self.success_url


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    login_required()


class CustomRegisterView(CreateView):
    model = User
    template_name = 'polls/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('polls:login')


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            close_date__gte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(close_date__gte=timezone.now())


class ProfileView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/profile.html'
    context_object_name = 'my_question_results'

    def get_queryset(self):
        return Vote.objects.filter(user_id=self.request.user.id)


class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    login_required()


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, 'Такой вариант ответа не найден')
        return render(request, 'polls/detail.html', {
            'question': question
        })
    else:
        try:
            Vote.objects.get(question_id=question_id, user_id=request.user.id)
        except Vote.DoesNotExist:
            Vote(
                question_id=question_id,
                choice_id=selected_choice.id,
                user_id=request.user.id
            ).save()
            messages.success(request, 'Вы успешно проголовали')
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

        messages.error(request, 'Вы уже проголосовали')
        return render(request, 'polls/detail.html', {
            'question': question
        })

