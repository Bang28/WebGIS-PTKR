from django.shortcuts import redirect
from django.contrib import messages

def user_is_aunthenticated(function=None, redirect_url="ptkr:beranda"):
    def decorator(view_func):
        def _wrapper_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.info(request, "Maaf, halaman yang anda minta tidak ditemukan.") 
                return redirect(redirect_url)
            
            return view_func(request, *args, **kwargs)
        
        return _wrapper_view
    
    if function:
        return decorator(function)
    
    return decorator