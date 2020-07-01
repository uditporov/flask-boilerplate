from app import app
from contextlib import ContextDecorator
from connectors.database import db
from flask import url_for


def paginate_data(response, paginated_query, page_number, url_name, query_params={}):
    next_url = url_for(url_name, page_number=page_number + 1, **query_params) if paginated_query.has_next else None
    prev_url = url_for(url_name, page_number=page_number - 1, **query_params) if paginated_query.has_prev else None

    response.metadata['next'] = next_url
    response.metadata['prev'] = prev_url
    response.metadata['page'] = page_number
    response.metadata['per_page'] = query_params.get('per_page') or app.config['ENTITY_PER_PAGE']
    response.data = paginated_query.items


def paginate_query(query, page_number, per_page=None):
    offset = per_page if per_page and per_page < app.config['ENTITY_PER_PAGE'] else app.config['ENTITY_PER_PAGE']
    paginated_query = query.paginate(page_number, offset, False)
    return paginated_query


class Atomic(ContextDecorator):

    def __init__(self, instance):
        instance.auto_commit = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            db.session.rollback()
        else:
            db.session.commit()

