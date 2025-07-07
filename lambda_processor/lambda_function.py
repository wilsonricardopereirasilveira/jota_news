import json
from .classifier.category_classifier import CategoryClassifier
from .classifier.tag_extractor import TagExtractor
from .classifier.urgency_scorer import UrgencyScorer
from .database.models import insert_news
from .utils.logger import logger

classifier = CategoryClassifier()
tagger = TagExtractor()
scorer = UrgencyScorer()


def lambda_handler(event, context):
    records = event.get('Records', [])
    for record in records:
        try:
            payload = json.loads(record['body'])
        except Exception as exc:
            logger.error({'invalid_json': str(exc)})
            continue
        title = payload.get('title', '')
        content = payload.get('content', '')
        category, subcategory = classifier.classify(title, content)
        tags = tagger.extract(f"{title} {content}")
        urgency = scorer.score(title, content, payload.get('published_at'))
        data = {
            'title': title,
            'content': content,
            'source': payload.get('source'),
            'published_at': payload.get('published_at'),
            'url': payload.get('url'),
            'author': payload.get('author'),
            'category': category,
            'subcategory': subcategory,
            'tags': tags,
            'urgency': urgency,
        }
        try:
            insert_news(data)
            logger.info({'processed': payload.get('url')})
        except Exception as exc:
            logger.error({'error': str(exc), 'url': payload.get('url')})
    return {'statusCode': 200}
