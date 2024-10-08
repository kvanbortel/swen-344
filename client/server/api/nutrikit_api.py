from flask_restful import Resource

from flask_restful import request
from flask_restful import reqparse
import json
from .swen_344_db_utils import *


class Foods(Resource):
    def get(self):
        result = exec_get_all("SELECT * FROM foods ORDER BY id ASC")
        keys = ['id', 'name', 'category_id', 'calories', 'totalFat', 'saturatedFat', 'transFat', 'protein', 'carbohydrate']
        return [dict(zip(keys, element)) for element in result]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('category_id')
        parser.add_argument('calories')
        parser.add_argument('totalFat')
        parser.add_argument('saturatedFat')
        parser.add_argument('transFat')
        parser.add_argument('protein')
        parser.add_argument('carbohydrate')
        args = parser.parse_args()
        name_count, = exec_get_one("SELECT COUNT(name) FROM foods WHERE name=%s", (args['name'],))
        if name_count:
            return 409, "Name already exists"
        sql = """
            INSERT INTO foods (name, category_id, calories, totalFat, saturatedFat, transFat, protein, carbohydrate)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        result = exec_commit(sql, (args['name'], args['category_id'], args['calories'], args['totalFat'],
                                   args['saturatedFat'], args['transFat'], args['protein'], args['carbohydrate']))
        return result

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('category_id')
        parser.add_argument('calories')
        parser.add_argument('totalFat')
        parser.add_argument('saturatedFat')
        parser.add_argument('transFat')
        parser.add_argument('protein')
        parser.add_argument('carbohydrate')
        args = parser.parse_args()
        sql = """
            UPDATE foods SET category_id=%s, calories=%s, totalFat=%s, saturatedFat=%s, transFat=%s,
            protein=%s, carbohydrate=%s
                WHERE id=%s
        """
        result = exec_commit(sql, (args['category_id'], args['calories'], args['totalFat'], args['saturatedFat'],
                                   args['transFat'], args['protein'], args['carbohydrate'], args['id']))
        return result
    
    def delete(self):
        id = request.args['id']
        exec_commit("""
            DELETE FROM foods WHERE id=%s
        """, (id,))


class Categories(Resource):
    def get(self):
        result = exec_get_all("SELECT * FROM categories ORDER BY id ASC")
        keys = ['id', 'name']
        return [dict(zip(keys, element)) for element in result]
