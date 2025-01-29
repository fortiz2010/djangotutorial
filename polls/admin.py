from django.contrib import admin

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
        ("Active Status", {"fields": ["is_active"]}),
        ("Created By", {"fields": ["created_by"]}),
    ]

    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "is_active", "was_published_recently"]
    list_filter = ["pub_date", "is_active"]
    search_fields = ["question_text"]




admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)