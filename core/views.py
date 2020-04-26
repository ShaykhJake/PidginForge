from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class IndexTemplateView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        # template_name = "index_backup.html"
        template_name = "index.html"
        
        # if not settings.DEBUG: # IMPORTANT: Remove the "not" here when truly going to production, because of static file services
        #     # template_name = "index.html"
        #     template_name = "index-dev.html"
        # else: 

        return template_name