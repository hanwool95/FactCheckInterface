import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from .models import C_result, V_result, Reference_article

from .task_explanation import task_explain_list


# Create your views here.
# 장고 orm 조건문 출처 https://brownbears.tistory.com/63

def check_user_and_get_number(request):
    user_name = request.user.get_username()
    number = '0'
    if user_name[:4] == 'user':
        number = user_name[4:]
    return number

def check_admin(request):
    return request.user.get_username()[:5] == 'admin'

def index(request):
    number = check_user_and_get_number(request)

    return render(request, 'survey/index.html', {'user_id': number})

def claim_current(request, state):
    """
    if check_admin(request):
        number = '관리자'
        claim_list = C_result.objects.all()
        number_of_claim = len(C_result.objects.filter(is_variation=False))
        number_of_variation = len(C_result.objects.filter(is_variation=True))
        return render(request, 'survey/all_current.html', {'user_id': number, 'claim_list': claim_list,
                                                             'number_of_claim': number_of_claim,
                                                             'number_of_variation': number_of_variation})
    """

    number = check_user_and_get_number(request)
    if state < 1:
        claim_list = C_result.objects.filter(user_id=number)
    elif state == 1:
        claim_list = C_result.objects.filter(user_id=number, is_variation=True)
    elif state == 2:
        claim_list = C_result.objects.filter(user_id=number, is_variation=False)
    elif state == 3:
        claim_list = C_result.objects.all()
    elif state == 4:
        claim_list = C_result.objects.filter(is_variation=True)
    else:
        claim_list = C_result.objects.filter(is_variation=False)
    number_of_claim = len(C_result.objects.filter(user_id=number, is_variation=False))
    number_of_variation = len(C_result.objects.filter(user_id=number, is_variation=True))

    number_of_user = len(C_result.objects.filter(user_id=number))

    if number_of_user != 0:
        number_of_True = len(C_result.objects.filter(user_id=number, T_F='True'))
        number_of_False = len(C_result.objects.filter(user_id=number, T_F='False'))
        number_of_NEI = len(C_result.objects.filter(user_id=number, T_F='None'))

        rate_true = round(number_of_True/number_of_user*100, 2)
        rate_false = round(number_of_False / number_of_user*100, 2)
        rate_nei = round(number_of_NEI/number_of_user*100, 2)

        rate_claim = round(number_of_claim/number_of_user*100, 2)
    else:
        rate_true = 0
        rate_false = 0
        rate_nei = 0
        rate_claim = 0


    return render(request, 'survey/claim_current.html', {'user_id': number, 'claim_list':claim_list,
                                                         'number_of_claim': number_of_claim,
                                                         'number_of_variation': number_of_variation, 'state':state,
                                                         'rate_true':rate_true, 'rate_false':rate_false,
                                                         'rate_nei':rate_nei, 'rate_claim': rate_claim})

def all_current(request):
    number = check_user_and_get_number(request)
    claim_list = C_result.objects.all()
    number_of_claim = len(C_result.objects.filter(is_variation=False))
    number_of_variation = len(C_result.objects.filter(is_variation=True))
    return render(request, 'survey/all_current.html', {'user_id': number, 'claim_list': claim_list,
                                                         'number_of_claim': number_of_claim,
                                                         'number_of_variation': number_of_variation})

def claim_detail(request, claim_id):
    number = check_user_and_get_number(request)
    q = C_result.objects.get(id=claim_id)

    try:
        return render(request, 'survey/claim_detail.html', {'user_id': int(number), 'claim': q})
    except:
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

def claim_delete(request, claim_id):
    number = check_user_and_get_number(request)
    q = C_result.objects.get(id=claim_id)
    if int(number) != q.user_id:
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

    C_result.objects.get(id=claim_id).delete()

    return HttpResponseRedirect(reverse('survey:claim_current', args=(0,)))

def claim_update(request, claim_id):
    number = check_user_and_get_number(request)
    q = C_result.objects.get(id=claim_id)
    if int(number) != q.user_id:
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })
    data = None
    original_claim = None
    if q.reference_id != 0:
        data = Reference_article.objects.get(reference_id=q.reference_id)
    if q.original_claim_id != 0:
        original_claim = C_result.objects.get(id=q.original_claim_id)
    try:
        return render(request, 'survey/claim_update.html', {'user_id': number, 'claim': q, 'data': data,
                                                            'original_claim': original_claim})
    except:
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

