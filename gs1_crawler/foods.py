from gs1_crawler.database import DataBase


class Foods(DataBase):
  def __init__(self):
    super().__init__()
    self.foods = self.db.foods

  def add_food(self, food):
    try:
      r = self.foods.update_one(food,
                              {"$set": food},
                              upsert=True)

    except Exception as e:
      print(e)


  def get_barcode_by_food_id(self, food_id):

    query = {"foodId": food_id}
    try:
      r = self.foods.find_one(query)
      # print(r['barcode'])
      # if r['barcode'] != None:
      return r['barcode']
    except Exception as e:
      print(e)

  def get_food_id_by_barcode(self, barcode):
    query = {"barcode": barcode}
    try:
      r = self.foods.find_one(query)
      # print(r['foodId'])
      return r['foodId']
    except Exception as e:
      print(e)



