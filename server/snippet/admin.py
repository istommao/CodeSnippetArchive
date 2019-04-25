
from django import forms
from django.contrib import admin
from django.template import loader
from django.utils.safestring import mark_safe

from snippet.models import Snippet


class InputMultiple(forms.Widget):
    template_name = 'widgets/input_multiple.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        context.update({'value': value, 'name': name})
        template = loader.get_template(self.template_name).render(context)

        return mark_safe(template)


class SnippetForm(forms.ModelForm):

    class Meta:
        model = Snippet
        widgets = {
            'tags': InputMultiple()
        }
        fields = '__all__'


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    """SnippetAdmin."""

    list_display = ('title', 'create_time')

    form = SnippetForm
