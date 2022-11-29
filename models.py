from config.default import conn_mariadb


class Todo():
    def __init__(self, id: int, data: str):
        self.id = id
        self.data = data

    def get_id(self):
        return self.id

    @staticmethod
    def get(id: int):
        db = conn_mariadb()
        cursor = db.cursor()
        sql = f"SELECT * FROM TODO WHERE ID={id}"
        cursor.execute(sql)
        todo = cursor.fetchone()
        cursor.close()
        return todo

    @staticmethod
    def update(id: int, data: str):
        db = conn_mariadb()
        cursor = db.cursor()
        target_todo = Todo.get(id)
        if target_todo is None:
            return None
        sql = f"UPDATE TODO SET DATA='{data}' WHERE ID={id}"
        result = cursor.execute(sql)
        db.commit()
        cursor.close()
        return result

    @staticmethod
    def create(data: str):
        db = conn_mariadb()
        cursor = db.cursor()
        sql = f"INSERT INTO TODO VALUES(DEFAULT, '{data}')"
        cursor.execute(sql)
        db.commit()
        cursor.close()
        return True

    @staticmethod
    def delete(id: int):
        db = conn_mariadb()
        cursor = db.cursor()
        sql = f"DELETE FROM TODO WHERE ID={id}"
        result = cursor.execute(sql)
        db.commit()
        cursor.close()
        return result
