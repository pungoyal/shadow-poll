__postcode_name_map = {'Ar Ramadi' :'31001', 'Al Fallujah' : '31002',
                       'Al Qa\'im':'31003' , 'Al Haditha' : '31004',
                       'Enna': '31005',  'Rawah' :'31006' ,
                       'Hit':'31007',  'Al Habanyah':'31008',
                       'Al Haqaniyah' :'31009', 'Al Khaldiya' : '31010',
                       'Ar Rutbah':'31011' , 'Anah' : '31012', 
                       'Al Karmah': '31013', 'Al Baghdadi' : '31014',
                       'Al Waleed': '31015' ,'31016' :'Al-Nukhaib' ,
                       'Al Ubaidi':'31017','Kabisa' : '31018',
                       'Tarbil':'31019',  'Abu Ghraib':'31020' ,
                       'Sadah':'31021', 'Akashat':'31022' 
                       }
    
def get_name(post_code):
    print post_code
    try:
        place_name = __postcode_name_map[post_code]
    except KeyError, ex:
        place_name = "Not Found"
    return place_name