import csv, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FactcheckInterface.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from survey.models import Reference_article
def get_data():
    f = open('good_article.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    next(rdr)
    for i, line in enumerate(rdr):
        Reference_article(reference_id=line[0], rev_id=line[1], url=line[2], title=line[3], text=line[4], count=0).save()

if __name__ == "__main__":
    get_data()