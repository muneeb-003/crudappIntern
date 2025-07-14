from django.shortcuts import get_object_or_404, redirect
from .models import Post , Comment

from django.views import generic , View
from django.urls import reverse


class PostListView(generic.ListView):
    model = Post
    template_name= "blog/index.html"
    context_object_name = "latestPosts"

class CreatePostView(generic.CreateView):
    model = Post
    template_name = "blog/form.html"
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  
    def get_success_url(self):
        return "/post/"

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class EditPostView(generic.UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/form.html'

    def get_success_url(self):
        # return '/post/<int:pk>/' 
        return reverse('blog:details', kwargs={'pk': self.object.pk})

class DeletePostView(generic.DeleteView):
    model = Post
    template_name = 'blog/confirm_delete.html'

    def get_success_url(self):
        return '/post/' 
    
class AddCommentView(generic.CreateView):
    def post(self,request,pk):
        post = get_object_or_404(Post,pk=pk)
        user = request.POST.get("user")
        commentText = request.POST.get("comment")

        if user and commentText:
            Comment.objects.create(post=post, user=user, comment=commentText)

        return redirect("blog:details", pk=pk)
    


class DeleteCommentView(View):

    # def post(self, pk):
    #     comment = get_object_or_404(Comment, pk=pk)
    #     post_id = comment.post.pk
    #     comment.delete()
    #     return redirect("blog:details", pk=post_id)

    def post(self, request, *args, **kwargs):
        comment_id = kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_id)
        post_id = comment.post.pk
        comment.delete()
        return redirect("blog:details", pk=post_id)