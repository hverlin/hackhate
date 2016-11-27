from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from apps.text_api.views import ping, twitter_status, facebook_posts, facebook_comments, facebook_reactions, \
    nltk_analysis, text_analysis_page, wot_checking, social_analysis, search_score, search_page, political_description
from junction_hate.hybrid_router import HybridRouter

router = HybridRouter(trailing_slash=False)

router.view_urls = [
    url(r'^ping', ping, name="Ping"),
    url(r'^twitter_status', twitter_status, name="Twitter status"),
    url(r'^facebook_comments', facebook_comments, name="Facebook_comments"),
    url(r'^facebook_reactions', facebook_reactions, name="Facebook reactions"),
    url(r'^facebook_posts', facebook_posts, name="Facebook posts"),
    url(r'^nltk_analysis', nltk_analysis, name="Nltk Analysis"),
    url(r'^search_score', search_score, name="Search Score"),
    url(r'^wot_checking', wot_checking, name="WoT checking")
]

urlpatterns = [
    # utilities
    url(r'^admin/', admin.site.urls),

    # API
    url(r'^api/', include(router.urls)),
    url(r'^docs$/', include('rest_framework_docs.urls')),
    url(r'^$', search_page, name="search page"),
    url(r'social_analysis$', social_analysis, name="social analysis page"),
    url(r'political_description$', political_description, name="political_description page"),
    url(r'analysis$', text_analysis_page, name="analysis page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
