import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from users.models import CustomUser, Role


class CustomUserManagement(object):
    @staticmethod
    @csrf_exempt
    def create_user(request):
        try:
            data = json.loads(request.body)
            username = data.get("username", "")
            password_1 = data.get("password_1", "")
            password_2 = data.get("password_2", "")
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")
            if not username:
                return JsonResponse({"message": "Provide username"})
            if CustomUser.objects.filter(username=username):
                return JsonResponse({"message": "Username exists"})
            if not password_1 or not password_1 == password_2:
                return JsonResponse({"message": "Incorrect password"})
            role = Role.objects.get(name="Teacher")
            # user = CustomUser(username=username, password=password_1, first_name=first_name, last_name=last_name)
            # user.save()
            username = str(username).lower()
            CustomUser.objects.create(
                username=username, password=password_1, first_name=first_name, last_name=last_name, role=role)
            return JsonResponse({"message": "successful"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"message": "Error occurred"})

    @staticmethod
    @csrf_exempt
    def delete_user(request):
        try:
            data = json.loads(request.body)
            username  = data.get("username", "")
            username  = str(username).lower()
            user = CustomUser.objects.filter(username=username)
            if not user:
                return JsonResponse({"message": "User does not exist"})
            user.first().delete()
            return JsonResponse({"message": "successfully deleted user"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"message": "Error occurred"})