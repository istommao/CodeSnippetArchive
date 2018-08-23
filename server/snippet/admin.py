from django.contrib import admin


from django.contrib import admin

from snippet.models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    """SnippetAdmin."""
