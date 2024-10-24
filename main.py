import requests
from bs4 import BeautifulSoup
import xlwt
import os
from datetime import datetime
import imghdr

dynamic_site_urls = ["https://onestophalal.com/pages/fresh-meat", "https://onestophalal.com/collections/halal-jerky"]
frozen_site = "https://onestophalal.com/pages/deli-frozen"
products = []
section_id = 1

def get_record(url):
    global section_id
    try:
        download_url = ""
        nutrition = ""
        certification = ""
        rating = ""
        rating_num = ""
        
        response = requests.get(url)
        soup_product = BeautifulSoup(response.text, 'html.parser')
        name = soup_product.find('h1', itemprop="name").get_text(strip=True)
        price = soup_product.find('span', class_='money').get_text(strip=True)
        parent_div = soup_product.find('div', id='tabs-2')
        description = parent_div.get_text(strip=True)
        
        nutrition_div = soup_product.find('div', id='tabs-3')
        if nutrition_div:
            nutrition = nutrition_div.get_text(strip=True)
        
        certification_div = soup_product.find('div', id='tabs-4')
        if certification_div:
            certification = certification_div.get_text(strip=True)
        else:
            certification = nutrition
            nutrition = ""
        
        rating_div = soup_product.find('div', class_='loox-rating')
        if rating_div:
            rating = rating_div["data-rating"]
            rating_num = rating_div["data-raters"]
        
        image_tag = soup_product.find('a', class_='image-slide-link')
        if 'href' in image_tag.attrs:
            image_url = "https:"+image_tag['href']
            if(image_url):
                try:
                    responseImage = requests.get(image_url)
                    image_type = imghdr.what(None, responseImage.content)
                    if responseImage.status_code == 200:
                        img_url = "products/"+current_time+"/images/"+prefix+str(section_id)+'.'+image_type
                        with open(img_url, 'wb') as file:
                            file.write(responseImage.content)
                            download_url = img_url
                    # download_url = "products/"+current_time+"/images/"+prefix+str(section_id)+'.'+"jpg"
                except Exception as e:
                    print(e)
        
        else:
            image_url = 'No image found'

        category_source = soup_product.find('ol', class_='breadcrumb')
        li_tags = category_source.find_all('li')

        # Get the content of the second <li> tag
        if len(li_tags) > 1:  # Check if there are at least 2 <li> tags
            category = li_tags[1].get_text(strip=True)
        else:
            category = "No Category"
        # Add product details to the list
        record = [
            str(section_id),
            "https://onestophalal.com",
            url,
            "One Stop Halal",
            category,
            description,
            name,
            "",
            "",
            price,
            download_url,
            image_url,
            "",
            "",
            rating,
            rating_num,
            "766 Gladys Avenue, Los Angeles, CA 90021",
            "+1(833)425-2566",
            "",
            "",
            "",
            nutrition,
            certification,
        ]
        
        products.append(record)
        print(record)
        
        section_id = section_id + 1
    except:
        print("Cannot find the product")

