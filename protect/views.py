from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Правильная проверка - пользователь НЕ в группе authors
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        # Проверяем, что пользователь ЕЩЁ НЕ в группе authors
        if not request.user.groups.filter(name='authors').exists():
            # Получаем или создаем группу
            authors_group, created = Group.objects.get_or_create(name='authors')
            # Добавляем пользователя в группу
            authors_group.user_set.add(request.user)
            messages.success(request, 'Поздравляем! Теперь вы автор!')
        else:
            messages.info(request, 'Вы уже являетесь автором')
        return redirect('index')