from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
    latest_question = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question
    }

    return render(request, 'about/index.html', context )

def detail(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'about/detail.html', { "question": question })

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'about/result.html', {'question': question})

def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'about/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('about:results', args=(question.id,)))
