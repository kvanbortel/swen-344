from flask_restful import Resource, reqparse, request
from db import library
from db.swen344_db_utils import *

class Books(Resource):
    def get(self):
        count = len(request.args)
        print(f"/books received {count} parameter(s)")
        # if there are no query parameters, return all books
        if (count == 0):
            return exec_get_all("""
                SELECT libraries.location, books.title, inventory.copies FROM inventory
                    INNER JOIN libraries ON libraries.id = inventory.library_id
                    INNER JOIN books     ON books.id = inventory.book_id
            """)
        # for each query parameter, return books where that criteria is met by looping through the colunns for matches
        # and adding "AND" when necessary
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

class ListCheckout(Resource):
    def get(self):
        """List checkout data"""
        user = request.args['user']
        books = exec_get_all("""
            SELECT books.title FROM books
                INNER JOIN checkout ON books.id = checkout.book_id
                INNER JOIN users    ON users.id = checkout.user_id
            WHERE users.name = %s
            ORDER BY title ASC
        """, (user,))
        return books
