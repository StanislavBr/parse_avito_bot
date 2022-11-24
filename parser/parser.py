from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import re,csv,os,random,string
from twocaptcha import TwoCaptcha
import cv2,pytesseract



options = Options()
options.add_argument('--user-data-dir=/home/sbaranov/.config/google-chrome/')
options.add_argument('--profile-directory=Default')
driver = webdriver.Chrome(executable_path = "/home/sbaranov/development/freelanse/bor_parse/chrome/chromedriver", options=options )




def parse(url,context=None):
    page = get_all_num_page(url)
    print(f'КОЛИЧЕСТВО СТРАНИЦ {str(page)}')
    links_all_page=get_links_all(link=url,coun=page)
    links_all_object=get_lisks_object(link=links_all_page)
    data=[]
    for i in links_all_object:
        try:
            data_num_src=get_data(i)
            print(data_num_src)
            data.append(data_num_src)
        except:
            continue
    print(data)
    print('НАЧИНАЮ ЗАПИСЬ')
    file=write_file(data=data)
    print('ЗАКОНЧИЛ ЗАПИСЬ')
    return file


def get_all_num_page(url):
    list_num_page=[]
    driver.get(url=url)
    time.sleep(1)
    paginate=driver.find_elements(By.CLASS_NAME,'pagination-item-JJq_j')
    for i in paginate:
        list_num_page.append(i.get_attribute('data-marker'))
    page=str(list_num_page[-2])
    page_curr=get_number_page(page)
    return int(page_curr)+1


def get_number_page(page):
    num=re.search(r'page[\(].{,20}.[\)]',page).group()[5:-1]
    return num


def get_links_all(link,coun):
    links_all_page=[]
    for i in range(1,int(coun)): 
    # for i in range(1,2): TEST
        link_curr= link+f'&p={i}'
        links_all_page.append(link_curr)
    return links_all_page


def get_lisks_object(link):
    links_obj=[]
    for b in link:
        driver.get(url=b)
        time.sleep(1)
        links_ob=driver.find_elements(By.CLASS_NAME,'iva-item-titleStep-pdebR')
        for a in links_ob:
            el=a.find_element(By.TAG_NAME,'a')
            links_one_object=el.get_attribute('href')
            print(links_one_object)
            links_obj.append(links_one_object)
    return links_obj


def get_data(link):
    name = get_name(link=link)
    number = get_number(link=link)
    return number, name


def get_number(link):
    driver.get(url=link)
    time.sleep(1)
    xpath_list=['/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div/span/span/div/div/button','/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div[1]/span/span/div/div/button','/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div[1]/span/span/div/div/button']
    for i in xpath_list:
        try:
            button_num=driver.find_element(By.XPATH,f'{i}')
            if button_num != None:
                break
        except:
            continue
    button_num.click()
    time.sleep(1)
    try:
        close=driver.find_element(By.CLASS_NAME,'popup-close-XlIOw')
    except:
        close=driver.find_element(By.XPATH,'/html/body/div[11]/div/button')
    close.click()
    time.sleep(1)
    try:
        number_img=driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div[1]/span/span/div/div/button/span/img')
    except:
        number_img=driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div/div[1]/span/span/div/div/button/span/img')
    number_img_link=number_img.get_attribute('src')
    number=get_number_for_link(number_img_link)
    return number


def get_number_for_link(link):
    try:
        os.remove('/home/sbaranov/development/freelanse/bor_parse/screen/screen.jpg')
    except:
        driver.get(url=link)
        driver.save_screenshot('screen/screen.jpg')
        img=cv2.imread('/home/sbaranov/development/freelanse/bor_parse/screen/screen.jpg')
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        number=pytesseract.image_to_string(image=img,config='')
        os.remove('/home/sbaranov/development/freelanse/bor_parse/screen/screen.jpg')
    return number


def write_file(data):
    rand_str=generate_random_string(8)
    name = f'/home/sbaranov/development/freelanse/bor_parse/parse{rand_str}.csv'
    with open(f'parse{rand_str}.csv', "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    return name

    
def get_name(link):
    try:
        name=get_name_current(link)
    except:
        name=get_name_not_curr(link=link)
    return name


def get_name_current(link):
    driver.get(url=link)
    time.sleep(1)
    xpath_list=['/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[3]/div[2]','/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[2]','/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/a/span','/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/a/span','/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/a/span']
    for i in xpath_list:
        try:
            obj_name=driver.find_element(By.XPATH,f'{i}')
            name=obj_name.text
            if name != None:
                break
        except:
            continue
    return name


def get_name_not_curr(link):
    driver.get(url=link)
    time.sleep(1)
    xpath_list=['/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/h1/span','/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div/div[1]/h1/span']
    for i in xpath_list:
        try:
            obj_name=driver.find_element(By.XPATH,f'{i}')
            name=obj_name.text
            print(name)
            if name != None:
                break
        except:
            continue
    return name

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

