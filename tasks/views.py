from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from django.shortcuts import render,redirect,get_object_or_404
from .forms import TaskForm
from .models import Task
from django.db.models import Q

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,'Registration Successfull')
            return redirect('task_list')
    else:
        form=RegisterForm()
    return render (request,'tasks/register.html',{'form':form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user:
            login(request,user)
            return redirect('task_list')
        else:
            messages.error(request,"Invalid User or Password")
    return render(request,'tasks/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
@login_required
def task_list(request):
    query = request.GET.get('q', '')  # default empty string
    tasks = Task.objects.filter(user=request.user)  # start with user's tasks

    if query:
        tasks = tasks.filter(title__icontains=query)  # filter by search

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'query': query})



@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            task =form.save(commit=False)
            task.user =request.user
            task.save()
            return redirect('task_list')
    else:
        form= TaskForm()
    return render(request, 'tasks/task_form.html',{'form':form})
@login_required
def task_update(request,pk):
    task = get_object_or_404(Task,pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('task_list')
    return render(request,'tasks/task_form.html',{'form':form})
@login_required
def task_delete(request,pk):
    task = get_object_or_404(Task,pk=pk)
    if request.method =='POST':
        task.delete()
        return redirect('task_list')
    return render (request, 'tasks/task_delete.html',{'task':task})




