from django import template

register = template.Library()

@register.inclusion_tag('partials/jplayer.html')
def jplayer(player_id, sound_file_name, server_name):
    context = { 'id':player_id,
                'sound_file_url': "http://" + server_name + sound_file_name 
              }
    return context
