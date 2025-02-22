from django.shortcuts import render , redirect,get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserLoginForm , UserProfileForm,UserEditForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Relation, UserInfo
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy




class UserRegisterView(View):
    form_class=UserRegisterForm
    template_name='accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)
    def get(self, request):
        form=self.form_class()
        return render(request,self.template_name, {'form':form})
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=User.objects.create_user(cd['username'],cd['email'],cd['password'])
            UserInfo.objects.get_or_create(user=user)


            messages.success(request,'you registered successfully, you can login now ', 'success')
            return redirect('home:home')
        else:
            # Handle invalid form data (e.g., re-render the form with errors)
            return render(request, self.template_name, {'form': form})



class UserLoginView(View):
    form_class=UserLoginForm
    template_name='accounts/login.html'
    def setup(self, request, *args, **kwargs):
        self.next=request.GET.get('next',None)
        return super().setup( request, *args, **kwargs)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)
    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,"you logged in successfully",'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request,"username or password is wrong", 'error')
        return render(request,self.template_name,{'form':form})

class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'u logged out successfully','success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        # Fetch all users
        users = User.objects.all()
        context = {'users': users}
        return render(request, self.template_name, context)


class UserSelfProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/urprofile.html'

    def get(self, request, user_id):
        # Fetch the user whose profile is being viewed
        profile_user = get_object_or_404(User, id=user_id)

        # Fetch posts (assuming the user has a related_name 'posts' for their posts)
        posts = profile_user.posts.all()

        # Check if the logged-in user is following this profile
        is_following = Relation.objects.filter(from_user=request.user, to_user=profile_user).exists()

        # Pass the data to the template
        context = {
            'profile_user': profile_user,  # The user whose profile is being viewed
            'posts': posts,  # Posts by the user
            'is_following': is_following,  # Whether the logged-in user is following this profile
        }
        return render(request, self.template_name, context)


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name='accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'

class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name='accounts/password_reset_done.html'

class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin,View):
    def get(self,request, user_id):
        followed=User.objects.get(id=user_id)
        relation=Relation.objects.filter(from_user=request.user,to_user=followed)
        if relation.exists():
            messages.error(request,'u are already following this user','warning')
        else:
            Relation.objects.create(from_user=request.user,to_user=followed)
            messages.success(request,f'you followed {followed} Now! ','success')
        return redirect('accounts:urprofile', followed.id)

class UserUnfollowView(LoginRequiredMixin,View):
    def get(self,request, user_id):
        unfollowed=User.objects.get(id=user_id)
        relation=Relation.objects.filter(from_user=request.user,to_user=unfollowed)
        if relation.exists():
            relation.delete()
            messages.success(request, f'you unfollowed {unfollowed} Now! ', 'success')
        else:
            messages.error(request, 'u dont follow this user', 'warning')
        return redirect('accounts:urprofile', unfollowed.id)



class UserEditView(LoginRequiredMixin,View):
    form_class=UserEditForm
    def get(self, request):
        form=self.form_class(instance=request.user.userinfo,initial={'email':request.user.email})
        return render(request,'accounts/edit.html',{'form':form})
    def post(self,request):
        form = self.form_class(request.POST,instance=request.user.userinfo)
        if form.is_valid():
            request.user.email=form.cleaned_data['email']
            request.user.save()
            userinfo = form.save(commit=False)  # Don't save to the database yet
            userinfo.age = form.cleaned_data['age']
            userinfo.bio = form.cleaned_data['bio']
            userinfo.save()


            messages.success(request,'your profile is edited successfully','success')
        else:
            messages.error(request,'try again','danger')
        return redirect('accounts:urprofile',request.user.id)






