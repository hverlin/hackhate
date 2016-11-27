from apps.text_api.models import Site
from apps.text_api.models import WebsiteType
from urllib.parse import urlparse
from newspaper import Article
from apps.classifiers.NltkClassifier import NltkClassifier

class WebSiteCredibility:

    def __init__(self, website_list):
        self.website_list = website_list


    def compute_score_for_website_liste(self):
        scores = dict()
        types = dict()
        for type in WebsiteType.objects.all():
            scores[type.name] = 0
            types[type.id] = type.name

        for website in self.website_list:
            #get just the start of url whitout www.
            url = urlparse(website)
            netloc = url.netloc.replace("www.", "")

            q = Site.objects.filter(url__icontains=netloc)
            for res in q:
                type = types[res.type_id]
                scores[type] += 1

        return scores



    def summary_links_content(self):
        link_list = self.website_list()
        sum = 0
        for link in link_list[0:30]:
            a = Article(link)
            a.download()
            a.parse()
            a.nlp()
            print(link)
            classifier = NltkClassifier()
            res_summary = classifier.analyse_text(txt=a.summary)
            sum += res_summary["compound"]

        mean = sum / len(link_list)
        print(mean)


if __name__ == '__main__':
    '''ds = WebSiteCredibility("earth is flat")
    ds.summary_links_content()'''