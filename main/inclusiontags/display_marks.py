from django.template.defaulttags import register
from main.views import MarksData
import json

@register.inclusion_tag('marks_list.html')
def display_marks():
    order = json.loads(MarksData.order_data()['order'])
    return {'order': order}