from gs1_crawler.foods import Foods

foods = Foods()

def read_barcode_list():
    barcodes = []
    food_id_list = read_food_id_list_file('food_id_list')
    for food_id in food_id_list:
        barcode = foods.get_barcode_by_food_id(food_id)

        if barcode != None:
            # print('@@@@@', barcode)
            barcodes.append(barcode)
    print(barcodes)

    return barcodes

  # test_barcode_list = ['8801007052755', '8801069222998']
  # return test_barcode_list

def test_food_id_list():
  test_food_id_list = [
                       '10000005',
                       '10000017',
                       '10000018',
                       '10000019',
                       '10000020',
                       '10000021',
                       '10000022',
                       '10000023']
  return test_food_id_list

def test_get_barcode():
  barcodes = []

  # food_id_list = read_food_id_list_file('food_id_list')
  # for food_id in food_id_list:
  #   barcode = foods.get_barcode_by_food_id(food_id)
  #   print(barcode)
  #   barcodes.append(barcode)
  # print('###',barcodes)

  # foods.get_food_id_by_barcode('8801007052755')

def read_food_id_list_file(fileName):

  with open(fileName + '.txt', 'rt') as f:
    food_id_list = f.read().splitlines()
    return food_id_list