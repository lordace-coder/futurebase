from django import template
import json
from bson import ObjectId

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)

@register.filter
def normalize_boolean(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.lower().strip()
        return value in ['true', '1', 'on', 'yes', 't']
    return bool(value)

@register.filter
def get_id(document):
    """Safely get the _id field from a MongoDB document"""
    if hasattr(document, '_id'):
        return document._id
    elif isinstance(document, dict):
        return document.get('_id', '')
    return ''

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

@register.filter(is_safe=True)
def tojson(obj):
    """Serialize object to JSON, handling MongoDB ObjectId"""
    return json.dumps(obj, cls=JSONEncoder) 