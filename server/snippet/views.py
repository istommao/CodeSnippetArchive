from django.views import View
from django.shortcuts import render

from snippet.models import Snippet


class SnippetListView(View):

    def get(self, request, *args, **kwargs):

        snippets = Snippet.objects.order_by('-create_time')
        return render(request, 'index.html', {'snippets': snippets})


class SnippetDetailView(View):

    def get(self, request, pk):

        snippet = Snippet.objects.filter(id=pk).first()
        return render(request, 'snippet.html', {'snippet': snippet})
