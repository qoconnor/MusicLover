from django.shortcuts import redirect, render

def loginRedirect(request):
    #if request.user.is_authenticated():
        return redirect('/account')
        #return redirect('/account/login')
