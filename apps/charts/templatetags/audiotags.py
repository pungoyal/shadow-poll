from django import template

register = template.Library()

@register.inclusion_tag('partials/jplayer.html')
def jplayer(player_id, sound_file_url ):
    context = { 'id':player_id,
                'sound_file_url':sound_file_url 
              }
    return context
