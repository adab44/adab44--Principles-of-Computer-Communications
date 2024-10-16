#
#   https://www.nslookup.io/website-to-ip-lookup/ bu siteyi ip adreslerini kontrol etmek için kullandın rapora koy
import requests
import time
from datetime import datetime


def Ping_Function(ip):
    try:
        starting_time = time.time() #time start
        response = requests.get(f"http://{ip}", timeout=4) #pingig here  
        ending_time = time.time() #time end
        duration = (ending_time - starting_time) * 1000 #to get milliseconds 
        result = f" {ip} is reachable, taken time: {duration:.2f} ms"
    except requests.ConnectionError:
        result = f"Failed to reach {ip} "
    
    return result
"""
def Ping_Https(ip):
    try:
        starting_time = time.time() #time end
        response = requests.get(f"https://{ip}", timeout=10)
        ending_time = time.time() #time end 
        duration = (ending_time - starting_time) * 1000 
        result = f"{ip} is reachable via HTTPS. taken time: {duration:.2f} ms"
    except requests.ConnectionError:
        result = f"Failed to reach {ip} via HTTPS"
    
    return result
"""
#to doc. results
def Save_Result(results):
    with open("dailypings.txt", "a") as file:
        file.write(f"\n ----   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---- \n")
        for result in results:
            file.write(result + "\n")

def main():
    ips = ["160.75.25.62", "185.45.67.130", "185.104.182.64","79.139.60.97","85.239.69.14","141.101.90.96","195.72.120.33","185.18.139.126","104.17.157.36","23.227.38.74"] #IPs to test
    #ip adresleri türkiyeye yakınlık sırasına göre konmuştur
    results = []
    
    for ip in ips:
        results.append(Ping_Function(ip)) #HTTP 
        #results.append(Ping_Https(ip)) #HTTPS bu çalışmadı istekler yanıtsız kalıyor
    
    Save_Result(results) #save

if __name__ == "__main__":
    main()  
