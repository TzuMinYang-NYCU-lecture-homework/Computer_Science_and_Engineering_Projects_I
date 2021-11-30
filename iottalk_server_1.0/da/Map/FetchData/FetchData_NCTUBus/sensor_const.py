#NCTUBus POST url
NCTUBus_url = 'https://slt.eup.tw:8443/Eup_Servlet_Nuser_SOAP/Eup_Servlet_Nuser_SOAP'
NCTUBus_post_data = {
"102262": 'Param={"MethodName":"GetCarStatusNow","Cust_ID":"5020599","Team_ID":"5019764","Car_Unicode":"102262","Unit_ID":"68","ShiftDetail_ID":"2304"}', 
"110428": 'Param={"MethodName":"GetCarStatusNow","Cust_ID":"5020599","Team_ID":"5019764","Car_Unicode":"110428","Unit_ID":"68","ShiftDetail_ID":"2269"}',
"102414": 'Param={"MethodName":"GetCarStatusNow","Cust_ID":"5020599","Team_ID":"5019764","Car_Unicode":"102414","Unit_ID":"68","ShiftDetail_ID":"2223"}',
}

#NCTUBus sensor list
#POST https://slt.eup.tw:8443/Eup_Servlet_Nuser_SOAP/Eup_Servlet_Nuser_SOAP
#Content-Type: application/x-www-form-urlencoded
#Param={"MethodName":"GetCarStatusNow","Cust_ID":"5020599","Team_ID":"5019764","Car_Unicode":"102262","Unit_ID":"68","ShiftDetail_ID":"2304"}
NCTUBus_sensor_list = [
{'DeviceId': '102262','Nickname': '光復博愛大巴', 'NAME_ON_MAP': 'NCTUBus_光復博愛大巴'},
{'DeviceId': '110428',"Nickname": '高鐵大巴', 'NAME_ON_MAP': 'NCTUBus_高鐵大巴'},
{'DeviceId': '102414',"Nickname": '機動中巴', 'NAME_ON_MAP': 'NCTUBus_機動中巴'},
]