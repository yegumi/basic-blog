from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment , Vote , User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm,CommentCreateForm , CommentReplyForm,PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    def get(self, request):
        return render(request, 'home/index.html')

# Search View for handling search queries
from django.views import View
from django.db.models import Q
from django.shortcuts import render
from .models import Post
from .forms import PostSearchForm


class SearchView(View):
    def get(self, request):
        form = PostSearchForm(request.GET)
        posts = Post.objects.none()  # Start with an empty queryset
        query = request.GET.get('q')

        if query:  # Only filter if query is not empty
            posts = Post.objects.filter(
                Q(body__icontains=query) | Q(user__username__icontains=query))

        return render(request, 'accounts/results.html', {'posts': posts, 'form': form})


class PostCommentView(View):
    form_class =CommentCreateForm
    reply_class=CommentReplyForm
    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(id=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        can_like=False
        form=self.form_class()
        rep=self.reply_class()
        comments=self.post_instance.pcomments.filter(is_reply=False)
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like=True


        return render(request, 'home/detail.html', {'post': self.post_instance, 'form': form, 'comments': comments, 'rep':rep, 'can_like':can_like})
    @method_decorator(login_required())
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        rep=self.form_class(request.POST)
        if form.is_valid():
            new_form=form.save(commit=False)
            new_form.user=request.user
            new_form.post=self.post_instance
            new_form.save()
            messages.success(request,'your comment is uploaded','success')

        return redirect('home:detail',self.post_instance.id,self.post_instance.slug)


class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id ==request.user.id:
            post.delete()
            messages.success(request,'you deleted this post successfully','success')
        else:
            messages.error(request,'you cant delete this post','danger')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin,View):
    def setup(self,request, *args, **kwargs):
        self.post_instance=Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)
    def dispatch(self, request, *args, **kwargs):
        post=self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request,'you cant update this post','danger')
            return redirect("home:home")
        return super().dispatch(request,*args,**kwargs)
    def get(self,request,*args, **kwargs):
        post=self.post_instance
        form= PostCreateUpdateForm(instance=post)
        return render(request,'home/update.html',{'form':form})

    def post(self,request,*args, **kwargs):
        post = self.post_instance
        form =PostCreateUpdateForm(request.POST,instance=post)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug=slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request,'you updated this post successfully','success')
            return redirect("home:detail",post.id,post.slug)

class PostCreateView(LoginRequiredMixin,View):
    form_class=PostCreateUpdateForm
    def get(self,request,*args,**kwargs):
        form=self.form_class()
        return render(request,'home/createpost.html',{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            new_form=form.save(commit=False)
            new_form.slug=slugify(form.cleaned_data['body'][:30])
            new_form.user=request.user
            new_form.save()
        messages.success(request,'your post is created successfully','success')
        return redirect('accounts:urprofile', request.user.id)


class CommentReplyView(LoginRequiredMixin,View):
    form_class=CommentReplyForm
    def post(self,request,post_id,comment_id):
        post = Post.objects.get(id=post_id)
        comment=Comment.objects.get(id=comment_id)
        form=self.form_class(request.POST)
        if form.is_valid():
            rep=form.save(commit=False)
            rep.user=request.user
            rep.post=post
            rep.reply=comment
            rep.is_reply=True
            rep.save()
            messages.success(request,'your reply is submitted', 'success')
        return redirect('home:detail',post.id,post.slug)



class LikeView(LoginRequiredMixin,View):
    def get(self, request, user_id, post_id):
        post=Post.objects.get(id=post_id)
        like_instance=Vote.objects.filter(user=request.user, post=post)
        if like_instance.exists():
            messages.error(request, 'you have already like this post', 'danger')
        else:
            Vote.objects.create(user=request.user, post=post)
            messages.success(request, ' you liked this post', 'success')

        return redirect("home:detail", post.id, post.slug)



















