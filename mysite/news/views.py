from django.shortcuts import render
from .models import News,Category
from django.shortcuts import get_object_or_404, redirect
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', ({'form': form}))


def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'],
                             form.cleaned_data['content'],
                             'poltergeystgogy1@yandex.ru',
                             ['gudovgeorgiy@gmail.com'],
                             fail_silently=False
                             )
            if mail:
                messages.success(request, 'Вы успешно отправили письмо!')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки письма!')
        else:
            messages.error(request, 'Ошибка в заполнении каптчи')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})



class HomeNews(MyMixin, ListView):
    model = News # тоже самое news = News.objects.all()
    template_name = 'news/home_news_list.html'
    context_object_name = 'news' # чтобы в темплейте можно было обращаться {% for item in news %} именно к news
    mixin_prop = 'hello world'
    # extra_context = {'title': 'Главная страница'}
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper("Главная страница")
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        # для уточнения запроса
        return News.objects.filter(is_published=True).select_related('category') # select_related('category') только для foreign key, manyTomany prefrached


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        allow_empty = False #запрет показа пустых списков
        return context

    def get_queryset(self):
        # для уточнения запроса
        return News.objects.filter(category_id = self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    # pk_url_kwarg = 'news_id'
    # template_name = 'news/news_detail.html'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home') изменение редиректа после создания
    login_url = '/admin/'



# def index(request):
#     news = News.objects.all()
#     context = {'news': news,
#                'title': "Список новостей",
#                }
#     return render(request, template_name="news/index.html", context=context)

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, "news/category.html", {'news': news, "category": category, })

# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # news = News.objects.create(**form.cleaned_data) #за счет ** питон сам присвоит соответствующий ключам значения
#             news = form.save() # если связанная с данными форма bounded form
#             return redirect(news) # на созданную новость, на домашнюю страницу - return redirect('Home')
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
