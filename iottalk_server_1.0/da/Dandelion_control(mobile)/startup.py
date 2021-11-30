import time
import requests
import register

while True:
    try:
        feature_list = ['size-I', 
                        'angle-I', 
                        'color_r-I', 
                        'color_g-I', 
                        'color_b-I',
                        'bg_color_r-I', 
                        'bg_color_g-I', 
                        'bg_color_b-I', 
                        's0-I', 
                        's1-I', 
                        's2-I', 
                        's3-I', 
                        'a1-I', 
                        'easingRate-I'];

        profile = {
            'd_name': 'Dandelion_control',
            'dm_name': 'Dandelion_control',
            'u_name': 'yb',
            'is_sim': False,
            'df_list': feature_list,
        }

        mac = "Dandelion_control"

        result = register.register(mac, profile)

        if result: 
            passwd_file = open(r'./da/Dandelion_control(mobile)/passwd_dandelion_control', 'w+')
            passwd_file.write(result[1])
            passwd_file.close()
            break
           
    except requests.exceptions.ConnectionError as e:
        print('requests.exceptions.ConnectionError:', e)
        print('retry after 3 second')
        time.sleep(3)
    except register.CSMError as e:
        print('csmapi.CSMError:', e)
        print('retry after 3 second')
        time.sleep(3)

print('Dandelion_control registration is done.' )
