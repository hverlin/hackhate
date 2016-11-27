import requests


class WotResult:
    def __init__(self, json):
        self.target = json['target']
        self.reputation = json["0"][0]
        self.trustworthiness = json["0"][1]
        categories = json['categories']

        def test_category(code: str) -> bool:
            return code in categories and categories[code] >= 20

        self.marked_positive = test_category("501")
        self.malware = test_category("101")
        self.phishing = test_category("103")
        self.scam = test_category("104")
        self.potentially_illegal = test_category("105")

        self.misleading_or_unethical = test_category("201")
        self.privacy_risk = test_category("202")
        self.suspicious = test_category("203")
        self.hate = test_category("204")
        self.spam = test_category("205")
        self.pup = test_category("206")

        self.alternative_or_controversial_medecine = test_category("302")

    def is_negative(self) -> bool:
        return (
            self.hate or
            self.malware or
            self.phishing or
            self.scam or
            self.potentially_illegal or
            self.misleading_or_unethical or
            self.privacy_risk or
            self.suspicious or
            self.hate or
            self.spam or
            self.pup or
            self.reputation <= 40
        )

    def is_positive(self):
        return self.marked_positive and self.reputation >= 60 and self.trustworthiness >= 20

    def is_undefined(self):
        return not self.is_positive() and not self.is_negative()

    def as_json(self):
        return {
            'target': self.target,
            'negative': self.is_negative(),
            'undefined': self.is_undefined(),
            'positive': self.is_positive(),
            'categories': {
                'malware': self.malware,
                'phishing': self.phishing,
                'scam': self.scam,
                'potentially_illegal': self.potentially_illegal,
                'misleading_or_unethical': self.misleading_or_unethical,
                'privacy_risk': self.privacy_risk,
                'suspicious': self.suspicious,
                'hate': self.hate,
                'spam': self.spam,
                'pup': self.pup,
            }
        }


class WotChecker:
    def __init__(self):
        self._private_key = ''
        self._api_url = 'http://api.mywot.com/0.4/public_link_json2'

    def test_websites_concatenated(self, hosts):
        """
        Query Web of Trust API for given websites
        :param hosts: URLs of at most 100 host separated by '/' and ending by '/'
        :return: a list of dict() objects (one for each URL). Can be empty
        Each object has this shape:
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
        params = {
            'hosts': hosts,
            'key': self._private_key
        }
        result = requests.get(self._api_url, params=params)

        if result.ok:
            content = result.json()
            return [WotResult(v).as_json() for v in content.values() if '0' in v]

        return []

    def test_websites(self, *hosts: str):
        """
        Concatenate hosts URLs and call test_websites_concatenated()
        """
        hosts = ''.join(map(lambda s: s + '/', hosts))

        return self.test_websites_concatenated(hosts)
