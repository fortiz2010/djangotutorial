from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

#mdodificado

def home(request):
    latest_vote = Vote.objects.select_related("question").order_by("-vote_date").first()
    context = {"latest_question": latest_vote.question if latest_vote else None}
    return render(request, "polls/home.html", context)


def exit(request):
    logout(request)
    return redirect('polls:home')

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
    Return the last five published questions (not including those set to be
    published in the future).
    """
        
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


#modificado y creado
@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    
    # Verificar si el usuario ya votó en esta pregunta
    existing_vote = Vote.objects.filter(user=request.user, question=question).first()
    if existing_vote:
        # Borrar el voto si ya existe
        existing_vote.delete()

    # Registrar el nuevo voto
    Vote.objects.create(user=request.user, choice=selected_choice, question=question)
    selected_choice.votes = F("votes") + 1
    selected_choice.save()

    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

    


@login_required
def delete_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    vote = Vote.objects.filter(user=request.user, question=question).first()
    if vote:
        vote.choice.votes = F("votes") - 1
        vote.choice.save()
        vote.delete()
    return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))
