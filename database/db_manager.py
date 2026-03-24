import pymysql
import os


class DbManager:
    def __init__(self):
        self.connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            autocommit=False
    )    

    def close(self):
        if self.connection:
            self.connection.close()

    def read_db(self, table_name : str) -> list[tuple[str, str]]:
        q = f"""
        SELECT curso, url FROM {table_name};
        """
    
        with self.connection.cursor() as cursor:
            cursor.execute(q)
            courses = cursor.fetchall()
        return courses        
   
    def db_update(self, courses : list[tuple[str, str]], table_name : str) -> None: 

        registered_courses = 0

        q = f"""
        INSERT IGNORE INTO {table_name} (
        curso, url
        )
        VALUES (%s, %s)
        """        


        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(q,courses)
                registered_courses = cursor.rowcount
            self.connection.commit()
        
            print(f"{len(courses) - registered_courses} of these courses were already stored in the database" )
            print(f"{registered_courses} new courses added to the database")
            
        except Exception as e:
            print(f"Error when updating DB{e}")
            self.connection.rollback()

    def update_course_info(self, course : dict, table_name : str):
   
        if course["informacion"] == "":
            q = f"""
            UPDATE {table_name}
            SET estado_url = %s WHERE url = %s;
            """
            info = 'no disponible'
     
        else:
            q = f"""
            UPDATE {table_name}
            SET informacion = %s WHERE url = %s;
            """
            info = course["informacion"]

            
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(q, (info, course["url"]))                    
            self.connection.commit()
            print("Course updated")
        except Exception as e:
            print(e)   