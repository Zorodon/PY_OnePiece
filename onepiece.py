import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from multiprocessing import Pool

def createDir(page):
    allDir = os.path.join(os.path.abspath('.'),"OP")
    isAllExist = os.path.exists(allDir)
    if not isAllExist:
        os.mkdir(allDir)
        print('创建总目录')
    else:
        print('总目录已存在')

    curDir = os.path.join(allDir,str(page))
    isExist = os.path.exists(curDir)
    if not isExist:
        os.mkdir(curDir)
        print('创建目录 {}'.format(page))
    else:
        print('目录存在 {}'.format(page))
    return curDir

def getComicWithPage(page):
    if page<6:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page)
    elif page<234:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page+1)
    elif page<297:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page+2)
    else:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page+3)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(800, 1000)
    driver.get(url)

    WebDriverWait(driver, 20, 0.5).until(
        EC.presence_of_element_located((By.ID, 'comicContain'))
    )
    print('web加载完成')

    # 滑动加载图片
    img_list = []
    web_lis = driver.find_elements(By.XPATH, "//ul[@id='comicContain']/li/img")
    for i in range(len(web_lis)):
        offsetY = 1000 * i
        js = 'document.getElementById("mainView").scrollTo(0,{})'.format(offsetY)
        driver.execute_script(js)
        time.sleep(0.5)
        web_src = web_lis[i].get_attribute("src")
        img_list.append(web_src)
        print('加载图片 {}'.format(web_src))

    print('图片加载完成')
    driver.quit()

    curDir = createDir(page)
    downloadImgs(img_list,curDir)

def downloadImgs(imgs,dir):
    p = Pool(10)
    for i in range(1,len(imgs)+1):
        filename = '{}.jpg'.format(i)
        filepath = os.path.join(dir,filename)
        p.apply_async(downloadUrl(imgs[i-1],filepath),args=(i,))
    p.close()
    p.join()


def downloadUrl(url,name):
    r = requests.get(url)
    with open(name, 'wb') as code:
        code.write(r.content)
        print('下载图片 {}'.format(url))


if __name__ == '__main__':
    #######注意！！！！
    # 没有page=6，234，297
    # page=23有问题,要关闭弹幕
    for i in range(1,300):
        getComicWithPage(i)
