from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.shortcuts import render
from categories.models import Language
from users.models import Profile
from elements.models import YouTubeElement, AudioElement, TextElement


# class IndexTemplateView(LoginRequiredMixin, TemplateView):

#     def get_template_names(self):
#         # template_name = "index_backup.html"
#         template_name = "index.html"
        
#         # if not settings.DEBUG: # IMPORTANT: Remove the "not" here when truly going to production, because of static file services
#         #     # template_name = "index.html"
#         #     template_name = "index-dev.html"
#         # else: 

#         return template_name

# class IndexTemplateView(LoginRequiredMixin, TemplateView):

def allow_guests(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        languages = Language.objects.all().count()
        users = Profile.objects.all().count()
        videos = YouTubeElement.objects.all().count()
        context = {
            'languages': languages,
            'users': users,
            'videos': videos
        }
        return render(request, "guest.html", context)

class IndexTemplateView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        # template_name = "index_backup.html"
        template_name = "index.html"
        
        # if not settings.DEBUG: # IMPORTANT: Remove the "not" here when truly going to production, because of static file services
        #     # template_name = "index.html"
        #     template_name = "index-dev.html"
        # else: 

        return template_name