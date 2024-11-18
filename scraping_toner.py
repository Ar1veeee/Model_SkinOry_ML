from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

url= 'https://www.tokopedia.com/search?navsource=home&search_id=2024111515421226C3BD593057A32DB7IV&shop_tier=2&source=universe&srp_component_id=04.06.00.00&st=product&q=toner%20skincare'

driver = webdriver.Chrome()
driver.get(url)

data=[]
for i in range(10):
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#zeus-root")))
    time.sleep(2)

    for j in range(23):
        driver.execute_script("window.scrollBy(0,250)")
        time.sleep(1)

    driver.execute_script("window.scrollBy(50,0)")
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source,"html.parser")
    for item in soup.findAll('div',class_='css-5wh65g'):
        gambar_produk = item.find('img')['src']
        nama_produk = item.find('div',class_='_6+OpBPVGAgqnmycna+bWIw==').text 

        harga_produk = 'No price'
        harga_tag = item.find('div', class_='XvaCkHiisn2EZFq0THwVug==')
        if harga_tag:
            harga_item = harga_tag.find('div', class_='_67d6E1xDKIzw+i2D2L0tjw== t4jWW3NandT5hvCFAiotYg==')
            if harga_item:
                harga_produk = harga_item.text
        
        rtg = item.findAll('span',class_='_9jWGz3C-GX7Myq-32zWG9w==')
        if len(rtg)>0:
            rating = item.find('span', class_='_9jWGz3C-GX7Myq-32zWG9w==').text
        else:
            rating ='None'
        
        tjl = item.findAll('span',class_='se8WAnkjbVXZNA8mT+Veuw==')
        if len(tjl)>0:
            terjual = item.find('span', class_='se8WAnkjbVXZNA8mT+Veuw==').text
        else:
            terjual ='None'    
        link_produk = item.find('a')['href']

        data.append(
            (gambar_produk,nama_produk,harga_produk,rating,terjual,link_produk)
        )


    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,"button[aria-label^='Laman berikutnya']")
    time.sleep(3)

df = pd.DataFrame(data, columns=['Gambar Produk','Nama Produk','Harga Produk','Rating Produk','Terjual','Link Produk'])
print (df)

df.to_csv('TokpedToner.csv', index= False)


