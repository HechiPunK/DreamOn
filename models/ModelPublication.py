from models.entities.Publication import Publication

class ModelPublication:
    @staticmethod
    def create_publication(db, content, users_id):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO publications (content, users_id) VALUES (%s, %s)"
            cursor.execute(sql, (content, users_id))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def get_publication(db):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT p.id_post, p.content, p.date, u.username 
                FROM publications p 
                LEFT JOIN users u ON p.users_id = u.id_user 
                ORDER BY p.date DESC
            """
            cursor.execute(sql)
            publications = cursor.fetchall()
            return [Publication(id_post=row[0], content=row[1], date=row[2], username=row[3]) for row in publications]
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def get_publications_by_user(db, user_id):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT p.id_post, p.content, p.date, u.username 
                FROM publications p 
                LEFT JOIN users u ON p.users_id = u.id_user 
                WHERE p.users_id = %s
                ORDER BY p.date DESC
            """
            cursor.execute(sql, (user_id,))
            publications = cursor.fetchall()
            return [Publication(id_post=row[0], content=row[1], date=row[2], username=row[3]) for row in publications]
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def get_publication_by_id(db, id):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT p.id_post, p.content, p.date, p.users_id, u.username 
                FROM publications p 
                LEFT JOIN users u ON p.users_id = u.id_user 
                WHERE p.id_post = %s
            """
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row:
                return Publication(id_post=row[0], content=row[1], date=row[2], username=row[3])
            return None
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def update_publication(db, id, new_content):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE publications SET content = %s WHERE id_post = %s"
            cursor.execute(sql, (new_content, id))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def delete_publication(db, id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM publications WHERE id_post = %s"
            cursor.execute(sql, (id,))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)