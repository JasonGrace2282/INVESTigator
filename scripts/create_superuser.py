from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    username = "admin"
    User.objects.create_superuser(username, "admin@gmail.com", input("Enter an admin password: "))
    print(f"Created admin account with {username = }")
