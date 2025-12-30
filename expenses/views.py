from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Category
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    expenses = Expense.objects.all()
    total = sum([e.amount for e in expenses])
    return render(request, 'expenses/dashboard.html', {'expenses': expenses, 'total': total})

@login_required
def add_expense(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        category_id = request.POST.get('category')
        Expense.objects.create(
            user=request.user,
            amount=request.POST.get('amount'),
            category=Category.objects.get(id=category_id),
            date=request.POST.get('date'),
            description=request.POST.get('description')
        )
        return redirect('dashboard')
    return render(request, 'expenses/add_expense.html', {'categories': categories})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        expense.amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        expense.category = Category.objects.get(id=category_id)
        expense.date = request.POST.get('date')
        expense.description = request.POST.get('description')
        expense.save()
        return redirect('dashboard')
    return render(request, 'expenses/edit_expense.html', {'expense': expense, 'categories': categories})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return redirect('dashboard')
