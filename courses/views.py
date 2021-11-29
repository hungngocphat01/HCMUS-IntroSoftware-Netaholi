from django.shortcuts import render
from .models import Course

# Create your views here.
def detail_page_view(req, pk):
    course = Course.objects.get(id=pk)
    context = {'course': course}
    return render(req, 'courses/details.html', context)