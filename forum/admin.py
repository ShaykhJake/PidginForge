from django.contrib import admin
from . models import (
  Forum,
  Moderator,
  Thread,
  ThreadFollower,
  Post
)
# Register your models here.

admin.site.register(Forum)
admin.site.register(Moderator)
admin.site.register(Thread)
admin.site.register(ThreadFollower)
admin.site.register(Post)