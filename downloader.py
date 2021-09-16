#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import requests
import time
import re
from bs4 import BeautifulSoup
import m3u8
import sys
from tqdm import tqdm

search_url = "https://ww.9anime2.com/search/"
watch_url = "https://ww.9anime2.com/watch/"
base = "https://ww.9anime2.com"


# In[ ]:





# In[2]:


anime = input("Enter Anime Name : ")
search_term = "%20".join(anime.split())


# In[ ]:





# In[3]:


url = search_url+search_term
r = requests.get(url)
soup = BeautifulSoup(r.text, features="lxml")


# In[ ]:





# In[4]:


titles = soup.find("ul", {"class": "anime-list"})
anime_list = titles.find_all("li")
title_list = ["\t".join(i.text.replace("\ndub","").replace(" Series","").replace("Special ","Special").split("\n")[3:]) for i in anime_list]


# In[ ]:





# In[5]:


print()
print(str(len(title_list)) + " Results found matching name : " + anime)
print("\nIndex \t Type \t Name\n")
for i in range(len(title_list)):
    print(str(i+1) + "\t " + title_list[i])


# In[6]:


print()
choice = input("Enter anime index to download : ")

suffix = "-".join(title_list[int(choice)-1].split('\t')[1].split()).lower()
url = "https://ww.9anime2.com/watch/"+suffix
r = requests.get(url)
soup = BeautifulSoup(r.text, features="lxml")


# In[7]:


episodes = soup.find("ul", {"class": "episodes"})
noe = len(episodes.find_all('li'))


# In[8]:


print('\n-------------------------\n')
print("Number of downloadable episodes in the series : " + str(noe))


# In[9]:


choice = input("\nEnter episode(s) to be downloaded (space-separatred): ")
choice = re.sub("[^0-9]", " ", choice)


# In[10]:


choices = choice.split()
for i in choices:
    if(int(i) not in range(1,noe+1)):
        print("Latest episode count is "+str(noe)+". ")
        print("Skipping episode "+i)
        choices.remove(i)
        print()


# In[11]:


choices = list(sorted(set(choices)))


# In[12]:


DOWNLOAD_LINKS = []
print('\n-------------------------\n')
print("Collecting download links \n")


# In[ ]:





# In[ ]:





# In[13]:


for i in tqdm(choices):
    URL = url+"/"+i
    episode_page = requests.get(URL)
    soup = BeautifulSoup(episode_page.text, features="lxml")
    embed = soup.find("iframe", {"id": "playerframe"}).get('src')
    embed_url = base + embed
    embed_page = requests.get(embed_url)
    soup = BeautifulSoup(embed_page.text, features="lxml")
    data  = str(soup.find_all("script")[-1].string)
    link = re.search("(?P<url>https?://[^\s]+)", data).group("url").replace("'","")
    if link[-10:] == 'index.m3u8':
        link = link[:-10]
    DOWNLOAD_LINKS.append(link)
    


# In[14]:


def download(link, filename):
    m3u8_file = link +"index.m3u8"
    m3u8_data = requests.get(m3u8_file)
    m3u8_master = m3u8.loads(m3u8_data.text)
    uris = [link + x['uri'] for x in m3u8_master.data['segments']]
    sess = requests.Session()
    with open(filename + ".ts", 'wb') as f:
        for uri in tqdm(uris):
            r = sess.get(uri)
            f.write(r.content)


# In[ ]:





# In[15]:


print('\n-------------------------\n')
print("Initiating Download \n")


# In[17]:


for i in range(len(DOWNLOAD_LINKS)):
    print("Downloading ep "+choices[i])
    download(DOWNLOAD_LINKS[i], suffix + "_episode_"+choices[i])


# In[ ]:


print("\nDOWNLOAD FINISHED !! ")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


input()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




