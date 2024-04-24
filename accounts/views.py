from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .forms import EditProfileForm
# Create your views here.


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return redirect('accounts:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "username already exists.")
            return redirect('accounts:signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been successfully created.")

        return redirect('articles:travelPage')

    return render(request, "accounts/signup.html")


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                # return render(request, "exchange/travelPage.html", {'fname': fname})
                return redirect('articles:travelPage')
        else:
            return render(request, "accounts/signin.html", {'error_message': "User doesn't exist"})

    return render(request, "accounts/signin.html")


def signout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logged Out Successfully!")
    return redirect('accounts:signin')


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = "accounts/edit_profile.html"
    success_url = reverse_lazy('articles:home')

    def get_object(self, queryset=None):
        return self.request.user

