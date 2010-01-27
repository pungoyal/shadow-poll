__postcode_name_map = {'Al-Anbar' :'31001', 'Al-Basrah' : '31002',
                       'Al-Muthannia':'31003' , 'Al-Qadisiyah' : '31004',
                       'An-Najaf': '31005',  'Arbil' :'31006' ,
                       'As-Sulaymaniyah':'31007',  'At-Ta\'mim':'31008',
                       'Babil' :'31009', 'Baghdad' : '31010',
                       'Dhi-Qar':'31011' , 'Dihok' : '31012', 
                       'Diyala': '31013', 'Karbala\'' : '31014',
                       'Maysan': '31015' , 'Ninawa':'31016',
                       'Sala ad-Din':'31017','Wasit' : '31018',
                       'As-Sulaymaniyah':'31019',  'Arbil':'31020' ,
                       'Al-Basrah':'31021', 'An-Najaf':'31022' 
                       }
    
def get_name(post_code):
    try:
        place_name = __postcode_name_map[post_code]
    except KeyError, ex:
        place_name = "Not Found"
    return place_name