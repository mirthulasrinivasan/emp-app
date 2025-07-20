
import json
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import employees, emp_details
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.http import JsonResponse

@csrf_exempt
def get_employees(request):
    try:
        search_query = request.GET.get('q', '').strip().lower()
        queryset = emp_details.objects.select_related('empid')
        if search_query:
            queryset = queryset.filter(
                empid__emp_id__icontains=search_query
            )

        data = queryset.values(
            'empid__emp_id',
            'empid__emp_name',
            'emp_num',
            'emp_email',
            'emp_add'
        )

        employees = []
        for item in data:
            employees.append({
                'emp_id': item['empid__emp_id'],
                'emp_name': item['empid__emp_name'],
                'phone': item['emp_num'],
                'email': item['emp_email'],
                'address': item['emp_add']
            })

        return JsonResponse(employees, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def index(request):
    details=emp_details.objects.all()
    return render(request,'details.html',{'details':details})
    
def add_employee_details(request):
    if request.method == "POST":
        name = request.POST['emp_name']
        employee_id = request.POST['emp_id']
        emp_number = request.POST['emp_num']
        email = request.POST['emp_email']
        add = request.POST['emp_add']
        
        employee = employees(emp_name=name, emp_id=employee_id)
        employee.save()
        details=emp_details(
        empid=employee,
        emp_num=emp_number,
        emp_email=email,
        emp_add=add
             )
        details.save()
        return redirect('index')
    return render(request,'index.html')

def delete_employee(request, id):
    detail = emp_details.objects.get(id=id)
    detail.delete()
    return redirect('index') 

@csrf_exempt
@require_http_methods(["POST"])
def add_employee_json(request):
    try:
        data = json.loads(request.body)
        if employees.objects.filter(emp_id=data['emp_id']).exists():
            return JsonResponse({'error': 'Employee ID already exists'}, status=400)
            
        emp = employees.objects.create(
            emp_id=data['emp_id'],
            emp_name=data['emp_name']
        )

        emp_detail = emp_details.objects.create(
            empid=emp,
            emp_email=data['email'],
            emp_num=data['phone'],
            emp_add=data['address']
        )

        return JsonResponse({'message': 'Employee added successfully'})
    except Exception as e:
        print("Error occurred:", e)
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_employee(request, emp_id):
    try:
        data = json.loads(request.body)
        emp = employees.objects.get(emp_id=emp_id)
        detail = emp_details.objects.get(empid=emp) 

        emp.emp_name = data.get('emp_name', emp.emp_name)
        detail.emp_num = data.get('phone', detail.emp_num)
        detail.emp_email = data.get('email', detail.emp_email)
        detail.emp_add = data.get('address', detail.emp_add)

        emp.save()
        detail.save()
        return JsonResponse({'message': 'Employee updated successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_employee_json(request, emp_id):
    try:
        emp = employees.objects.get(emp_id=emp_id)
        emp_details.objects.filter(empid=emp).delete() 
        emp.delete()
        return JsonResponse({'message': 'Employee deleted successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
def check_email_exists(request):
    email = request.GET.get('email')
    exists = emp_details.objects.filter(emp_email=email).exists()
    return JsonResponse({'exists': exists})

@csrf_exempt
def check_phone_exists(request):
    phone = request.GET.get('phone')
    exists = emp_details.objects.filter(emp_num=phone).exists()
    return JsonResponse({'exists': exists})

@csrf_exempt
def signup_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create_user(
            username=data['username'],
            email=data.get('email'),
            password=data['password']
        )
        return JsonResponse({'message': 'Signup successful', 'user': user.username})

@csrf_exempt
def login_user(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': f"Welcome {request.user.username}"})
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
