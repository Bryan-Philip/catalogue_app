from django.template.defaulttags import register
from main.repo_manager import COMMIT_HASH

@register.inclusion_tag('update_status.html')
def git_status():
    LOCAL = COMMIT_HASH('local')
    REMOTE = COMMIT_HASH('remote')
    if LOCAL == REMOTE:
        update = False
    elif LOCAL != REMOTE:
        update = True
    else:
        update = False
    return { 'update': update }