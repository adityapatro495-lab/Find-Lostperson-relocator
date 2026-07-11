from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignUpForm


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            role = user.userprofile.role
            if role == 'ADMIN':
                return redirect('match_review')
            elif role == 'FAMILY':
                return redirect('case_dashboard')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})
