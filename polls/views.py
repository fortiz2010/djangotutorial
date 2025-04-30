from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout##

#funcion de la vista home muestra la ultima pregunta que el usuario respondio y muestra la plantilla home.html
def home(request):
    latest_question = None
    if request.user.is_authenticated:
        for question in Question.objects.order_by('-pub_date'): # Obtener la última pregunta que el usuario ha votado
            for choice in question.choice_set.all():
                if request.user in choice.voted_by.all():
                    latest_question = question
                    break
            if latest_question:
                break
    return render(request, 'polls/home.html', {'latest_question': latest_question})


def exit(request):
    logout(request)
    return redirect('polls:home')

#vista encargada de mostrar la plantilla index y de mostrar las preguntas publicadas en la aplicacion
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
    Return the last five published questions (not including those set to be
    published in the future).
    """
        
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

#vista encargada de mostrar los detalles de mostrar los detalles de la pregunta que se busque responder
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        question = self.get_object()

        # Verificar si el usuario ya votó en esta encuesta
        user_has_voted = False
        if user.is_authenticated:
            for choice in question.choice_set.all():
                if user in choice.voted_by.all():
                    user_has_voted = True
                    break

        context['user_has_voted'] = user_has_voted
        return context

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


#vista encargada de mostrar los resultados de las votaciones de la preguntas
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

#esta funcion solo podra hacerse si es que esta logueado el usuario
@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user

    # Verificar si el usuario ya votó en esta encuesta
    user_has_voted = False
    for choice in question.choice_set.all():
        if user in choice.voted_by.all():
            user_has_voted = True
            break

    if user_has_voted:
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Ya has votado en esta encuesta. Borra tu voto para votar nuevamente.",
            },
        )

    if not question.is_active:
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Esta encuesta ha sido deshabilitada.",
            },
        )

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "No seleccionaste una opción.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.voted_by.add(user)
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

    
@login_required
def delete_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user

    # Buscar la opción que el usuario votó
    for choice in question.choice_set.all():
        if user in choice.voted_by.all():
            choice.votes = F("votes") - 1
            choice.voted_by.remove(user)
            choice.save()
            break

    return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))

@login_required
def disable_poll(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.created_by:
        question.is_active = False
        question.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

