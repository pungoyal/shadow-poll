__postcode_name_map = {'31001' : 'Al Rumadi', '31002': 'Al Falojah',
                       '31003' : 'Al Qa\'im', '31004' : 'Haditha',
                       '31005' : 'Enna', '31006' : 'Rawah',
                       '31007' : 'Heet', '31008' :'Al Habanyah',
                       '31009' : 'Al Haqaniyah', '31010' : 'Al Khaldiya',
                       '31011' : 'Al Rutbah', '31012' : 'Al Quqa', 
                       '31013' : 'Al Karmah', '31014' : 'Al Baghdadi',
                       '31015' : 'Al Waleed','Al-Nukhaib' : '31016',
                       '31017' : 'Al Ubaidi','31018' : 'Kabisa',
                       '31019': 'Tarbil', '31020' : 'Abu Ghraib',
                       '31021' : 'Sadah', '31022':'Akashat' 
                       }
    
def get_name(post_code):
    try:
        place_name = __postcode_name_map[post_code]
    except KeyError, ex:
        place_name = "Not Found"
    return place_name