from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import wget
import argparse

def download_file(name,url,cookies):
    #print(url)
    s = str(name).strip().replace(' ', '')
    s = str(s).strip().replace('/', '-')
    print(f"{name}")
    wget.download(url,f"{s}.mp4")
    #r = requests.get(url,cookies=cookies,stream=True)
    #with open(f"{s}.mp4",'wb+') as f:
    #    for chunk in r.iter_content(chunk_size=1024*1024*32):
    #        if chunk:
    #            f.write(chunk)
    #            f.flush()
    print(f" Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--auth', type=str, required=True)
    args = parser.parse_args()

    # install chromedriver on home path
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    authn = ".ASPXAUTH"
    url = ""
    cookies = {".ASPXAUTH":""}
    
    if(args.url):
        url = args.url
    if(args.auth):
        cookies[".ASPXAUTH"] = args.auth

    driver.get(url)
    driver.add_cookie({"name":".ASPXAUTH","value":cookies[".ASPXAUTH"]})
    driver.get(url)
    time.sleep(5)
    players = driver.find_elements_by_xpath('//a[@class="thumbnail-link"]')
    viewer_urls = [i.get_attribute('href') for i in players if i.get_attribute('href')]
    embed_urls = [i.replace("Viewer","Embed") for i in viewer_urls]
#driver.get(embed_urls[0])
    for i in embed_urls:
        driver.get(i)
        script = driver.find_elements_by_xpath('//script')[-1]
        scstr = script.get_attribute("innerHTML")
        d_url = scstr[scstr.find('"VideoUrl"')+12:scstr.find('"ViewerIconUrl"')-2]
        furl = d_url.replace('\\',"")
        if( "hls" in furl): 
            furl = furl.replace('hls','mp4')
            furl = furl[:furl.find("mp4")+3]
        #print(furl)
        download_file(driver.title,furl,cookies)


