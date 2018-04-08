from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    if 'products' not in request.session:
        request.session['products'] = [
            {
                'name' : "Dojo Shirt",
                'price' : 19.99,
                'id' : 1
            },
            {
                'name' : "Dojo Sweater",
                'price' : 29.99,
                'id' : 2
            },
            {
                'name' : "Dojo Cup",
                'price' : 4.99,
                'id' : 3
            },
            {
                'name' : "Algorithm book",
                'price' : 49.99,
                'id' : 4
            },
        ]
    return render(request,'amadon/index.html')

def test(request):
    print "this is a test"
    return redirect('/amadon')

def buy(request,number):
    count = request.POST['amount']
    print request.session['products']
    for product in request.session['products']:
        print "*"*50
        print product
        print number
        print "*"*50
        if product['id'] == int(number):
            print "they are buying {}".format(product['name'])
            request.session['last_bought'] = {
                'name' : product['name'],
                'total' : (product['price'] * float(count)),
                'amount' : count,
                'price' : product['price']
            }
            if 'total' not in request.session:
                request.session['total'] = request.session['last_bought']['total']
            else:
                request.session['total'] += request.session['last_bought']['total']
            if 'count' not in request.session:
                request.session['count'] = 1
            else:
                request.session['count'] += 1
            return redirect('/amadon/checkout')
    else:
        print "error finding product"
        return redirect('/amadon')

def checkout(request):
    print "went through checkout"
    print "last bought:"
    print request.session['last_bought']
    return render(request, 'amadon/checkout.html')
