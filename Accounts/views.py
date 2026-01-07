from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Teacher, Student, Classe, Topic, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

def home(request):
    return render(request, "home.html")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data["role"]

            if role == 'teacher':
                Teacher.objects.create(user=user)
            elif role == 'student':
                Student.objects.create(user=user)

            return redirect('login')
    else :
        form = RegisterForm()
    return render(request,'register.html',{'form':form})

def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=identifier, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)

            if hasattr(user,'student'):
                return redirect("student")
            elif hasattr(user,'teacher'):
                return redirect("teacher")

        else:
            messages.error(request, "Invalid username/email or password")

    return render(request, "login.html")


@login_required
@ensure_csrf_cookie
def student_view(request):
    student = None
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        
        classes = Classe.objects.all()
        return render(request, 'student.html', {'classes': classes, 'topics': [], 'messages': [], 'message': 'No student profile found.'})

    classes = Classe.objects.all()
    notice = None

    if request.method == 'POST':

        if 'class_id' in request.POST:
            cid = request.POST.get('class_id')
            try:
                classe = Classe.objects.get(id=cid)
                student.classe = classe
                student.save()
                notice = f'Joined class {classe.name}'
            except Classe.DoesNotExist:
                notice = 'Class not found'
            return render(request, 'student.html', {'classes': classes, 'topics': Topic.objects.filter(classe=student.classe) if student.classe else [], 'messages': Message.objects.filter(classe=student.classe) if student.classe else [], 'message': notice})

        if 'message' in request.POST:
            text = request.POST.get('message')
            if student.classe and text:
                Message.objects.create(sender=request.user, classe=student.classe, text=text)
                notice = 'Message sent'
            else:
                notice = 'Join a class first to send messages'
            return render(request, 'student.html', {'classes': classes, 'topics': Topic.objects.filter(classe=student.classe) if student.classe else [], 'messages': Message.objects.filter(classe=student.classe) if student.classe else [], 'message': notice})

    topics = Topic.objects.filter(classe=student.classe) if student.classe else []
    msgs = Message.objects.filter(classe=student.classe).order_by('-created_at') if student.classe else []

    return render(request, 'student.html', {'classes': classes, 'topics': topics, 'messages': msgs, 'message': None})

@login_required
@ensure_csrf_cookie
def teacher_view(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    classes = Classe.objects.filter(teacher=teacher)

    selected_class = None
    selected_class_id = request.POST.get('selected_class') or request.GET.get('selected_class')

    if selected_class_id:
        try:
            selected_class = Classe.objects.get(id=selected_class_id, teacher=teacher)
        except Classe.DoesNotExist:
            selected_class = None

    if not selected_class and classes.exists():
        selected_class = classes.first()

    if request.method == 'POST':

        if 'logout' in request.POST:
            logout(request)
            return redirect('login')

        if 'create_class' in request.POST:
            class_name = request.POST.get('class_name')
            if class_name:
                new = Classe.objects.create(name=class_name, teacher=teacher)
                return redirect(request.path + "?selected_class=" + str(new.id))
            return redirect('teacher')

        if 'create_topic' in request.POST:
            if selected_class:
                title = request.POST.get('topic_title')
                if title:
                    Topic.objects.create(title=title, classe=selected_class)
            return redirect(request.path + "?selected_class=" + (str(selected_class.id) if selected_class else ''))

        if 'delete_class' in request.POST:
            if selected_class:
                selected_class.delete()
            return redirect('teacher')

        if 'delete_topic' in request.POST:
            tid = request.POST.get('delete_topic')
            if tid and selected_class:
                Topic.objects.filter(id=tid, classe=selected_class).delete()
            return redirect(request.path + "?selected_class=" + (str(selected_class.id) if selected_class else ''))

        if 'toggle_topic' in request.POST:
            tid = request.POST.get('topic_id')
            if tid and selected_class:
                t = get_object_or_404(Topic, id=tid, classe=selected_class)
                t.is_completed = not t.is_completed
                t.save()
            return redirect(request.path + "?selected_class=" + (str(selected_class.id) if selected_class else ''))

        if 'send_all' in request.POST or 'send_one' in request.POST:
            text = request.POST.get('message')
            if selected_class and text:

                Message.objects.create(sender=request.user, classe=selected_class, text=text)
            return redirect(request.path + "?selected_class=" + (str(selected_class.id) if selected_class else ''))

    if selected_class:
        students = Student.objects.filter(classe=selected_class)
        topics = Topic.objects.filter(classe=selected_class)
        messages_list = Message.objects.filter(classe=selected_class).order_by('-created_at')
    else:
        students = Student.objects.none()
        topics = Topic.objects.none()
        messages_list = Message.objects.none()

    return render(request, 'teacher.html', {
        'classes': classes,
        'topics': topics,
        'students': students,
        'messages': messages_list,
        'selected_class': selected_class.id if selected_class else None,
    })