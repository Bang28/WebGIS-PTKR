from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def signOut(request):
    """Sign Out"""
    logout(request)
    messages.success(request, "Sign Out Succesfully")
    return redirect('ptkr:beranda')

def signIn(request):
    """Sign In"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Sign in Succesfully")
            return redirect('ptkr:beranda')
        else:
            messages.error(request, 'Sign in Failed, Please check your username and password.')
            return redirect('ptkr:beranda')