from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Teacher, Student, Classe, Topic, Message, Contact
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
    student_classes = student.classes.all()
    notice = None

    if request.method == 'POST':

        if 'class_id' in request.POST:
            cid = request.POST.get('class_id')
            try:
                classe = Classe.objects.get(id=cid)
                student.classes.add(classe)
                student.save()
                return redirect(request.path + "?selected_class=" + str(classe.id))
            except Classe.DoesNotExist:
                notice = 'Class not found'
                return render(request, 'student.html', {'classes': classes, 'student_classes': student_classes, 'topics': [], 'messages': [], 'message': notice, 'selected_class': None})

        if 'leave_class' in request.POST:
            cid = request.POST.get('leave_class')
            try:
                classe = Classe.objects.get(id=cid)
                student.classes.remove(classe)
                next_selected = student.classes.first().id if student.classes.exists() else None
                if next_selected:
                    return redirect(request.path + "?selected_class=" + str(next_selected))
                else:
                    return redirect(request.path)
            except Classe.DoesNotExist:
                notice = 'Class not found'
                return render(request, 'student.html', {'classes': classes, 'student_classes': student_classes, 'topics': [], 'messages': [], 'message': notice, 'selected_class': None})

        if 'message' in request.POST:
            text = request.POST.get('message')
            active_cid = request.POST.get('active_class') or request.GET.get('selected_class')
            target_class = None
            if active_cid:
                try:
                    target_class = student.classes.get(id=active_cid)
                except Classe.DoesNotExist:
                    target_class = None

            if target_class and text:
                Message.objects.create(sender=request.user, classe=target_class, text=text)
                return redirect(request.path + "?selected_class=" + str(target_class.id))
            else:
                notice = 'Select a class you belong to in order to send messages'
                return render(request, 'student.html', {'classes': classes, 'student_classes': student_classes, 'topics': Topic.objects.filter(classe=target_class) if target_class else [], 'messages': Message.objects.filter(classe=target_class) if target_class else [], 'message': notice, 'selected_class': target_class.id if target_class else None})

    selected_id = request.GET.get('selected_class')
    if selected_id:
        try:
            selected = student.classes.get(id=selected_id)
        except Classe.DoesNotExist:
            selected = None
    else:
        selected = student.classes.first() if student.classes.exists() else None

    topics = Topic.objects.filter(classe=selected) if selected else []
    msgs = Message.objects.filter(classe=selected).order_by('-created_at') if selected else []

    return render(request, 'student.html', {'classes': classes, 'student_classes': student_classes, 'topics': topics, 'messages': msgs, 'message': None, 'selected_class': selected.id if selected else None})

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
        students = Student.objects.filter(classes=selected_class).distinct()
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

def about_view(request):
    return render(request,'about.html')

def contact_view(request):
    errors = []

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        message = request.POST.get('message')

        if not name or not email or not message or not phone or not address:
            errors.append("All fields are required.")

        if not errors:
            contact = Contact(
                name=name,
                email=email,
                phone=phone,
                address=address,
                message=message
            )
            contact.save()

            return redirect('contact')

    return render(request, 'contact.html', {'errors': errors})