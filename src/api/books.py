from flask_restful import Resource, reqparse, request
from db import library
from db.swen344_db_utils import *
import json

class Books(Resource):
    def get(self):
        count = len(request.args)
        print(f"/books received {count} parameter(s)")
        if (count == 0):
            return exec_get_all("""
                SELECT libraries.location, books.title, inventory.copies FROM inventory
                    INNER JOIN libraries ON libraries.id = inventory.library_id
                    INNER JOIN books     ON books.id = inventory.book_id
            """)
        else:
            sql = """ 
                SELECT libraries.location, books.title, inventory.copies FROM inventory
                    INNER JOIN libraries ON libraries.id = inventory.library_id
                    INNER JOIN books     ON books.id = inventory.book_id
                WHERE
            """
            params = []
            for i, key in enumerate(request.args.keys()):
                value = request.args[key]
                sql = f"{sql} {key}::text ILIKE %s"
                params.append(f"%{value}%")
                if (i < count - 1):
                    sql = sql + " AND "
            print(sql)
            print(params)
            result = exec_get_all(sql, params)
            return result
        
    def delete(self):
        print("Delete API call")
        print(request.data)

