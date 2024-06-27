import pandas as pd
import urllib.request
import pprint as pp
from urllib.request import urlopen
from bs4 import BeautifulSoup

# List of sku numbers to run
sku_list = [

]

uniqueid_list = [

]


# Setting up the user agent
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'MyApp/1.0')]
urllib.request.install_opener(opener)

# Setting up a dataframe
mc_dict = {'Sku': [],
           'uniqueid':[], 
           'Marketing_Copy': [],
           'Product_Title': [], 
           'Img_1': [], 
           'Img_2': [], 
           'Img_3': [], 
           'Img_4': [],
           'PDF_1': [],
           'PDF_2': [],
           'Bullet_1': [],
           'Bullet_2': [],
           'Bullet_3': [],
           'Bullet_4': [],
           'Bullet_5': []
        #    'Sku_Not_Found': [],
        #    'uniqueid_not_found': []
           }

# main_df = pd.DataFrame.from_dict(mc_dict)
dict_list= []

for uniqueid, sku in zip(uniqueid_list, sku_list):
        # Extracting the page source for the sku from Signature Hardwares website and creating a soup object
        try:
            page = urlopen('https://www.signaturehardware.com/drea-wall-mount-bathroom-faucet---brushed-gold/{}.html'.format(sku))
            soup = BeautifulSoup(page, 'lxml')

            mc_dict['Sku'].append(sku)
            mc_dict['uniqueid'].append(uniqueid)
        
            # Extracting Marketing Copy and adding it to mc_dict
            try:
                main_div = soup.find("div", {"class": "col-sm-12 col-md-8 col-lg-9 px-0 short-desc"})
                marketing_copy = str(main_div.text).strip()
                mc_dict['Marketing_Copy'].append(marketing_copy)
            except:
                mc_dict['Marketing_Copy'].append('NULL')
            
            # Extracting product title
            try:
                prod_div = soup.find("div", {"class": "js-product-detail-content item-quantity-available-msg"})
                title = prod_div.find("h1", {"class": "product-name hidden-md-down"})
                title = title.text
                mc_dict['Product_Title'].append(title)
            except:
                mc_dict['Product_Title'].append('NULL')

            # Extracting pdfs
            
            try:
                href_div = soup.find("div", {"class": "resource-container"})

                hrefs = href_div.find_all("a", href=True)
                href_list = []
                
                for href in hrefs:
                    href = href.get('href')
                    href_list.append(href)
                try:
                    mc_dict['PDF_1'].append(href_list[0])
                except:
                    mc_dict['PDF_1'].append('NULL')
                
                try:
                    mc_dict['PDF_2'].append(href_list[1])
                except:
                    mc_dict['PDF_2'].append('NULL')
            except:
                mc_dict['PDF_1'].append('NULL')
                mc_dict['PDF_2'].append('NULL')

            # Extracting Images and adding them to mc_dict
            try:
                img_div = soup.find("div", {"class": "c-product-detail__images c-product-detail__images--pdp js-pdp-carousel-wraper primary-images col-12 col-lg-7 position-relative"})
                alt_srcs = img_div.find_all("img", attrs = {'srcset' : True})
                alt_srcs = list(alt_srcs)
                src_list = []
                for src in alt_srcs:
                    src = src['src']
                    if src.endswith('w=950&fmt=auto'):
                        src_list.append(src)
            except:
                mc_dict['Img_1'].append('NULL')
                mc_dict['Img_2'].append('NULL')
                mc_dict['Img_3'].append('NULL')
                mc_dict['Img_4'].append('NULL')

            try:
                mc_dict['Img_1'].append(src_list[0])
            except:
                mc_dict['Img_1'].append('NULL')
            
            try:
                mc_dict['Img_2'].append(src_list[1])
            except:
                mc_dict['Img_2'].append('NULL')

            try:
                mc_dict['Img_3'].append(src_list[2])
            except:
                mc_dict['Img_3'].append('NULL')
            
            try:
                mc_dict['Img_4'].append(src_list[3])
            except:
                mc_dict['Img_4'].append('NULL')
            
            # Extracting all specs into dictionaries and adding them to dict_list
            try:
                divs = soup.find("div", {"class": "product-specifications-inner"})
                keys = divs.find_all("span", {"class": "attribute-label"})
                values = divs.find_all("span", {"class": "attribute-value"})

                d = {'Sku': []}
                d['Sku'].append(sku)
                
                for key, value in zip(keys, values):
                    d[key.text] = value.text
                dict_list.append(d)
                pp.pprint(d)

                main_df = pd.DataFrame.from_dict(dict_list).fillna('NULL')

                # Changing the Sku column from main_df from list to a string format
                sku_col = main_df['Sku']
                new_col = []
                for sku in sku_col:
                    sku = str(sku)[2:8]
                    new_col.append(sku)

                main_df['Sku'] = new_col

            except:
                pass

            # Extracting all bullet points
            try:
                divs = soup.find("div", {"class": "col-sm-12 col-md-8 col-lg-9 px-0 long-desc"})
                bullets = divs.find_all('li')

                # Loading text from bullets into a list
                b_list = []
                for bullet in bullets:
                    bullet = bullet.text
                    b_list.append(bullet)

                # Assigning bullets to mc_dict columns
                try:
                    mc_dict['Bullet_1'].append(b_list[0])
                except:
                    mc_dict['Bullet_1'].append('NULL')

                try:
                    mc_dict['Bullet_2'].append(b_list[1])
                except:
                    mc_dict['Bullet_2'].append('NULL')

                try:
                    mc_dict['Bullet_3'].append(b_list[2])
                except:
                    mc_dict['Bullet_3'].append('NULL')

                try:
                    mc_dict['Bullet_4'].append(b_list[3])
                except:
                    mc_dict['Bullet_4'].append('NULL')

                try:
                    mc_dict['Bullet_5'].append(b_list[4])
                except:
                    mc_dict['Bullet_5'].append('NULL')
            except:
                mc_dict['Bullet_1'].append('NULL')
                mc_dict['Bullet_2'].append('NULL')
                mc_dict['Bullet_3'].append('NULL')
                mc_dict['Bullet_4'].append('NULL')
                mc_dict['Bullet_5'].append('NULL')
            
        except:
                mc_dict['Sku'].append(sku)
                mc_dict['uniqueid'].append(uniqueid)
                mc_dict['Marketing_Copy'].append('NULL')
                mc_dict['Product_Title'].append('NULL')
                mc_dict['Img_1'].append('NULL')
                mc_dict['Img_2'].append('NULL')
                mc_dict['Img_3'].append('NULL')
                mc_dict['Img_4'].append('NULL')
                mc_dict['PDF_1'].append('NULL')
                mc_dict['PDF_2'].append('NULL')
                mc_dict['Bullet_1'].append('NULL')
                mc_dict['Bullet_2'].append('NULL')
                mc_dict['Bullet_3'].append('NULL')
                mc_dict['Bullet_4'].append('NULL')
                mc_dict['Bullet_5'].append('NULL')
                
try:
    #  Creating dataframes from the dict_list and mc_dict dictionaries
    mc_df = pd.DataFrame.from_dict(mc_dict, orient='index')
    mc_df = mc_df.transpose()
    mc_df.fillna('NULL')

    # Creating a merge of the original dataframes
    final_df = pd.merge(mc_df, main_df, how='left', left_on='Sku', right_on='Sku')
    final_df.set_index('Sku', inplace=True)
    final_df.fillna('NULL', inplace=True)

    #  Writing the dataframe to an excel worksheet
    final_df.to_excel('SH_Data.xlsx', sheet_name='SH_Data')

except:
    # Creating dataframes from the dict_list and mc_dict dictionaries
    mc_df = pd.DataFrame.from_dict(mc_dict, orient='index')
    mc_df = mc_df.transpose()
    mc_df.fillna('NULL')

    #  Writing the dataframe to an excel worksheet
    mc_df.to_excel('SH_Data.xlsx', sheet_name='SH_Data')


print('Run Complete!')
