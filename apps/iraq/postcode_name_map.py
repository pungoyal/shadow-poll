__postcode_name_map = {'31001' : 'Al Rumadi', '31002': 'Al Falojah',
                       '31003' : 'Al Qa\'im', '31004' : 'Haditha',
                       '31005' : 'Enna', '31006' : 'Rawah',
                       '31007' : 'Heet', 'Al Habanyah' : '31008',}
    
def get_name(post_code):
    try:
        place_name = __postcode_name_map[post_code]
    except KeyError, ex:
        place_name = "Not Found"
    return place_name
