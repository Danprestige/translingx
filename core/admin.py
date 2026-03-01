from django.contrib import admin
from .models import User, Post  # Only import models that exist

# Register your models to appear in the Django admin
admin.site.register(User)
admin.site.register(Post)

# Optional: Uncomment this if you add a Follow model later
# from .models import Follow
# admin.site.register(Follow)