def claim_update_result(request, claim_id):
    number = check_user_and_get_number(request)
    q = C_result.objects.get(id=claim_id)
    if int(number) != q.user_id:
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })


    q.claim = request.POST['claim']
    q.title1 = request.POST['title1']
    q.evidence1 = request.POST['evidence1']
    q.title2 = request.POST['title2']
    q.evidence2 = request.POST['evidence2']
    q.title3 = request.POST['title3']
    q.evidence3 = request.POST['evidence3']
    q.title4 = request.POST['title4']
    q.evidence4 = request.POST['evidence4']
    q.title5 = request.POST['title5']
    q.evidence5 = request.POST['evidence5']
    q.T_F = request.POST['T_F']
    q.pubdate = timezone.now()

    q.save()

    return HttpResponseRedirect(reverse('survey:claim_detail', args=(claim_id,)))

def making_claim(request):
    number = check_user_and_get_number(request)
    reference_list = Reference_article.objects.filter(count__lte=5)
    data = random.choice(reference_list)

    return render(request, 'survey/making_claim.html', {'user_id': number, 'data': data})

def making_variation(request):
    number = check_user_and_get_number(request)
    task_index = random.choice([0, 1, 2, 3, 4])
    try:
        claim_list = C_result.objects.filter(finish__lte=5, id__gt=136)
        if len(claim_list) == 0:
            claim_list = C_result.objects.filter(finish=6)
        data = random.choice(claim_list)
    except:
        print('error')
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })
    claim = data.claim
    claim_id = data.id
    title1 = data.title1
    evidence1 = data.evidence1
    title2 = data.title2
    evidence2 = data.evidence2
    title3 = data.title3
    evidence3 = data.evidence3
    title4 = data.title4
    evidence4 = data.evidence4
    title5 = data.title5
    evidence5 = data.evidence5
    T_F = data.T_F

    return render(request, 'survey/making_variation.html', {'user_id': number, 'claim': claim,
                                                            'claim_id':claim_id, 'e1':evidence1, 'title1': title1,
                                                            'e2':evidence2, 'title2': title2,
                                                            'e3':evidence3, 'title3': title3,
                                                            'e4':evidence4, 'title4': title4,
                                                            'e5':evidence5, 'title5': title5, 'T_F':T_F,
                                                            'task':task_index})

def claim_results(request, reference_id):
    number = check_user_and_get_number(request)

    try:
        C_result(user_id=number, claim=request.POST['claim'],
                 title1=request.POST['title1'], evidence1=request.POST['evidence1'],
                 title2=request.POST['title2'], evidence2=request.POST['evidence2'],
                 title3=request.POST['title3'], evidence3=request.POST['evidence3'],
                 title4=request.POST['title4'], evidence4=request.POST['evidence4'],
                 title5=request.POST['title5'], evidence5=request.POST['evidence5'],
                 T_F=request.POST['T_F'], pub_date=timezone.now(), finish=0, is_variation=False, original_claim_id=0,
                 reference_id=reference_id).save()
        q = Reference_article.objects.get(reference_id=reference_id)
        q.count += 1
        q.save()
    except:
        print('error')
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

    return HttpResponseRedirect(reverse('survey:claim_current', args=(0,)))



def variation_results(request, claim_id):
    number = check_user_and_get_number(request)
    try:
        C_result(user_id=number, claim=request.POST['claim'],
                 title1=request.POST['title1'], evidence1=request.POST['evidence1'],
                 title2=request.POST['title2'], evidence2=request.POST['evidence2'],
                 title3=request.POST['title3'], evidence3=request.POST['evidence3'],
                 title4=request.POST['title4'], evidence4=request.POST['evidence4'],
                 title5=request.POST['title5'], evidence5=request.POST['evidence5'],
                 T_F=request.POST['T_F'], pub_date=timezone.now(), finish=0, is_variation=True,
                 original_claim_id=claim_id).save()
        q = C_result.objects.get(id=claim_id)
        q.finish += 1
        q.save()
    except:
        print('error')
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

    return HttpResponseRedirect(reverse('survey:claim_current', args=(0,)))
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

