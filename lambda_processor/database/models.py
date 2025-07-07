from .connection import get_connection
from ..utils.logger import logger


def insert_news(data: dict):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM news_news WHERE url=%s', (data.get('url'),))
            if cur.fetchone():
                logger.info({'skip': 'duplicate', 'url': data.get('url')})
                return
            cur.execute('SELECT id FROM categories_category WHERE name=%s', (data['category'],))
            row = cur.fetchone()
            category_id = row[0] if row else None
            if data.get('subcategory'):
                cur.execute('SELECT id FROM categories_subcategory WHERE name=%s', (data['subcategory'],))
                srow = cur.fetchone()
                subcategory_id = srow[0] if srow else None
            else:
                subcategory_id = None
            cur.execute(
                'INSERT INTO news_news (category_id, subcategory_id, title, content, source, published_at, is_urgent) '
                'VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id',
                (
                    category_id,
                    subcategory_id,
                    data['title'],
                    data.get('content'),
                    data.get('source'),
                    data.get('published_at'),
                    data.get('urgency', 0) > 70,
                ),
            )
            news_id = cur.fetchone()[0]
            for tag in data.get('tags', []):
                slug = tag.replace(' ', '-').lower()
                cur.execute(
                    'INSERT INTO news_tag (name, slug) VALUES (%s,%s) ON CONFLICT (slug) DO UPDATE SET name=EXCLUDED.name RETURNING id',
                    (tag, slug),
                )
                tag_id = cur.fetchone()[0]
                cur.execute(
                    'INSERT INTO news_newstag (news_id, tag_id) VALUES (%s,%s) ON CONFLICT DO NOTHING',
                    (news_id, tag_id),
                )
        conn.commit()
    except Exception as exc:
        conn.rollback()
        logger.error({'db_error': str(exc)})
        raise
    finally:
        conn.close()
