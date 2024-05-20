from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .forms import EditProfileForm
# Create your views here.


def signup(request):
    # Handles user registration
    if request.method == "POST":
        # Collects data from the form submission
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Checks if passwords match
        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return redirect('accounts:signup')

        # Checks if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "username already exists.")
            return redirect('accounts:signup')

        # Creates a new user if validations pass
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        # Inform user of successful account creation
        messages.success(request, "Your Account has been successfully created.")
        return redirect('articles:index')

    # Render the signup form if not POST request
    return render(request, "accounts/signup.html")


def signin(request):
    # Handles user login
    if request.method == 'POST':
        # Collect login credentials
        username = request.POST['username']
        pass1 = request.POST['pass1']

        # Authenticate user
        user = authenticate(username=username, password=pass1)

        if user is not None:
            # Login successful
            login(request, user)
            if 'next' in request.POST:
                # Redirect to requested page if 'next' parameter exists
                return redirect(request.POST.get('next'))
            else:
                #  Redirect to homepage if login successful and no 'next' parameter
                return redirect('articles:index')
        else:
            # Render login form with error if authentication fails
            return render(request, "accounts/signin.html", {'error_message': "User doesn't exist"})

    # Render login form if not POST request
    return render(request, "accounts/signin.html")


def signout(request):
    # Handles user logout
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logged Out Successfully!")
    return redirect('accounts:signin')


class UserEditView(generic.UpdateView):
    # Class-based view to handle user profile editing
    form_class = EditProfileForm # Form class used for editing profile
    template_name = "accounts/edit_profile.html" # Template used to render the edit profile page
    success_url = reverse_lazy('articles:index') # Redirect URL on successful update

    def get_object(self, queryset=None):
        # Method to get the object to be edited;
        return self.request.user

