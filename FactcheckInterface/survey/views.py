import random
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from .models import C_result, V_result, Reference_article

from .task_explanation import admin_dict, admin_list
print(admin_dict)
print(admin_list)

# Create your views here.
# 장고 orm 조건문 출처 https://brownbears.tistory.com/63

#출처: https://icodebroker.tistory.com/6852 [ICODEBROKER]
import datetime

def AddDays(sourceDate, count):
    targetDate = sourceDate + datetime.timedelta(days = count)
    return targetDate

def GetWeekFirstDate(sourceDate):
    temporaryDate = datetime.datetime(sourceDate.year, sourceDate.month, sourceDate.day)
    weekDayCount = temporaryDate.weekday()
    targetDate = AddDays(temporaryDate, -weekDayCount)
    return targetDate

def GetLastWeekFirstDate(sourceDate):
    temporaryDate = datetime.datetime(sourceDate.year, sourceDate.month, sourceDate.day)
    weekDayCount = temporaryDate.weekday()
    targetDate = AddDays(temporaryDate, -weekDayCount)
    targetDate = AddDays(targetDate, -7)
    return targetDate


def check_user_and_get_number(request):
    user_name = request.user.get_username()
    number = '0'
    if user_name[:4] == 'user':
        number = user_name[4:]
    return number

def check_admin(number):
    return number in admin_list

def True_False_text_to_Boolean(text):
    Boolean = None
    if text == "True":
        Boolean = True
    else:
        Boolean = False
    return Boolean

def index(request):
    number = check_user_and_get_number(request)

    return render(request, 'survey/index.html', {'user_id': number})

def admin_current(request):
    number = check_user_and_get_number(request)
    if number not in admin_list:
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })
    user_list = admin_dict[number]
    information_list = []
    for user in user_list:
        claim_list = C_result.objects.filter(user_id=user)
        number_of_claim = len(C_result.objects.filter(user_id=user, is_variation=False))
        number_of_variation = len(C_result.objects.filter(user_id=user, is_variation=True))
        number_of_user = len(claim_list)
        first_date = GetWeekFirstDate(datetime.datetime.today())
        last_date = GetLastWeekFirstDate(datetime.datetime.today())
        number_of_week = len(C_result.objects.filter(user_id=user, pub_date__gte=first_date))
        number_of_lweek = len(C_result.objects.filter(user_id=user, pub_date__gte=last_date)) - number_of_week

        today = datetime.date.today()
        first_day = today.replace(day=1)
        number_of_month = len(C_result.objects.filter(user_id=user, pub_date__gte=first_day))

        number_of_True = len(C_result.objects.filter(user_id=user, T_F='True'))
        number_of_False = len(C_result.objects.filter(user_id=user, T_F='False'))
        number_of_NEI = len(C_result.objects.filter(user_id=user, T_F='None'))

        rate_true = round(number_of_True / number_of_user * 100, 2)
        rate_false = round(number_of_False / number_of_user * 100, 2)
        rate_nei = round(number_of_NEI / number_of_user * 100, 2)

        rate_claim = round(number_of_claim / number_of_user * 100, 2)

        class data_class:
            id = 0
            claim = 0
            variation = 0
            number = 0
            week = None
            lweek = None
            month = None
            true = None
            false = None
            nei = None
            true_rate = None
            false_rate = None
            nei_rate = None
            claim_rate = None

            def __init__(self, value):
                self.id = value

        data = data_class(user)
        data.claim = number_of_claim
        data.variation = number_of_variation
        data.number = number_of_user
        data.week = number_of_week
        data.true = number_of_True
        data.false = number_of_False
        data.nei = number_of_NEI
        data.true_rate = rate_true
        data.false_rate = rate_false
        data.nei_rate = rate_nei
        data.claim_rate = rate_claim
        data.lweek = number_of_lweek
        data.month = number_of_month
        globals()[user] = data

        information_list.append(globals()[user])

    return render(request, 'survey/admin_current.html', {'information': information_list})





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
    kw = request.GET.get('kw', '')
    kinds = request.GET.get('kinds', '')
    if kw:
        try:
            kw_number = int(''.join(list(filter(str.isdigit, kw))))
        except:
            kw_number = 0

    number = check_user_and_get_number(request)
    if number == '0':
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })
    admin_Flag = check_admin(number)
    if state < 1:
        claim_list = C_result.objects.filter(user_id=number)
    elif state == 1:
        claim_list = C_result.objects.filter(user_id=number, is_variation=True)
    elif state == 2:
        claim_list = C_result.objects.filter(user_id=number, is_variation=False)
    elif state == 3:
        if kw:
            try:
                if kinds == 'user_id':
                    claim_list = C_result.objects.filter(user_id=kw_number)
                else:
                    claim_list = C_result.objects.filter(id=kw_number)
            except:
                return render(request, 'survey/detail.html', {
                    'error_message': "unaccepted.",
                })
        else:
            claim_list = C_result.objects.all()
    elif state == 4:
        if kw:
            try:
                if kinds == 'user_id':
                    claim_list = C_result.objects.filter(user_id=kw_number, is_variation=True)
                else:
                    claim_list = C_result.objects.filter(id=kw_number, is_variation=True)
            except:
                return render(request, 'survey/detail.html', {
                    'error_message': "unaccepted.",
                })
        else:
            claim_list = C_result.objects.filter(is_variation=True)
    else:
        if kw:
            try:
                if kinds == 'user_id':
                    claim_list = C_result.objects.filter(user_id=kw_number, is_variation=False)
                else:
                    claim_list = C_result.objects.filter(id=kw_number, is_variation=False)
            except:
                return render(request, 'survey/detail.html', {
                    'error_message': "unaccepted.",
                })
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

    claim_list = list(reversed(claim_list))

    return render(request, 'survey/claim_current.html', {'user_id': number, 'claim_list':claim_list,
                                                         'number_of_claim': number_of_claim,
                                                         'number_of_variation': number_of_variation, 'state':state,
                                                         'rate_true':rate_true, 'rate_false':rate_false,
                                                         'rate_nei':rate_nei, 'rate_claim': rate_claim,
                                                         'admin_Flag':admin_Flag})

