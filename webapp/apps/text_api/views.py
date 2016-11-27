import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.WikidataQuery import WikidataQuery as Wq
from apps.classifiers.HateBaseClassifier import HateBaseClassifier
from apps.classifiers.NltkClassifier import NltkClassifier
from apps.classifiers.WotChecker import WotChecker
from apps.fact_checker.DuckduckgoSearch import DuckduckgoSearch
from apps.fact_checker import WebSiteCredibility
from apps.text_api.models import SocialSearch
from apps.text_interface import TextFromFacebook as Facebook
from apps.text_interface import TextFromTwitter as Twitter
from apps.text_interface.TextFromFacebook import TextFromFacebook
from apps.text_interface.TextFromTwitter import TextFromTwitter
from apps.fact_checker.WebSiteCredibility import WebSiteCredibility
from newspaper import Article


@api_view()
def ping(request):
    return Response({'success': 'pong'}, status=200)


@api_view()
def twitter_status(request):
    """
    Return a list of twitter status for a user

    query params:
    - user: name of the page
    - number: nb of results (max=20)
    """
    user = request.query_params.get("user")
    nb = request.query_params.get("number")
    txt = Twitter.TextFromTwitter()
    list_tweets = txt.get_status_from_user(user=user, tweet_number=nb)
    return Response({"tweets": list_tweets}, status=200)


@api_view()
def facebook_posts(request):
    """
    Return a list of facebook posts

    query params:
    - name: name of the page
    - number: nb of results (max=20)
    """
    nb = request.query_params.get("number")
    name = request.query_params.get("page_name")
    fb = Facebook.TextFromFacebook()
    list_posts = fb.get_posts_from_page(page_name=name, post_number=nb)
    return Response({"posts": list_posts}, status=200)


@api_view()
def facebook_comments(request: Request):
    """
    Return a list of facebook comments for a post

    query params:
    - id: id of the post
    - number: nb of results (max=20)
    """

    nb = request.query_params.get("number")
    id = request.query_params.get("id")

    fb = Facebook.TextFromFacebook()
    list_comments = fb.get_comments_from_post(post_id=id, comment_number=nb)
    return Response({"comments": list_comments},
                    status=200)


@api_view()
def facebook_reactions(request, format=None):
    """
    Return a list of facebook reactions for a post

    query params:
    - id: id of the post
    """
    id = request.query_params.get("id")
    fb = Facebook.TextFromFacebook()
    reactions = fb.get_reactions_from_post(post_id=id)
    return Response({"reactions": reactions}, status=200)


@api_view()
def nltk_analysis(request):
    """
    query params:
    - text: text to analyze
    result: {
        'reactions': {
            'compound': between -1 and 1,
            'neg': between 0 and 1,
            'neu': between 0 and 1,
            'pos': between 0 and 1
        }
    }
    """
    nltk = NltkClassifier()
    text = request.query_params.get("text")
    analysis = nltk.analyse_text(text)
    return Response({"reactions": analysis}, status=200)


@api_view()
def wot_checking(request):
    """
    Query Web of Trust API for given websites

    Query params:
     - hosts: URLs of at most 100 host separated by '/' and ending by '/'

    Response: A list of Json objects following the schema below (one for each successful request)
    {
        'target': string (the URL host),
        'negative': Boolean,
        'undefined': Boolean,
        'positive': Boolean,
        'categories': {
            'malware': Boolean,
            'phishing': Boolean,
            'scam': Boolean,
            'potentially_illegal': Boolean,
            'misleading_or_unethical': Boolean,
            'privacy_risk': Boolean,
            'suspicious': Boolean,
            'hate': Boolean,
            'spam': Boolean,
            'pup': Boolean,
        }
    }
    """
    wot_checker = WotChecker()
    hosts = request.query_params.get("hosts")
    results = wot_checker.test_websites_concatenated(hosts)

    return Response({"results": results}, status=200)


def text_analysis_page(request):
    url = None
    text = request.GET.get('text')
    if not text:
        return JsonResponse({"error": "please provide text"})

    if "http" in text or "www" in text:
        url = text
        article = Article(text)
        article.download()
        article.parse()
        text = article.text

    return render_analysis_text(request, text, url)


