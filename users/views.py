import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from users.models import CustomUser, Role


class CustomUserManagement:
    @staticmethod
    @csrf_exempt
    def create_user(request):
        try:
            data = json.loads(request.body)
            username = data.get("username", "").lower()
            password_1 = data.get("password_1", "")
            password_2 = data.get("password_2", "")
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")

            if not username:
                return JsonResponse({"message": "Provide username"}, status=400)
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({"message": "Username already exists"}, status=400)
            if not password_1 or password_1 != password_2:
                return JsonResponse({"message": "Passwords do not match"}, status=400)

            # Retrieve the role
            role = Role.objects.get(name="Teacher")

            # Create the user with hashed password
            user = CustomUser.objects.create(
                username=username,
                password=make_password(password_1),  # Hash the password
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            return JsonResponse({"message": "User created successfully", "user_id": user.id}, status=201)

        except Role.DoesNotExist:
            return JsonResponse({"message": "Role 'Teacher' does not exist"}, status=400)
        except Exception as ex:
            print(ex)
            return JsonResponse({"message": "An error occurred while creating the user"}, status=500)

    @staticmethod
    @csrf_exempt
    def delete_user(request):
        try:
            data = json.loads(request.body)
            username = data.get("username", "").lower()
            user = CustomUser.objects.filter(username=username).first()

            if not user:
                return JsonResponse({"message": "User does not exist"}, status=404)

            user.delete()
            return JsonResponse({"message": "User deleted successfully"}, status=200)

        except Exception as ex:
            print(ex)
            return JsonResponse({"message": "An error occurred while deleting the user"}, status=500)
