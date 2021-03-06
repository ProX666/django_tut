from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Choice, Question


class IndexView(generic.ListView):
	# override standard template polls/question_list.html (<app name>/<model name>_list.html)
    template_name = 'polls/index.html'
	# override automatically generated context variable question_list,
	# or use question_list in templates/polls/index.html
	# but it is a lot easier to just tell Django to use the variable you want
    context_object_name = 'latest_question_list'

    def get_queryset(self):
		"""
		Return the last five published questions (not including those set to be
		published in the future).
		"""
		return Question.objects.filter(
			pub_date__lte=timezone.now()
		).filter(choice__isnull=False).distinct().order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
	# override standard template polls/question_detail.html (<app name>/<model name>_detail.html)
    template_name = 'polls/detail.html'

    def get_queryset(self):
		"""
		Excludes any questions that aren't published yet.
		"""
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
	# override standard template polls/question_detail.html (<app name>/<model name>_detail.html)
    template_name = 'polls/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
