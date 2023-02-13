from django.shortcuts import render
def my_view(request):
    context = {'foo':'bar'}
    return render(request,'myapp/my_template.html',context )