# Step 1: Function to scrape product info from One Stop Halal
def scrape_onestophalal(current_time, prefix):
    response = requests.get("https://onestophalal.com")
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    global section_id
    nav = soup.find("nav", class_="wsmenu")

    sub_lists = nav.find_all('ul', class_="wsmenu-sub-list")

    sub_menues = nav.find_all('ul', class_="wsmenu-submenu")

    for list in sub_lists:
        ul_lists = list.find_all('ul')
        for ul in ul_lists:
            li_lists = ul.find_all('li')
            for li in li_lists:
                urls.append('https://onestophalal.com' + li.find('a')['href'])
    for menu in sub_menues:
        li_lists = menu.find_all('li')
        for li in li_lists:
            urls.append('https://onestophalal.com' + li.find('a')['href'])
            print('https://onestophalal.com' + li.find('a')['href'])
            
    for dynamic_site in dynamic_site_urls:
        response = requests.get(dynamic_site)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', class_='hlal_123')

        for link in links:
            get_record("https://onestophalal.com" + link["href"])
        
        collection_links = soup.find_all('g', class_='hlal_1234')
        for link in collection_links:
            get_record(link["onclick"])
    # site
    response = requests.get(frozen_site)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', class_='frozen_page')

    for link in links:
        get_record("https://onestophalal.com" + link["href"])

    for url in urls:
        last_slash_index = url.rfind('/')

        category = url[last_slash_index + 1:]  # +1 to exclude the '/'
        # Send a request to the website
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize an empty list to store product information
        content = soup.find_all('div', class_="main_box")
        # Example: Assuming each product is in a div with class 'product-item'
        for product in content:
            try:
                download_url = ""
                nutrition = ""
                certification = ""
                rating = "",
                rating_num = ""
                
                name = product.find('h5').get_text(strip=True)
                price = product.find('span', class_='money').get_text(strip=True)
                description_url = 'https://onestophalal.com' + product.find('a')['href']
                response = requests.get(description_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                parent_div = soup.find('div', id='tabs-2')
                description = parent_div.get_text(strip = True)
                
                nutrition_div = soup.find('div', id='tabs-3')
                if nutrition_div:
                    nutrition = nutrition_div.get_text(strip=True)
                
                certification_div = soup.find('div', id='tabs-4')
                if certification_div:
                    certification = certification_div.get_text(strip=True)
                else:
                    certification = nutrition
                    nutrition = ""
                    
                rating_div = soup.find('div', class_='loox-rating')
                if rating_div:
                    rating = rating_div["data-rating"]
                    rating_num = rating_div["data-raters"]
                
                image_tag = product.find('img', class_='lazy')
                if 'src' in image_tag.attrs:
                    image_url = "https:"+image_tag['src']
                elif 'data-src' in image_tag.attrs:
                    image_url = "https:"+image_tag['data-src']
                else:
                    image_url = 'No image found'
                    
                if(image_url):
                    try:
                        responseImage = requests.get(image_url)
                        image_type = imghdr.what(None, responseImage.content)
                        if responseImage.status_code == 200:
                            img_url = "products/"+current_time+"/images/"+prefix+str(section_id)+'.'+image_type
                            with open(img_url, 'wb') as file:
                                file.write(responseImage.content)
                                download_url = img_url
                        # download_url = "products/"+current_time+"/images/"+prefix+str(section_id)+'.'+"jpg"
                    except Exception as e:
                        print(e)

                category_source = soup.find('ol', class_='breadcrumb')
                li_tags = category_source.find_all('li')

                # Get the content of the second <li> tag
                if len(li_tags) > 1:  # Check if there are at least 2 <li> tags
                    category = li_tags[1].get_text(strip=True)
                else:
                    category = "No Category"
                # Add product details to the list
                record = [
                    str(section_id),
                    "https://onestophalal.com",
                    "https://onestophalal.com" + product.find('a')['href'],
                    "One Stop Halal",
                    category,
                    description,
                    name,
                    "",
                    "",
                    price,
                    download_url,
                    image_url,
                    "",
                    "",
                    rating,
                    rating_num,
                    "766 Gladys Avenue, Los Angeles, CA 90021",
                    "+1(833)425-2566",
                    "",
                    "",
                    "",
                    nutrition,
                    certification,
                ]
                
                products.append(record)
                print(record)
                
                section_id = section_id + 1
            except:
                print("Cannot find the product")
    
    return products

# Step 3: Main function
if __name__ == '__main__':
    # Scrape the product data
    titleData = ["id","Store page link", "Product item page link", "Store_name", "Category", "Product_description", "Product Name", "Weight/Quantity", "Units/Counts", "Price", "image_file_names", "Image_Link", "Store Rating", "Store Review number", "Product Rating", "Product Review number", "Address", "Phone number", "Latitude", "Longitude", "Description Detail", "Nutrition & Info", "Halal Certification"]
    widths = [10,50,50,60,45,70,35,25,25,20,130,130,30,30,30,30,60,50,60,60,80,80,80]
    style = xlwt.easyxf('font: bold 1; align: horiz center')
    products = []

    if(not os.path.isdir("products")):
        os.mkdir("products")

    now = datetime.now()
    current_time = now.strftime("%m-%d-%Y-%H-%M-%S")
    prefix = now.strftime("%Y%m%d%H%M%S%f_")
    os.mkdir("products/"+current_time)
    os.mkdir("products/"+current_time+"/images")
    
    records = scrape_onestophalal(current_time, prefix)
    
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Sheet1')

    for col_index, value in enumerate(titleData):
        first_col = sheet.col(col_index)
        first_col.width = 256 * widths[col_index]  # 20 characters wide
        sheet.write(0, col_index, value, style)
        
    for row_index, row in enumerate(records):
        for col_index, value in enumerate(row):
            sheet.write(row_index+1, col_index, value)

    # Save the workbook
    workbook.save("products/"+current_time+"/products.xls")
    
    
