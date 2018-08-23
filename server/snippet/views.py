from django.views import View
from django.shortcuts import render

from snippet.models import Snippet


class SnippetListView(View):

    def get(self, request, *args, **kwargs):

        snippet = Snippet.objects.order_by('-create_time').first()
        return render(request, 'snippet.html', {'snippet': snippet})
