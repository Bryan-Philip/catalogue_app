from django.template.defaulttags import register

@register.filter
def in_list(key, list_val):
    if(len(list_val)) > 0:
        if key in list_val:
            return True
        else:
            return False
    else:
        return False