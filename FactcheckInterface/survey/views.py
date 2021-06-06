from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from .models import C_result, V_result

# Create your views here.


def check_user_and_get_number(request):
    user_name = request.user.get_username()
    number = '0'
    if user_name[:4] == 'user':
        number = user_name[4:]
    return number

def index(request):
    number = check_user_and_get_number(request)

    return render(request, 'survey/index.html', {'user_id': number})

def claim_current(request):
    number = check_user_and_get_number(request)
    claim_list = C_result.objects.filter(user_id=number)
    number_of_list = len(claim_list)

    return render(request, 'survey/claim_current.html', {'user_id': number, 'claim_list':claim_list,
                                                         'number_of_list': number_of_list})

def claim_detail(request, claim_id):
    number = check_user_and_get_number(request)
    q = C_result.objects.get(id=claim_id)
    if int(number) != q.user_id:
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

    return render(request, 'survey/claim_detail.html', {'user_id': number, 'claim': q})

    try:
        return render(request, 'survey/claim_detail.html', {'user_id': number, 'claim': q})
    except:
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

def making_claim(request):
    number = check_user_and_get_number(request)

    return render(request, 'survey/making_claim.html', {'user_id': number})

def making_variation(request):
    number = check_user_and_get_number(request)
    try:
        data = C_result.objects.filter(finish=0)[0]
    except:
        print('error')
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })
    title = data.title
    claim = data.claim
    claim_id = data.id
    evidence1 = data.evidence1
    evidence2 = data.evidence2
    evidence3 = data.evidence3
    evidence4 = data.evidence4
    evidence5 = data.evidence5
    T_F = data.T_F

    return render(request, 'survey/making_variation.html', {'user_id': number, 'title': title, 'claim': claim,
                                                            'claim_id':claim_id, 'e1':evidence1, 'e2':evidence2,
                                                            'e3':evidence3, 'e4':evidence4, 'e5':evidence5, 'T_F':T_F})

def claim_results(request):
    number = check_user_and_get_number(request)
    try:
        C_result(user_id=number, claim=request.POST['claim'],
                 title1=request.POST['title1'], evidence1=request.POST['evidence1'],
                 title2=request.POST['title2'], evidence2=request.POST['evidence2'],
                 title3=request.POST['title3'], evidence3=request.POST['evidence3'],
                 title4=request.POST['title4'], evidence4=request.POST['evidence4'],
                 title5=request.POST['title5'], evidence5=request.POST['evidence5'],
                 T_F=request.POST['T_F'],pub_date=timezone.now(), finish=0).save()
    except:
        print('error')
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

    return HttpResponseRedirect(reverse('survey:claim_current'))

def variation_results(request, claim_id):
    number = check_user_and_get_number(request)
    print(claim_id)

    try:
        V_result(user_id=number, claim_id=int(claim_id),
                 variation1=request.POST['variation1'], variation2=request.POST['variation2'],
                 variation3=request.POST['variation3'], variation4=request.POST['variation4'],
                 variation5=request.POST['variation5'],
                 T_F1=request.POST['T_F1'], T_F2=request.POST['T_F2'], T_F3=request.POST['T_F3'],
                 T_F4=request.POST['T_F4'], T_F5=request.POST['T_F5'], pub_date=timezone.now()).save()

        q = C_result.objects.get(id=claim_id)
        q.finish = 1
        q.save()

    except:
        print('error')
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

    return HttpResponseRedirect(reverse('survey:claim_current'))
"""
def detail(request, group_id, user_id, current_num):
    if user_id != int(check_user_and_get_number(request)) or group_id != int(get_pagenumber_from_userid_n_current(user_id, current_num)):
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })
    questions = Reference.objects.filter(group=group_id)
    questions = get_question_and_round_bert_score(questions)
    context = questions[0].context
    title = questions[0].title
    return render(request, 'survey/detail.html', {'question_list': questions, 'context': context, 'user_id': user_id, 'group_id': group_id,
                                                  'current_num': current_num, 'context_num': len(user_dic[user_id]), 'page_num': current_num +1,
                                                  'title': title})
                                                  
"""

