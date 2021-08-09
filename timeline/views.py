from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Post, Like, Want, Notation
from django.http.response import JsonResponse
from functools import reduce
from operator import and_


class IndexView(generic.ListView):
    template_name = 'index.html'
    paginate_by = 10

    def get_queryset(self):
        posts = Post.objects.order_by('-created_at')
        return posts


class CreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    success_url = reverse_lazy('timeline:index')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        messages.success(self.request, '投稿が完了しました。')
        redirect_url = super(CreateView, self).form_valid(form)

        notation = Notation(user=self.request.user, post=self.object)
        notation.save()

        return redirect_url

    def form_invalid(self, form):
        messages.warning(self.request, '投稿が失敗しました。')
        return redirect('timeline:index')


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('timeline:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author == request.user:
            messages.success(self.request, '削除しました。')
            return super().delete(request, *args, **kwargs)

class TradedView(LoginRequiredMixin, generic.View):
    model = Post

    def get(self, request, pk):
        post = Post.objects.get(id=pk)

        if post.author == request.user:
            post.traded = True
            post.save()
            messages.success(self.request, '登録しました。')
            return redirect('timeline:index')


class LikeView(LoginRequiredMixin, generic.View):
    model = Like

    def post(self, request):
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)
        like = Like(user=self.request.user, post=post)
        like.save()

        Want.objects.create(wanting=self.request.user, wanted=post.author)

        like_count = Like.objects.filter(post=post).count()
        data = {'message': '欲しい！を伝えました。',
                'like_count': like_count}
        return JsonResponse(data)

def find(request):
    posts = Post.objects.order_by('-created_at')[:42]
    msg = '書籍検索'
    if (request.method == 'POST'):
        find = request.POST['find']
        if find:
            q_list = ''
            for c in find:
                if c in {' ', '　'}:
                    pass
                else:
                    q_list += c
            query = reduce(
                    and_, [Q(text__icontains=q) | Q(station__icontains=q) for q in q_list]
                )
            posts = Post.objects.order_by('-created_at').filter(query)
            msg = '検索結果: ' + str(posts.count()) + '件'

    params = {
        'message': msg,
        'posts': posts,
    }
    return render(request, 'find.html', params)


index = IndexView.as_view()
create = CreateView.as_view()
delete = DeleteView.as_view()
traded = TradedView.as_view()
like = LikeView.as_view()
