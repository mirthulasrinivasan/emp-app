import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class AuthGuardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ✅ Intercept signup
        if request.path == '/api/signup/' and request.method == 'POST':
            try:
                data = json.loads(request.body)
                username = data.get('username', '').strip()
                email = data.get('email', '').strip()

                if username.lower() == 'admin':
                    return JsonResponse({'error': 'Username "admin" is not allowed'}, status=400)

                if User.objects.filter(username=username).exists():
                    return JsonResponse({'error': 'Username already exists'}, status=409)

                if email and User.objects.filter(email=email).exists():
                    return JsonResponse({'error': 'Email already exists'}, status=409)

            except Exception as e:
                return JsonResponse({'error': f'Invalid signup data: {str(e)}'}, status=400)

        # ✅ Intercept login
        if request.path == '/api/login/' and request.method == 'POST':
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')

                user = authenticate(username=username, password=password)
                if user is None:
                    # ❌ If login fails, return error
                    return JsonResponse({'error': 'Invalid username or password'}, status=401)

                # ✅ Log the user in (create session)
                login(request, user)

            except Exception as e:
                return JsonResponse({'error': f'Login error: {str(e)}'}, status=400)

        return self.get_response(request)
