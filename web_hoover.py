#!/usr/bin/env python
# coding: utf-8


import re
import os
import http.client  # bibliotheque HTTP
import sys
from tqdm import tqdm
import requests
from requests.exceptions import Timeout, ConnectionError
import argparse 



def getInnerURLs(content_file):
    try:
        content = str(content_file, "UTF8")
        # re.M == recherche Multilignes
        matches = re.findall(
            "[\"';&][^;'\"&]*/[^;'\"&]+\.(?:js|png|jpeg|jpg|gif|css|xml|ico)[\"';&]", content, re.M)
        matches = [re.sub("[\"';&]", "", url) for url in matches]
        return matches
    except:
        return


def create_nameFile(URL):
    name_file = URL.split("/")[-1]

    if (re.findall('[^"]+\.css|[^"]+\.js|[^"]+\.xss|[^"]+\.s?html', name_file, re.M)):
        if(not os.path.exists("fichiers")):
            os.mkdir("fichiers")
        return "./fichiers/"+name_file
    elif (re.findall('[^"]+\.gif|[^"]+\.jpg|[^"]+\.png|[^"]+\.ico', name_file, re.M)):
        if(not os.path.exists("images")):
            os.mkdir("images")
        return "./images/"+name_file
    else:
        if(not os.path.exists("other")):
            os.mkdir("other")
        return "./other/"+name_file




def download_file(URL):

    connexionHTTP = None

    URL = URL.strip("//")

    URL = "http://"+URL if not re.match("https:*|http:*", URL) else URL

    try:
        with requests.get(URL, stream=True) as response:

            content_length = int(response.headers['Content-length']) if 'Content-length' in response.headers.keys(
            ) else len(response.content)


            chunk_size = 1024
            content = bytes()

           
            for chunk in response.iter_content(chunk_size):
                content += chunk
      
            return content

    except TimeoutError:
        return None
    except (ConnectionError, UnicodeError) as e:
        print("\n error , source : ",URL)
        return None
        




def write_content(name_file, content):
    if(content != None):
        with open(name_file, "wb") as file:
            file.write(content)

def parseArguments():
    parser=argparse.ArgumentParser(description="web downloader description")
    parser.add_argument("--url",required=True,metavar='URL',help="your url")
    return parser.parse_args()

def main():
    #os.system('cls')
    args=parseArguments()
    name_root_file = "index.html"
    
    root_file_content = download_file(args.url)
    
    if root_file_content!=None:
        count=0
        URLS = getInnerURLs(root_file_content)
        total=len(URLS)
        print("found {} rescouces to download".format(total))
        for url in tqdm(URLS,total=total):
            #create new path for file 
            name_file = create_nameFile(url)
            #download the file 
            resource_content = download_file(url)
            if resource_content !=None:
                count += 1  
            #replace url with the new path 
            root_file_content = re.sub(url, name_file, root_file_content.decode())
            #convert it to bytes
            root_file_content = bytes(root_file_content, encoding="utf-8")
            #write the content
            write_content(name_file, resource_content)
        #write the root file content (index.html)    
        write_content(name_root_file, root_file_content)
        print(count)
        print(" {:2.2f} % resources successfully downloaded ".format(count/total*100))
    else :
        print("error , please check your url")    



# https://www.eurosport.com/football/van-dijk-dismisses-talk-of-title-despite-reds-leading-the-way_sto7062094/story.shtml
# https://www.datacamp.com/community/tutorials/markov-chains-python-tutorial

if __name__ == '__main__':
    main()