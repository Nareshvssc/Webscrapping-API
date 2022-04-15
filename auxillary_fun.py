
from bs4 import BeautifulSoup as bs
import driver_launcher
def dico_covert_to_string(information):
    """dumping the data in to excel file"""
    new_dic = {}
    for i, j in information.items():
        if type(j) == list:
            values = ''
            for k in range(len(j)):
                values += j[k] + ';'
            new_dic[i] = values
        else:
            new_dic[i] = j
    #df=pd.DataFrame([new_dic])
    #df.to_csv("web_scrapping.csv",'a')
    return new_dic

def return_page_html(url):
    driver = driver_launcher.driver_launchfun(url)
    driver.maximize_window()
    page = driver.page_source
    page_bs = bs(page,"html.parser")
    return page_bs

def return_list_of(item):
    x=[]
    for i in range(len(item)):
       x.append(item[i].text)
    return x

