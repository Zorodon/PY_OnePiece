import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import aiohttp,asyncio
from aiohttp import TCPConnector


def createDir(page):
    allDir = os.path.join(os.path.abspath('.'),"OP")
    isAllExist = os.path.exists(allDir)
    if not isAllExist:
        os.mkdir(allDir)
        print('-创建总目录')
    else:
        print('-总目录已存在')

    curDir = os.path.join(allDir, str(page))
    if page < 10:
        curDir = os.path.join(allDir, '00{}'.format(page))
    elif page < 100:
        curDir = os.path.join(allDir, '0{}'.format(page))

    isExist = os.path.exists(curDir)
    if not isExist:
        os.mkdir(curDir)
        print('-创建目录 {}'.format(page))
    else:
        print('-目录存在 {}'.format(page))
    return curDir

def getComicWithPage(page):
    # !!!!!!!!!!!!!!!   page缺页
    if page < 6:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page)
    elif page < 234:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 1)
    elif page < 297:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 2)
    elif page < 304:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 3)
    elif page < 310:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 4)
    elif page < 385:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 5)
    elif page < 493:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 6)
    elif page < 525:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 7)
    elif page < 637:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 8)
    elif page < 640:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 9)
    elif page == 641:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/651'
    elif page == 642:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/650'
    elif page == 643:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/652'
    elif page == 644:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/654'
    elif page == 645:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/653'
    elif page < 648:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 9)
    elif page < 650:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 10)
    elif page == 650:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/714'
    elif page < 653:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 9)
    elif page < 659:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 11)
    elif page < 661:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 3)
    elif page < 705:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 9)
    elif page < 706:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/645'
    elif page < 718:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 9)
    elif page < 723:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 10)
    elif page < 726:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 11)
    elif page < 748:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 12)
    elif page < 756:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 13)
    elif page < 774:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 14)
    elif page < 779:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 15)
    elif page < 794:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 16)
    elif page < 909:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 17)
    else:
        url = 'https://ac.qq.com/ComicView/index/id/505430/cid/{}'.format(page + 18)

    # !!!!!!!!!!!!!!!
    # page<679分辨率 617*960,
    # page<934分辨率 877*1280
    # <分辨率 1644*2400
    page_height = 1000
    page_width = 800

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(page_width, page_height)
    driver.get(url)

    print('--web加载开始')
    try:
        WebDriverWait(driver, 20, 0.5).until(
            EC.presence_of_element_located((By.ID, 'comicContain'))
        )
    except TimeoutError:
        driver.quit()
        print('--web加载失败')
    print('--web加载完成')

    print('---图片加载开始')
    # 滑动加载图片 tx自动加载下三页，隐约会有问题
    img_list = []
    web_lis = driver.find_elements(By.XPATH, "//ul[@id='comicContain']/li/img")
    for i in range(0,(page_height-2)*len(web_lis),page_height):
        js = 'document.getElementById("mainView").scrollTo(0,{})'.format(i)
        driver.execute_script(js)
        # 等待时间自己控制，和网络好坏和图片大小有关
        time.sleep(0.6)

    for web_li in web_lis:
        try:
            web_src = web_li.get_attribute("src")
        except StaleElementReferenceException:
            driver.quit()
            print('---图片加载出错\n')
            print('---重试 ', page)
            getComicWithPage(page)
            return
        img_list.append(web_src)
        if '//ac.gtimg.com/media/images/pixel.gif' in web_src:
            driver.quit()
            print('---图片未加载\n')
            print('---重试 ',page)
            getComicWithPage(page)
            return
        print('加载图片 {}'.format(web_src))
    print('---图片加载完成')
    driver.quit()

    curDir = createDir(page)
    downloadImgs(img_list,curDir)

def downloadImgs(imgs,dir):
    print('----图片下载开始')
    tasks = []
    for i in range(1,len(imgs)+1):
        filename = '{}.jpg'.format(i)
        filepath = os.path.join(dir,filename)
        task = asyncio.ensure_future(downloadUrl(imgs[i - 1], filepath))
        tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print('----图片下载完成')

async def downloadUrl(url,name):
    async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        async with session.get(url) as r:
            chunk = await r.content.read()
            with open(name,'wb') as fp:
                fp.write(chunk)
                print('下载图片 {}'.format(url))


if __name__ == '__main__':
    #######注意！！！！！！！！
    # page=23有问题,要关闭弹幕
    for i in range(1,935):
        # start = time.time()
        print('-----开始 ',i)
        getComicWithPage(i)
        print('-----完成 {}\n'.format(i))
        # end = time.time()
        # print('Time-----',end-start)
