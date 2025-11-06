from config import get_db_connection

class Database:
    def __init__(self):
        self.connection = get_db_connection()

    def close(self):
        self.connection.close()

    # USERS operations
    def add_user(self, user_id, username, gender, age):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO USERS (user_id, username, gender, age) VALUES (%s, %s, %s, %s)",
                       (user_id, username, gender, age))
        self.connection.commit()
        cursor.close()

    def get_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM USERS")
        users = cursor.fetchall()
        cursor.close()
        return users

    # GAMES operations
    def add_game(self, game_id, title, developer, tag_names):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO GAMES (game_id, title, developer) VALUES (%s, %s, %s)",
                       (game_id, title, developer))
        for tag_name in tag_names:
            tag_id = self.get_tag_id(tag_name)
            if not tag_id:
                tag_id = self.add_tag(tag_name)
            cursor.execute("INSERT INTO GAMETAGS (game_id, tag_id) VALUES (%s, %s)",
                           (game_id, tag_id))
        self.connection.commit()
        cursor.close()

    def get_games(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT g.game_id, g.title, g.developer, GROUP_CONCAT(t.tag_name SEPARATOR ', ') as tags
            FROM GAMES g
            LEFT JOIN GAMETAGS gt ON g.game_id = gt.game_id
            LEFT JOIN TAGS t ON gt.tag_id = t.tag_id
            GROUP BY g.game_id, g.title, g.developer
        """)
        games = cursor.fetchall()
        cursor.close()
        return games

    # TAGS operations
    def add_tag(self, tag_name):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO TAGS (tag_name) VALUES (%s)", (tag_name,))
        self.connection.commit()
        tag_id = cursor.lastrowid
        cursor.close()
        return tag_id

    def get_tags(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM TAGS")
        tags = cursor.fetchall()
        cursor.close()
        return tags

    def get_tag_id(self, tag_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT tag_id FROM TAGS WHERE tag_name = %s", (tag_name,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def get_games_by_tag(self, tag_name):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT g.game_id, g.title, g.developer, AVG(r.rating) as avg_rating
            FROM GAMES g
            JOIN GAMETAGS gt ON g.game_id = gt.game_id
            JOIN TAGS t ON gt.tag_id = t.tag_id
            LEFT JOIN REVIEWS r ON g.game_id = r.game_id
            WHERE t.tag_name = %s
            GROUP BY g.game_id, g.title, g.developer
        """, (tag_name,))
        games = cursor.fetchall()
        cursor.close()
        return games

    # REVIEWS operations
    def add_review(self, user_id, game_id, rating, comment):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO REVIEWS (user_id, game_id, rating, comment) VALUES (%s, %s, %s, %s)",
                       (user_id, game_id, rating, comment))
        self.connection.commit()
        cursor.close()

    def get_reviews_by_game(self, game_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT r.review_id, u.username, r.rating, r.comment, r.added_date
            FROM REVIEWS r
            JOIN USERS u ON r.user_id = u.user_id
            WHERE r.game_id = %s
            ORDER BY r.added_date DESC
        """, (game_id,))
        reviews = cursor.fetchall()
        cursor.close()
        return reviews

    def get_games_average_rating(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT g.game_id, g.title, g.developer, AVG(r.rating) as avg_rating
            FROM GAMES g
            LEFT JOIN REVIEWS r ON g.game_id = r.game_id
            GROUP BY g.game_id, g.title, g.developer
            ORDER BY avg_rating DESC
        """)
        games = cursor.fetchall()
        cursor.close()
        return games