def all_current(request):
    number = check_user_and_get_number(request)
    if number == '0':
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

    claim_list = C_result.objects.all()
    number_of_claim = len(C_result.objects.filter(is_variation=False))
    number_of_variation = len(C_result.objects.filter(is_variation=True))
    return render(request, 'survey/all_current.html', {'user_id': number, 'claim_list': claim_list,
                                                         'number_of_claim': number_of_claim,
                                                         'number_of_variation': number_of_variation})

def claim_detail(request, claim_id):
    number = check_user_and_get_number(request)
    if number == '0':
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

    q = C_result.objects.get(id=claim_id)

    try:
        return render(request, 'survey/claim_detail.html', {'user_id': int(number), 'claim': q})
    except:
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

def claim_delete(request, claim_id):
    number = check_user_and_get_number(request)
    if number == '0':
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

    q = C_result.objects.get(id=claim_id)
    if int(number) != q.user_id:
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

    C_result.objects.get(id=claim_id).delete()

    return HttpResponseRedirect(reverse('survey:claim_current', args=(0,)))

def claim_update(request, claim_id):
    number = check_user_and_get_number(request)
    if number == '0':
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })

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
    q.is_more_than_two = True_False_text_to_Boolean(request.POST['more_than_two'])

    q.save()

    return HttpResponseRedirect(reverse('survey:claim_detail', args=(claim_id,)))

def making_claim(request):
    number = check_user_and_get_number(request)
    if number == '0':
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })


    reference_list = Reference_article.objects.filter(count__lte=1000)
    data = random.choice(reference_list)

    return render(request, 'survey/making_claim.html', {'user_id': number, 'data': data})

def making_variation(request):
    number = check_user_and_get_number(request)
    if number == '0':
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })


    task_index = random.choice([0, 1, 2, 3, 4])
    try:
        claim_list = C_result.objects.filter(finish__lte=5, id__gt=136, is_variation=False)
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
    more_than_two = data.is_more_than_two

    return render(request, 'survey/making_variation.html', {'user_id': number, 'claim': claim,
                                                            'claim_id':claim_id, 'e1':evidence1, 'title1': title1,
                                                            'e2':evidence2, 'title2': title2,
                                                            'e3':evidence3, 'title3': title3,
                                                            'e4':evidence4, 'title4': title4,
                                                            'e5':evidence5, 'title5': title5, 'T_F':T_F,
                                                            'task':task_index, 'more_than_two':more_than_two})

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
                 reference_id=reference_id,
                 is_more_than_two=True_False_text_to_Boolean(request.POST['more_than_two'])).save()
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
                 original_claim_id=claim_id,
                 is_more_than_two=True_False_text_to_Boolean(request.POST['more_than_two'])).save()
        q = C_result.objects.get(id=claim_id)
        q.finish += 1
        q.save()
    except:
        print('error')
        return render(request, 'survey/detail.html', {
            'error_message': "unaccepted.",
        })
    if request.POST['action'] == '저장 후 베리에이션 추가 제작':
        return HttpResponseRedirect(reverse('survey:making_variation'))
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

