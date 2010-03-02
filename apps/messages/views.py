from django.http import HttpResponseServerError,HttpResponseNotFound,HttpResponse

def home_page(request):
    return HttpResponse("hey hey hey. so, you made it, aye!")

def view_404(request):
    response = HttpResponseNotFound()
    response.write("The path is not found")
    return response

def view_500(request):
    response = HttpResponseServerError()
    response.write("Something went wrong")
    return response
