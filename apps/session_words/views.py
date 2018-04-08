from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request,'session_words/index.html')

def process(request):
    print "*"*50
    word = {
        'word' : request.POST['word'],
        'color' : request.POST['color'],
    }
    if 'large_font' in request.POST:
        word['large_font'] = True
    print word

    if 'words' not in request.session:
        request.session['words'] = [word]
    else:
        words = request.session['words']
        words.append(word)
        request.session['words'] = words
    print "*"*50
    return redirect('/session_words')
