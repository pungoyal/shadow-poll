__postcode_name_map = {'Ar Ramadi' :'31001', 'Al Fallujah' : '31002',
                       'Al Qa\'im':'31003' , 'Al Haditha' : '31004',
                       'Samarra': '31005',  'Rawah' :'31006' ,
                       'Hit':'31007',  'Al Habanyah':'31008',
                       'Al Haqaniyah' :'31009', 'Balad Ruz' : '31010',
                       'Ar Rutbah':'31011' , 'Anah' : '31012', 
                       'Al Karmah': '31013', 'Al Baghdadi' : '31014',
                       'Al Waleed': '31015' , 'Balad':'31016',
                       'Hatra':'31017','Al Ba\'aj' : '31018',
                       'Bayji':'31019',  'Abu Ghraib':'31020' ,
                       'Najaf':'31021', 'As Salaman':'31022' 
                       }
    
def get_name(post_code):
    try:
        place_name = __postcode_name_map[post_code]
    except KeyError, ex:
        place_name = "Not Found"
    return place_name