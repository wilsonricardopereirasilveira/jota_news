import re

STOPWORDS = {
    'a', 'o', 'e', 'de', 'do', 'da', 'para', 'com', 'um', 'uma',
    'os', 'as', 'em', 'no', 'na', 'nos', 'nas'
}


def tokenize(text: str):
    words = re.findall(r'[a-zA-Z\u00C0-\u00FF]+', text.lower())
    return [w for w in words if w not in STOPWORDS]
