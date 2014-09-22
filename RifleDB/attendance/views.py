import datetime

from django.shortcuts import render

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


COOLDOWN_CARD_SECONDS = 10

def checkInOut(request):
    # Get the current time
    now = datetime.datetime.now()
    # Extract the RFID from the the POST form
    rfid = request.POST['RFID']
    # Get the current list of members currently checked in once for the different output views
    members_checked_in = Member.objects.filter(checked_in=True)
    # if the RFID is not registered, log as an "in" attempt
    try:
        card = AccessCard.objects.get(pk=rfid)
    except (KeyError, AccessCard.DoesNotExist):
        l = LoggingEvent(rfid=rfid, check_in=now, valid=False)
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
        l = LoggingEvent(rfid=rfid, check_in=now, valid=False)
        l.save()
        # Redisplay the RFID input form.
        return render(request, 'attendance/RFID_form.html', {
            'error_message': "This is not the latest card registered to member: %s %s." % (m.f_name, m.l_name),
            'members_checked_in': members_checked_in,
        })
    # if it is a checked-in member
    if m.checked_in:
        # Get the latest check-in
        ls = LoggingEvent.objects.filter(rfid=card.rfid).order_by('-check_in')
        if len(ls) >= 1:
            l = ls[0]
            # Check that the latest check-in was at least 1 min ago
            if datetime.timedelta(0) < (now - l.check_in) < datetime.timedelta(
                    seconds=COOLDOWN_CARD_SECONDS):  # TODO: prevent check-out before check-in
                return render(request, 'attendance/RFID_form.html', {
                    'error_message': 'Member %s %s checked in less than %i seconds ago. Card on cooldown.' % (m.f_name, m.l_name, COOLDOWN_CARD_SECONDS),
                    'members_checked_in': members_checked_in,
                })
            if now - l.check_in < datetime.timedelta(0):  # TODO: prevent check-out before check-in
                return render(request, 'attendance/RFID_form.html', {
                    'error_message': 'Hey %s %s, go back to your DeLorean: You\'re trying to check out before you checked in.' % (m.f_name, m.l_name),
                    'members_checked_in': members_checked_in,
                })
            # put the timestamp in 'check_out' column
            l.check_out = now
            l.save()
    # if it is a checked-out member,
    else:
        # Get the latest entry for that member in the logging table
        old_ls = LoggingEvent.objects.filter(rfid=card.rfid).order_by('-check_out')
        if len(old_ls) >= 1:
            old_l = old_ls[0]
            # Check that the latest check-out was at least 1 min ago
            if datetime.timedelta(0) < (now - old_l.check_out) < datetime.timedelta(
                    seconds=COOLDOWN_CARD_SECONDS):  # TODO: prevent check-in before latest check-out
                return render(request, 'attendance/RFID_form.html', {
                    'error_message': 'Member %s %s checked out less than %i seconds ago. Card on cooldown.' % (m.f_name, m.l_name, COOLDOWN_CARD_SECONDS),
                    'members_checked_in': members_checked_in,
                })
            if now - old_l.check_in < datetime.timedelta(0):  # TODO: prevent check-in before latest check-out
                return render(request, 'attendance/RFID_form.html', {
                    'error_message': 'Hey %s %s, go back to your DeLorean: You\'re trying to check out before you checked in.' % (m.f_name, m.l_name),
                    'members_checked_in': members_checked_in,
                })
        # create a new entry and put the timestamp in 'check_in' column
        l = LoggingEvent(rfid=rfid, check_in=now, valid=True)
        l.save()
        # Switch the status from in to out or vice-versa
    m.checked_in = 1 - m.checked_in
    m.save()
    # Get the updated list of members currently checked in
    members_checked_in = Member.objects.filter(checked_in=True)
    return render(request, 'attendance/RFID_form.html', {
        'member': m,
        'members_checked_in': members_checked_in})