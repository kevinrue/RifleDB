import datetime

from django.shortcuts import render, get_object_or_404

from attendance.models import Member, AccessCard, LoggingEvent

def index(request):
    members_checked_in = Member.objects.filter(checked_in=True)
    return render(request, 'attendance/index.html', {
        'members_checked_in': members_checked_in
    })

def swipe(request):
    members_checked_in = Member.objects.filter(checked_in=True)
    return render(request, 'attendance/RFID_form.html', {
        'members_checked_in': members_checked_in
    })

def checkInOut(request):
    # Extract the RFID from the the POST form
    rfid = request.POST['RFID']
    # Get the current list of members currently checked in once for the different output views
    members_checked_in = Member.objects.filter(checked_in=True)
    # if the RFID is not registered, log as an "in" attempt
    try:
        card = AccessCard.objects.get(pk=rfid)
    except (KeyError, AccessCard.DoesNotExist):
        l = LoggingEvent(rfid=rfid, check_in=datetime.datetime.now(), check_out=None)
        l.save()
        # Redisplay the RFID input form.
        return render(request, 'attendance/RFID_form.html', {
            'error_message': "This card is not registered in the system.",
            'members_checked_in': members_checked_in,
        })
    # At this stage, we know the card is registered (to a member), get the member (without try/except)
    m = Member.objects.get(pk=card.member.student_id)
    # Get the latest card registered to this member
    latest_card = AccessCard.objects.filter(member=m.student_id).order_by('-reg_date')[0]
    # if the card swiped is not the latest card for that member, log the attempt as a non-member above
    if card != latest_card:
        l = LoggingEvent(rfid=rfid, check_in=datetime.datetime.now(), check_out=None)
        l.save()
        # Redisplay the RFID input form.
        return render(request, 'attendance/RFID_form.html', {
            'error_message': "This is not the latest card registered to member: %s %s." % (m.f_name, m.l_name),
            'members_checked_in': members_checked_in,
        })
    if m.checked_in:
        # if it is a checked-in member, put the timestamp in 'check_in' column
        l = LoggingEvent.objects.filter(rfid=card.rfid).order_by('-check_in')[0]
        l.check_out = datetime.datetime.now()
        l.save()
    else:
        # if it is a checked-out member, create a new entry and put the timestamp in 'check_out' column
        l = LoggingEvent(rfid=rfid, check_in=datetime.datetime.now(), check_out=None)
        l.save()
        # Switch the status from in to out or vice-versa
    m.checked_in = 1 - m.checked_in
    m.save()
    # Get the updated list of members currently checked in
    members_checked_in = Member.objects.filter(checked_in=True)
    return render(request, 'attendance/RFID_form.html', {
        'member': m,
        'members_checked_in': members_checked_in})