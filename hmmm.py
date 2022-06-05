from turtle import down
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os
import wget
import argparse
from urllib.parse import urlparse



def process_page(url,folder_name=None):
    i = url.replace("Viewer","Embed")
    driver.get(i)
    driver.add_cookie({"name":".ASPXAUTH","value":cookies[".ASPXAUTH"]})
    driver.get(i)
    
    script = driver.find_elements_by_xpath('//script')[-1]
    scstr = script.get_attribute("innerHTML")
    d_url = scstr[scstr.find('"VideoUrl"')+12:scstr.find('"ViewerIconUrl"')-2]
    furl = d_url.replace('\\',"")
    if( "hls" in furl): 
        furl = furl.replace('hls','mp4')
        furl = furl[:furl.find("mp4")+3]
    #print(furl)
    if folder_name is not None:
        download_file(driver.title,furl,folder_name)
    else:
        download_file(driver.title,furl)


def download_file(name,url,folder_name=None):
    s = str(name).strip().replace(' ', '_')
    s = str(s).strip().replace('/', '-')
    print(f"Downloading {name} ...")
    if folder_name is not None:
        final_directory = os.path.join(os.getcwd(),folder_name)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        
        wget.download(url,f"{final_directory}/{s}.mp4")
    else:
        wget.download(url,f"{s}.mp4")
    print(f" Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--auth', type=str, required=True)
    parser.add_argument('--bpath', type=str, required=True)
    args = parser.parse_args()

    # install chromedriver on home path
    os.environ['WDM_LOG_LEVEL'] = '0'
    s=Service(ChromeDriverManager().install())
    if(args.bpath):
        options = webdriver.ChromeOptions()
        options.binary_location = args.bpath
        driver = webdriver.Chrome(service=s,options=options)
    else:
        driver = webdriver.Chrome(service=s)
    
    authn = ".ASPXAUTH"
    url = ""
    cookies = {".ASPXAUTH":""}
    
    if(args.url):
        url = args.url
    if(args.auth):
        cookies[".ASPXAUTH"] = args.auth
    
    parsed_url = urlparse(url)
    print(parsed_url.path)
    if(parsed_url.path.endswith("/Pages/Viewer.aspx")):
        print("Single video mode.")
        process_page(url)
        quit()
    elif(parsed_url.path.endswith("/Sessions/List.aspx")):   
        print("All videos mode.")    
        driver.get(url)
        driver.add_cookie({"name":".ASPXAUTH","value":cookies[".ASPXAUTH"]})
        driver.get(url)
        time.sleep(5)
        players = driver.find_elements_by_xpath('//a[@class="thumbnail-link"]')
        folder_name  = driver.find_elements_by_xpath('//*[@id="contentHeaderText"]')[0].get_attribute("innerHTML")
        viewer_urls = [i.get_attribute('href') for i in players if i.get_attribute('href')]
        [process_page(i,folder_name) for i in viewer_urls]
        quit()
    else:
        print("Error parsing URL. Try adding/removing quotes from the URL parameter")
