from webapp.apps.fact_checker.DuckduckgoSearch import DuckduckgoSearch
from WotChecker import WoTChecker

website_liste = DuckduckgoSearch().search_on_html_duckduckgo("donal trump")
print(website_liste)
wtc = WoTChecker()
res = wtc.test_websites(*website_liste)
print(res)