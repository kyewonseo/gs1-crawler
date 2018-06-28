from urllib import parse
from scrapy import Spider, Request
# from __future__ import print_function
from goodlens_product_db.products import Products
from goodlens_product.product_common import ProductCommon
from pprint import pprint
from gs1_crawler.foods import Foods

import gs1_crawler.utils
import re

api_instance = Products()
foods = Foods()

class KoreanNet(Spider):
  def __init__(self):
    self.domain = "http://gs1.koreannet.or.kr"
    self.sub_domain = "/pr/"

  def start_requests(self):
    yield Request(url=self.domain)

  def parse(self, response):

    food_id_list = gs1_crawler.utils.read_food_id_list_file('food_id_list')
    print('food_id_list=>',food_id_list)

    for food_id in food_id_list:
      barcode = foods.get_barcode_by_food_id(food_id)
      if barcode != None:
        yield Request(url=self.domain + self.sub_domain + barcode, callback=self.sub_parse)


  def sub_parse(self, response):
    tmp_image_labels = []
    for num in range(0, 3):
      image = response.css("div.productview > div.pv_title > div.pv_img > ul.btn_img > li > a::attr('onclick')")[
        num].extract()
      product_image_url = self.parse_product_image_url(image)

      if product_image_url != None:
        tmp_image_labels.append(product_image_url)

    # print(tmp_image_labels)

    item_key_list = []
    item_value_list = []

    item_keys = response.css("div.productview > div.pv_title > table.pv_info > tbody > tr > th").extract()
    item_values = response.css("div.productview > div.pv_title > table.pv_info > tbody > tr > td").extract()

    for num in range(len(item_keys)):
      item_key_list.append(self.trim_html_table_tag(item_keys[num]))

    for num in range(len(item_values)):
      item_value_list.append(self.trim_html_table_tag(item_values[num]))

    dictionary = dict(zip(item_key_list, item_value_list))
    # print(dictionary)

    tmp_kan = dictionary.get('KAN 상품분류')
    tmp_standard_table = response.css(
      "div.productview > div.contents > table.detail_info > tbody > tr > td::text").extract()
    tmp_standard_length_list = tmp_standard_table[0]
    standard_length_list = self.split_standard_length(tmp_standard_length_list)

    tmp_weight_pure = tmp_standard_table[1]
    tmp_weight_total = tmp_standard_table[2]
    # tmp_create_date = tmp_standard_table[3]

    product_name = response.css("div.productview > div.pv_title > h3::text")[0].extract()
    image_labels = tmp_image_labels
    gtin = dictionary.get('바코드(GTIN)')
    kan_code = dictionary.get('KAN 상품분류코드')
    kan = self.trim_kan_classify_tag(tmp_kan)
    manufacturer = dictionary.get('제조사/생산자')
    manufacture_seller = dictionary.get('판매자')
    company_address = dictionary.get('회사주소/도로명주소')
    phone_number = dictionary.get('대표전화')
    width = standard_length_list[0]
    depth = standard_length_list[1]
    height = standard_length_list[2]
    standard_length_unit = standard_length_list[3]
    weight_pure = self.trim_weight_tag(tmp_weight_pure)
    weight_total = self.trim_weight_tag(tmp_weight_total)
    weight_unit = self.get_weight_unit(tmp_weight_total)

    # product_id = foods.get_food_id_by_barcode(gtin)
    # print('product_name=>',product_name)
    # print('gtin=>',gtin)
    # print('product_id=>',product_id)

    product_common = ProductCommon()
    product_common.product_id = foods.get_food_id_by_barcode(gtin)
    product_common.product_name = product_name
    product_common.image_labels = image_labels
    product_common.gtin = gtin
    product_common.kan_code = kan_code
    product_common.kan = kan
    product_common.manufacturer = manufacturer
    product_common.manufacture_seller = manufacture_seller
    product_common.company_address = company_address
    product_common.phone_number = phone_number
    product_common.width = width
    product_common.depth = depth
    product_common.height = height
    product_common.standard_length_unit = standard_length_unit
    product_common.weight_pure = weight_pure
    product_common.weight_total = weight_total
    product_common.weight_unit = weight_unit

    try:
      print(product_common)
      api_response = api_instance.add_product_common(product_common)
      if api_response is not None:
        if 'upserted' in api_response:
          product_id = api_response['product_id']
          print(api_response)
      pprint(api_response)
    except Exception as e:
      print("Exception when calling Products->add_product_common: %s\n" % e)

  def parse_product_image_url(self, product_image):
    image = product_image.split('\'')[1]
    try:
      image_url = self.domain[:-4] + image
      fileNm = parse.parse_qs(parse.urlparse(image_url).query).get('fileNm')

      if fileNm != None:
        return image_url

    except Exception as e:
      print(e)


  def trim_html_table_tag(self, item):
    pattern = re.compile(r'(<|</)(th|td)>')
    str = re.sub(pattern,'',item)
    # print(str)

    return str

  def trim_kan_classify_tag(self, kan):
    pattern = re.compile(r'\s&gt;\s')
    str = re.sub(pattern, '>', kan)
    # print(str)

    return str

  def split_standard_length(self, standard_length):

    unit_pattern = re.compile(r'[^(|a-z|)]')
    unit = re.sub(unit_pattern, '', standard_length)[3:][:-1]
    # print(unit)

    standard_length = standard_length[:-5]
    pattern = re.compile(r'\sx\s')
    str_list = re.split(pattern, standard_length)
    str_list.append(unit)
    # print(str_split)

    return str_list

  def trim_weight_tag(self, weight):
    pattern = re.compile(r'\D')
    str = re.sub(pattern, '', weight)
    # print(str)

    return str

  def get_weight_unit(self, weight):
    unit_pattern = re.compile(r'[^(|a-z|)]')
    unit = re.sub(unit_pattern, '', weight)[1:][:-1]
    # print(unit)

    return unit