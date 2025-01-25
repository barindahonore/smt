from django import template

from citizen.models import Abakandida

register = template.Library()


@register.simple_tag(name='get_total_votes')

def get_total_votes(citizen, post):
    votes = Abakandida.objects.get(citizen=citizen, post=post).votes
    return votes