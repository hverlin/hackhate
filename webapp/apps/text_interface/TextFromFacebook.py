from django.utils.safestring import mark_safe
from facepy import GraphAPI
import scipy.stats
from apps.classifiers import NltkClassifier
from apps.fact_checker import DuckduckgoSearch as DuckSearch
from apps.fact_checker import WebSiteCredibility
from junction_hate import settings_local as st


class TextFromFacebook():
    def __init__(self):
        app_id = st.FACEBOOK_app_id
        app_secret = st.FACEBOOK_app_secret

        self.graph = GraphAPI(oauth_token=app_id + "|" + app_secret)

        # self.graph = GraphAPI(oauth_token=access_token)

    def get_page_id(self, page_name):
        request = page_name
        answer = self.graph.get(request)
        return answer["id"]

    # return a list with all the post message and their id
    def get_posts_from_page(self, id, post_number):

        post_list = []

        request = id + "/posts"
        posts = self.graph.get(path=request, limit=post_number)
        for p in posts["data"]:
            if "message" in p:
                post = {"id": p["id"], "message": p["message"]}
                post_list.append(post)

        return post_list

    def get_comments_from_post(self, post_id, comment_number):

        request = post_id + "/comments"
        comments = self.graph.get(path=request, limit=comment_number)
        comment_list = []

        for c in comments["data"]:
            if "message" in c:
                comment_list.append(c["message"])

        return comment_list

    # return the number of reactions by type of reaction : "LIKE","LOVE","HAHA","WOW","SAD","ANGRY","THANKFUL"
    def get_reactions_from_post(self, post_id):

        request = post_id + "/reactions"
        summary = "total_count"
        reaction_possibility = {"LIKE", "LOVE", "HAHA", "WOW", "SAD", "ANGRY", "THANKFUL"}
        reaction_count = dict()

        for rp in reaction_possibility:
            reactions = self.graph.get(path=request, limit=0, type=rp, summary=summary)
            number_react = reactions["summary"]["total_count"]
            reaction_count[rp] = number_react

        return reaction_count

    def get_nltk_statistic(self, id, post_number=30):
        classifier = NltkClassifier.NltkClassifier()
        posts = self.get_posts_from_page(id, post_number)
        posts_with_scores = []
        compound_scores = []
        if len(posts) > 0:
            for post in posts:
                scores = classifier.analyse_text(post['message'])
                posts_with_scores.append({
                    'message': post['message'],
                    'scores': scores
                })
                compound_scores.append(scores['compound'])
            stats = scipy.stats.describe(compound_scores)
            return {
                "posts": posts_with_scores,
                "stats": {
                    "labels": mark_safe(["min", "mean", "max"]),
                    "scores": [stats.minmax[0], stats.mean, stats.minmax[1]],
                }
            }
        else:
            return None

    def search_first_page(self, search_page):
        request = "search?q=" + search_page + "&type=page"
        pages = self.graph.get(path=request, limit=1)
        if not pages["data"]:
            return None
        else:
            page_id = pages["data"][0]["id"]
            fields = "description,about,cover,fan_count,general_info,name,username,picture"
            page = self.graph.get(path=page_id, fields=fields)
            return page


if __name__ == '__main__':
    facebook = TextFromFacebook()
    # print(facebook.get_nltk_statistic("153080620724", 10))
    # print(facebook.get_nltk_statistic("barackobama", 10))
    facebook = TextFromFacebook()
    f_page = facebook.search_first_page(search_page="lepen")
    print(f_page['id'])
    if f_page is not None and f_page['id'] is not None:
        facebook_stats = facebook.get_nltk_statistic(id=f_page["id"])
        print(facebook_stats)
