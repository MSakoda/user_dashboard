from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'survey/index.html')

def process_survey(request):
    print "*"*50
    # name = request.POST['name']
    # location = request.POST['location']
    # language = request.POST['language']
    # comment = request.POST['comment']
    request.session['name'] = request.POST['name']
    request.session['location'] = request.POST['location']
    request.session['language'] = request.POST['language']
    request.session['comment'] = request.POST['comment']
    print "*"*50
    return redirect('/survey/success')

def success(request):
    return render(request,'survey/success.html')
