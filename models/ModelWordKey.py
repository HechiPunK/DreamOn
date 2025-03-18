from models.entities.WordKey import WordKey

class ModelWordKey:
    @classmethod
    def get_by_keyword(cls, db, word, type):
        try:
            cursor = db.connection.cursor()
            columna = "jungian_date" if type == "jungian" else "modern_date"
            sql = f"SELECT {columna} FROM word_key WHERE keyword = %s"
            cursor.execute(sql, (word,))
            row = cursor.fetchone()

            return row[0] if row else None
        except Exception as ex:
            raise Exception(ex)
        
    @staticmethod
    def agregar_significado(db, word, jungian_date, modern_date, user_id):
        try:
            cursor = db.connection.cursor()
            sql = """
                INSERT INTO word_key (keyword, jungian_date, modern_date, user_id)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (word, jungian_date, modern_date, user_id))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def obtener_significados_por_usuario(db, user_id):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT keyword, jungian_date, modern_date, user_id 
                FROM word_key
                WHERE user_id = %s
            """
            cursor.execute(sql, (user_id,))
            significados = cursor.fetchall()
            return [{"word": row[0], "jungian_date": row[1], "modern_date": row[2]} for row in significados]
        except Exception as ex:
            raise Exception(ex)