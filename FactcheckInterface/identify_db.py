# python manage.py shell


from survey.models import C_result
print(len(C_result.objects.all()))
from survey.models import C_result
print(C_result.objects.all())
from survey.models import C_result
print(C_result.objects.all().values())
from survey.models import V_result
print(V_result.objects.all().values())

from survey.models import Reference_article
print(Reference_article.objects.all().values())

from polls.models import Result
print(len(Result.objects.filter(T_F='True')))





###### 주의##################3
from survey.models import Paraphrased
Paraphrased.objects.all().delete()

################주의###################