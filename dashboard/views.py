from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
@login_required
def index(request):
    return render(request, 'dashboard/index.html')