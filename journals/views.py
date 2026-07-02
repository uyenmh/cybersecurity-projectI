from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import connection
from .models import Entry

# Create your views here.

@login_required
def index(request):
    # Flaw 1: A01:2021 – Broken Access Control
    # Any logged in user can view another user's journal entries
    # by changing the "user" parameter in the URL.
    # For example: http://127.0.0.1:8000/journals/?user=anotheruser
    username = request.GET.get("user", request.user.username)
    user = User.objects.get(username=username)

    # Fix for flaw 1:
    # Use the authenticated user instead of getting the "user" parameter from the URL.
    # user = request.user

    entries = Entry.objects.filter(owner=user)
    query = request.GET.get("query")

    # Flaw 2: A03:2021 – Injection
    # Entering ' OR 1=1-- in the search bar returns entries from all users
    # instead of only the entries of the logged in user.
    if query:
        sql = f"""
            SELECT id, content, created_at
            FROM journals_entry
            WHERE owner_id = {user.id}
            AND content LIKE '%{query}%'
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            entries = [{"id": row[0], "content": row[1], "created_at": row[2]} for row in rows]

    # Fix for flaw 2:
    # Use Django's ORM to filter the entries instead of raw SQL queries.
    # if query:
    #     entries = entries.filter(content__icontains=query)

    return render(request, "journals/index.html", {"entries": entries, "user": user, "query": query})


def register(request):
    user = request.user
    if user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(request, "journals/register.html", {"form": form})


@login_required
def add_entry(request):
    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content:
            entry = Entry(owner=request.user, content=content)
            entry.save()

    return redirect("index")


@login_required
def delete_entry(request, entry_id):
    if request.method == "POST":
        user = request.user
        entry = Entry.objects.get(pk=entry_id, owner=user)
        entry.delete()

    return redirect("index")


@login_required
def delete_all_entries(request):
    if request.method == "POST":
        user = request.user
        entries = Entry.objects.filter(owner=user)
        entries.delete()

    return redirect("index")