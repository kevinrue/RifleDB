from django.shortcuts import render
from django.http import HttpResponse
from attendance.models import Member

def index(request):
    members_checked_in = Member.objects.filter(checked_in=True)
    output = '\n'.join([p.f_name for p in members_checked_in])
    return HttpResponse(output)

