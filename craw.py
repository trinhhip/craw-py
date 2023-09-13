import requests
import os
import sys
import csv
import datetime
from bs4 import BeautifulSoup  
from urllib.parse import urlsplit

url='https://thietbiquanghoc.com.vn/san-pham-pc387638.html'
# Use urlsplit to split the URL into components
parsed_url = urlsplit(url)

# Get the base URL (scheme://netloc)
BASE_URL = parsed_url.scheme + "://" + parsed_url.netloc

# Tạo images folder để lưu 
BASE_PATH = os.getcwd()
IMG_PATH = BASE_PATH + '/images'


if not os.path.exists(IMG_PATH):
    os.makedirs(IMG_PATH)



# download ảnh về images folder
def download_img(img_link, img_name):
    response = requests.get(img_link, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(IMG_PATH, img_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)


# export data ra file .csv
current_time = datetime.datetime.now()
csv_file = f'craw-products-{current_time}.csv'
export_data = []
for i in range(1,25):
    url = f'https://thietbiquanghoc.com.vn/san-pham-pc387638.html?page={i}' 
    response = requests.get(url)
    # check nếu gửi request thành công
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tìm đến những thẻ div chứa thông tin sản phẩm
        datas = soup.find_all('div', class_='product-item')
        for data in datas:
            # download và xử lý imgs
            img_tag = data.find('img', attrs={'src': True})
            data_src_value = img_tag['data-src']
            img_name = os.path.basename(data_src_value)
            # download_img(data_src_value, img_name)

            # lấy thông tin tên, brand, giá gốc, giá khuyến mãi
            p_name = data.find('a', class_='tp_product_name').get_text()
            p_brand = data.find('span', class_='vendor-title')
            if p_brand is not None:
                p_brand = p_brand.get_text()
            else:
                p_brand = ''

            p_current_price = data.find('span', class_="current-price").get_text()
            p_original_price = data.find('span', class_="original-price")
            if p_original_price is not None:
                p_original_price = p_original_price.get_text()
            else:
                p_original_price = ''

            p_info = {'name': p_name, 'image': img_name, 'brand': p_brand, 'current_price': p_current_price, 'original_price': p_original_price}
            export_data.append(p_info)


with open(csv_file, 'w', newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames=['name', 'image', 'brand', 'current_price', 'original_price'])
    # Write the header row
    csv_writer.writeheader()

    # Write the data rows
    csv_writer.writerows(export_data)