def render_analysis_text(request, text, url):
    nltk = NltkClassifier()

    analysis = nltk.analyse_text(text)
    hate_classifier = HateBaseClassifier()
    bad_words = hate_classifier.classify_with_info(text)
    arr, keys = [], []
    for (key, item) in analysis.items():
        arr.append(item)
        keys.append(key)

    if url:
        ds = DuckduckgoSearch(search=url)
    else:
        ds = DuckduckgoSearch(search=text)

    website_list = ds.get_link_list()
    wsc = WebSiteCredibility(website_list=website_list)
    credibility = wsc.compute_score_for_website_liste()

    click_bait = ds.estimate_number_click_bait()
    credibility["CLICKBAIT"] += click_bait

    duck_search = ds.get_request()
    return render(request, 'analysis/text_analysis.html',
                  {
                      "text": text,
                      "analysis": arr,
                      "keys_analysis": mark_safe(keys),
                      "bad_words": bad_words,
                      "credibility": credibility,
                      "duckduck_url": duck_search
                  })


def social_analysis(request):
    text = request.GET.get('text')
    if not text:
        return JsonResponse({"error": "please provide text"})

    nltk = NltkClassifier()

    twitter_stats, facebook_stats, stats = None, None, {}

    twitter = TextFromTwitter()
    t_user = twitter.search_first_user(search_user=text)

    if t_user is not None:
        twitter_stats = twitter.get_nltk_statistic(user=t_user["screen_name"])


    facebook = TextFromFacebook()
    f_page = facebook.search_first_page(search_page=text)

    if f_page is not None:
        facebook_stats = facebook.get_nltk_statistic(id=f_page["id"])
        if facebook_stats is None:
            f_page = None

    stats["labels"] = mark_safe(["min", "mean", "max"]),

    try:
        if t_user and f_page:

            ss, created = SocialSearch.objects.get_or_create(search=text.title())
            ss.number += 1
            ss.picture_url = t_user["profile_image_url"]
            ss.save()

            stats["scores"] = [
                np.min([twitter_stats["stats"]["scores"][0], facebook_stats["stats"]["scores"][0]]),
                np.mean([twitter_stats["stats"]["scores"][1], facebook_stats["stats"]["scores"][1]]),
                np.max([twitter_stats["stats"]["scores"][2], facebook_stats["stats"]["scores"][2]]),
            ]
        elif t_user is not None:
            stats["scores"] = twitter_stats["stats"]["scores"]
        elif f_page is not None:
            stats["scores"] = facebook_stats["stats"]["scores"]
    except:
        pass

    if t_user is None and f_page is None:
        return render_analysis_text(request, text, None)
    else:
        return render(request, 'analysis/social_analysis.html',
                      {
                          "twitter": twitter_stats,
                          "t_user": t_user,
                          "facebook": facebook_stats,
                          "f_page": f_page,
                          "stats": stats
                      })


def search_page(request):
    return render(request, 'analysis/search.html',
                  {
                      "searchs": SocialSearch.objects.all()[:10]
                  })


@api_view()
def search_score(request, format=None):
    """
    Return a score compute in function of the websites get by a duckduckgo research

    query params:
    - search: search string
    """
    search = request.query_params.get("search")

    ds = DuckduckgoSearch(search=search)

    website_list = ds.get_link_list()
    wsc = WebSiteCredibility(website_list=website_list)
    scores = wsc.compute_score_for_website_liste()

    click_bait = ds.estimate_number_click_bait()
    scores["CLICKBAIT"] += click_bait

    duck_search = ds.get_request()

    return Response({
        "search": search,
        "scores": scores,
        "search_link": duck_search}, status=200)


def get_political_qid(request, wikidata):
    id_type = request.GET.get('id_type')

    if id_type == "facebook":
        facebook_id = request.GET.get('id')
        res = wikidata.search_politician_with_facebook(facebook_id=facebook_id)

    elif id_type == "twitter":
        twitter_id = request.GET.get('id')
        res = wikidata.search_politician_with_twitter(twitter_id=twitter_id)
    else:
        lastname = request.GET.get('lastname')
        firstname = request.GET.get('firstname')

        res = wikidata.search_politician(firstname=firstname, lastname=lastname)

    if res:
        return res
    else:
        return None


def political_description(request):
    wikidata = Wq()
    res = get_political_qid(request=request, wikidata=wikidata)
    if res:
        name = res[0]
        qid = res[1]
        return render(request, 'analysis/political_description.html',
                      {
                          "poli_name": name,
                          "poli_awards": wikidata.awards(qid),
                          "poli_birthdate": wikidata.birthdate(qid),
                          "poli_image": wikidata.image(qid),
                          "poli_official_website": wikidata.official_website(qid),
                          "poli_political_parties": wikidata.political_parties(qid)
                      })
    else:
        return JsonResponse({"error": "not found"}, status=404)
