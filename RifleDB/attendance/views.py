from django.shortcuts import render

from attendance.models import Member

def index(request):
    members_checked_in = Member.objects.filter(checked_in=True)
    context = {'members_checked_in': members_checked_in}
    return render(request, 'attendance/index.html', context)
