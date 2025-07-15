from django.shortcuts import get_object_or_404, redirect ,render
from .models import Post , Comment
from django.http import HttpResponse

from django.views import generic , View
from django.urls import reverse

from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    posts = Post.objects.all()
    # print(posts)
    context = {"latestPosts": posts}
    return render(request,"blog/index.html",context)



# class PostListView(generic.ListView):
#     model = Post
#     template_name= "blog/index.html"
#     context_object_name = "latestPosts"

#     # def get_queryset(self):
#     #     posts = Post.objects.all()
#     #     print("All posts:", posts)
#     #     return posts

    

class CreatePostView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "blog/form.html"
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("blog:index")


# def PostDetailView(request,pk):
#     # pass
#     post = get_object_or_404(Post,pk=pk)
#     return render(post,"blog/post_detail.html",{"post":post})

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class EditPostView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/form.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return HttpResponse("Unauthorized", status=401)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # return '/post/<int:pk>/' 
        return reverse('blog:details', kwargs={'pk': self.object.pk})

class DeletePostView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return HttpResponse("Unauthorized", status=401)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:index")
    
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
    
class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('blog:index')
        return render(request, 'registration/signup.html', {'form': form})