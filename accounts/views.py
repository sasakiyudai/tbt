from .models import CustomUser, Comment 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import ProfileForm
from django.contrib.messages.views import SuccessMessageMixin
from timeline.models import Post, Notation
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http.response import JsonResponse

class ProfileEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'account/edit.html'
    success_url = '/accounts/edit/'
    success_message = 'プロフィールを更新しました。'

    def get_object(self):
        return self.request.user

class ProfileDetail(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    template_name = 'account/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Post.objects.order_by('-created_at')
        return context

class PostDetail(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'account/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Comment.objects.order_by('-created_at')
        return context

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        Comment.objects.create(text=request.POST["text"], post=post, user=request.user)

        subject = f'{request.user.username}さんから新着メッセージ：{post.text}@{post.station}'
        massege = f'{post.author.username}さんの投稿\n========================\n'\
                  f'{post.text}\n@{post.station}\n========================\n'\
                  f'に、{request.user.username}さんからメッセージが追加されました。\n\n{request.POST["text"]}\n\n'\
                  f'https://{settings.ALLOWED_HOSTS[0]}/accounts/posts/{pk}\n'
        from_mail = []
        notations = Notation.objects.filter(post=post)
        recipient = [notation.user.email for notation in notations if notation.user != request.user]
        send_mail(subject, massege, from_mail, recipient)

        return redirect('accounts:post_detail', pk)

class ProfileDetailWanted(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    template_name = 'account/wanted.html'

class ProfileDetailWanting(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    template_name = 'account/wanting.html'

class NotationView(LoginRequiredMixin, generic.View):
    model = Notation

    def post(self, request):
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)

        try:
            notation = Notation(user=self.request.user,post=post)
            notation.save()

            data = {'message': '通知をONにしました。\nこの投稿に新着メッセージがくると、メールに通知がきます。'}
            return JsonResponse(data)
        except:
            notation = Notation.objects.get(user=self.request.user, post=post)
            notation.delete()

            data = {'message': '通知をOFFにしました。'}
            return JsonResponse(data)

edit = ProfileEdit.as_view()
detail = ProfileDetail.as_view()
wanted = ProfileDetailWanted.as_view()
wanting = ProfileDetailWanting.as_view()
post_detail = PostDetail.as_view()
notation = NotationView.as_view()
