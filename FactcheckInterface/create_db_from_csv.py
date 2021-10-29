import csv, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FactcheckInterface.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""
from survey.models import Reference_article
def get_data():
    f = open('good_article.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    next(rdr)
    for i, line in enumerate(rdr):
        Reference_article(reference_id=line[0], rev_id=line[1], url=line[2], title=line[3], text=line[4], count=0).save()
"""

from survey.models import Paraphrased
def get_data():
    f = open('10_21_utf8-sig.paraphrase.1000.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    next(rdr)
    for i, line in enumerate(rdr):
        Paraphrased(claim_id = int(line[0]),user_id=int(line[1]), claim=line[2], title1=line[3], evidence1=line[4],
                          title2=line[5], evidence2=line[6],
                          title3=line[7], evidence3=line[8],
                          title4=line[9], evidence4=line[10],
                          title5=line[11], evidence5=line[12],
                          T_F= line[13], is_more_than_two=line[14],
                          paraphrased1=line[15], paraphrased2=line[16], paraphrased3=line[17], paraphrased4=line[18],
                          paraphrased5=line[19], finish=0).save()

if __name__ == "__main__":
    get_data()