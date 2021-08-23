import requests
import os
import config
import time

def getenv(env):
    d=dict(os.getenv)
    if env in d:
        return d[env]
    else:
        raise Exception

def getCMSResults(url,verbose=False):
    try:
        ATOPSITE_API_KEY=getenv("ATOPSITE_API_KEY")
    except:
        try:
            ATOPSITE_API_KEY=config.ATOPSITE_API_KEY
        except:
            print("api key for whatcms.org not provided.")
            exit(1)
    try:        
        res=requests.get(f"https://whatcms.org/API/Tech?key={ATOPSITE_API_KEY}&url={url}")
    except requests.exceptions.ConnectionError:
        print("Unable To Connect To the Internet.")
        exit(1)
    if res.status_code==200:
        if res.json()["result"]["code"]==101:
            print("Invalid API key for whatcms.org")
            exit(1)
        if res.json()["result"]["code"]==120:
            tts=float(res.json()["retry_in_seconds"])
            if verbose:
                print(f"Maxium API Request Reached. Trying Again in {tts} seconds.")
            time.sleep(tts)
            return getCMSResults(url,verbose)
        if verbose:
            print(res.text)
        cms=None
        framework=None
        programming_lang=None
        server=None
        for des in res.json()["results"]:
            if "CMS" in des["categories"]:
                cms=des["name"]
            elif "Web Framework" in des["categories"]:
                framework=des["name"]
            elif "Programming Language" in des["categories"]:
                programming_lang=des["name"]
            elif "Web Server" in des["categories"]:
                server=des["name"]
        return {
            "cms":cms,
            "framework":framework,
            "language":programming_lang,
            "server":server
        }
    else:
        print("Unknown Error Occured.")
        exit(1)


def getHostResults(url,verbose=False):
    try:
        ATOPSITE_API_KEY=getenv("ATOPSITE_API_KEY")
    except:
        try:
            ATOPSITE_API_KEY=config.ATOPSITE_API_KEY
        except:
            print("api key for whatcms.org not provided.")
            exit(1)
    try:        
        res=requests.get(f"https://www.who-hosts-this.com/API/Host?key={ATOPSITE_API_KEY}&url={url}")
    except requests.exceptions.ConnectionError:
        print("Unable To Connect To The Internet.")
        exit(1)
    if res.status_code==200:
        if res.json()["result"]["code"]==101:
            print("Invalid API key for whatcms.org")
            exit(1)
        elif res.json()["result"]["code"]==120:
            tts=float(res.json()["retry_in_seconds"])
            if verbose:
                print(f"Maxium API Request Reached. Trying Again in {tts} seconds.")
            time.sleep(tts)
            return getHostResults(url,verbose)
        if verbose:
            print(res.text)
        ipv4=None
        ipv6=None
        isp=None
        for des in res.json()["results"]:
            if des["type"]=="AAAA":
                ipv6=des["ip"]
            if des["type"]=="A":
                ipv4=des["ip"]
                isp=des["isp_name"]
        return {
            "ipv4":ipv4,
            "ipv6":ipv6,
            "isp":isp
        }
    else:
        print("Unknown Error Occured.")
        exit(1)

def getThemeResults(url,verbose=False):
    try:
        ATOPSITE_API_KEY=getenv("ATOPSITE_API_KEY")
    except:
        try:
            ATOPSITE_API_KEY=config.ATOPSITE_API_KEY
        except:
            print("api key for whatcms.org not provided.")
            exit(1)
    try:
        res=requests.get(f"https://www.themedetect.com/API/Theme?key={ATOPSITE_API_KEY}&url={url}")
    except requests.exceptions.ConnectionError:
        print("Unable To Connect To The Internet.")
        exit(1)
    if res.status_code==200:
        if res.json()["result"]["code"]==101:
            print("Invalid API key for whatcms.org")
            exit(1)
        elif res.json()["result"]["code"]==203:
            return {
                "name":None,
                "url":None,
                "author":None,
                "description":None
            }
        elif res.json()["result"]["code"]==120:
            tts=float(res.json()["retry_in_seconds"])
            if verbose:
                print(f"Maxium API Request Reached. Trying Again in {tts} seconds.")
            time.sleep(tts)
            return getThemeResults(url,verbose)
        try:
            name=res.json()["results"][0]["theme_name"]
        except IndexError:
            name=None
        try:
            uri=res.json()["results"][0]["theme_uri"]
        except IndexError:
            uri=None
        try:
            author=res.json()["results"][0]["author"]
        except IndexError:
            author=None
        try:
            desc=res.json()["results"][0]["description"]
        except IndexError:
            desc=None
        return {
            "name":name,
            "url":uri,
            "author":author,
            "description":desc
        }
    else:
        print("Unknow Error Occured.")
        exit(1)


def deepScan(url):
    print("Process Started. This might take a minute or so. So , be patient or take a sip at your coffee.")
    cmsresults=getCMSResults(url)
    hostresults=getHostResults(url)
    themeresults=getThemeResults(url)
    print(f"Scan Results of {url}")
    print(f"****************"+("*"*len(url)))
    print("\tContent Management System: ")
    print("\t==========================")
    print(f"\t\tName: {cmsresults['cms'] or 'Unknown'}")
    print(f"\t\tFramework: {cmsresults['framework'] or 'Unknown'}")
    print(f"\t\tProgramming Language: {cmsresults['language'] or 'Unknown'}")
    print(f"\t\tServer: {cmsresults['server'] or 'Unknown'}")
    print("\tHost Details: ")
    print("\t=============")
    print(f"\t\tIPv4: {hostresults['ipv4'] or 'Unknown'}")
    print(f"\t\tIPv6: {hostresults['ipv6'] or 'Unknown'}")
    print(f"\t\tISP: {hostresults['isp'] or 'Unknown'}")
    print("\tTheme Details:")
    print("\t=============")
    print(f"\t\tName: {themeresults['name'] or 'Unknown'}")
    print(f"\t\tAuthor: {themeresults['author'] or 'Unknown'}")
    print(f"\t\tURL: {themeresults['url'] or 'Unknown'}")
    print(f"\t\tDescription: {themeresults['description'] or 'Unknown'}")

if __name__=="__main__":
    url=input("Enter Target Site's URL : ")
    deepScan(url)