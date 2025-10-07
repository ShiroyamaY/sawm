import re
from django.db import connection, IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_GET, require_POST


def validate_input(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_]{3,32}", value or ""))


@require_GET
def index(request):
    return redirect('login')


@require_GET
def login_view(request):
    return render(request, 'login.html')


@require_POST
def login_vuln(request):
    username = request.POST.get('login', '')
    password = request.POST.get('password', '')
    # VULNERABLE: string formatting directly into SQL
    sql = f"SELECT id, login FROM demo_user WHERE login = '{username}' AND password = '{password}'"
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
    except Exception as e:
        messages.error(request, f"SQL error: {e}")
        return redirect('login')
    if row:
        request.session['user'] = {'id': row[0], 'login': row[1]}
        return redirect('admin_area')
    messages.error(request, 'Invalid credentials (vulnerable).')
    return redirect('login')


@require_POST
def login_safe(request):
    username = request.POST.get('login', '')
    password = request.POST.get('password', '')
    if not validate_input(username) or not validate_input(password):
        messages.error(request, 'Invalid input format.')
        return redirect('login')
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, login FROM demo_user WHERE login = %s AND password = %s",
            [username, password]
        )
        row = cursor.fetchone()
    if row:
        request.session['user'] = {'id': row[0], 'login': row[1]}
        return redirect('admin_area')
    messages.error(request, 'Invalid credentials (safe).')
    return redirect('login')


def admin_area(request):
    user = request.session.get('user')
    if not user:
        messages.error(request, 'Please login first.')
        return redirect('login')
    return render(request, 'admin.html', {'user': user})


def logout_view(request):
    request.session.flush()
    messages.info(request, 'Logged out.')
    return redirect('login')


@require_GET
def init_seed(request):
    users = [
        ("alice", "password1"),
        ("bob", "password2"),
        ("charlie", "password3"),
        ("dave", "password4"),
        ("eve", "password5"),
        ("mallory", "password6"),
        ("trent", "password7"),
    ]
    inserted = 0
    with connection.cursor() as cursor:
        for login, pwd in users:
            try:
                cursor.execute(
                    "INSERT INTO demo_user (login, password) VALUES (%s, %s)",
                    [login, pwd]
                )
                inserted += 1
            except Exception:
                pass
    return render(request, 'init.html', { 'inserted': inserted, 'total': len(users) })
