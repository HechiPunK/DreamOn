from .entities.User import User

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_user, username, password FROM users 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password))
                return user 
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_user, username, mail FROM users WHERE id_user = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                return User(row[0], row[1], None, row[2])  
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def register(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_user FROM users WHERE username = %s OR mail = %s"
            cursor.execute(sql, (user.username, user.mail))
            if cursor.fetchone() != None:
                return False 
            hashed_password = User.hash_password(user.password)
            sql = """INSERT INTO users (username, mail, password) VALUES (%s, %s, %s)"""
            print(f"Ejecutando consulta: {sql} con los valores {user.username}, {user.mail}, {hashed_password}")
            cursor.execute(sql, (user.username, user.mail, hashed_password))
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
           
    # @classmethod
    # def update_profile(cls, db, user):    
    #     try:
    #         cursor = db.connection.cursor()
    #         sql = """
    #             UPDATE users 
    #             SET profile_pic = %s, description = %s, phone = %s, address = %s 
    #             WHERE id_sesion = %s
    #         """
    #         params = (user.profile_pic, user.description, user.phone, user.address, user.id)
    #         print(f"Ejecutando SQL: {sql} con parámetros {params}")  # Debug
    #         cursor.execute(sql, params)
    #         db.connection.commit()
    #         return True
    #     except Exception as ex:
    #         db.connection.rollback()
    #         print(f"Error en update_profile: {str(ex)}")  # Debug
    #         raise Exception(ex)