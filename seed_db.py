from config import get_db_connection

def seed_database():
    """Insert sample data into the database."""
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Check if tables exist
        cursor.execute("SHOW TABLES LIKE 'TAGS'")
        if not cursor.fetchone():
            print("Error: Tables do not exist. Please run schema.sql first to create the database tables.")
            return

        # Insert sample tags (merged genres and tags)
        cursor.execute("""
            INSERT INTO TAGS (tag_name) VALUES
            ('RPG'),
            ('Racing'),
            ('射擊'),
            ('策略'),
            ('冒險'),
            ('動作'),
            ('模擬'),
            ('益智'),
            ('恐怖'),
            ('運動'),
            ('像素風'),
            ('劇情導向'),
            ('多人'),
            ('單人'),
            ('合作'),
            ('競技'),
            ('休閒'),
            ('教育'),
            ('經典')
        """)

        # Insert sample users
        cursor.execute("""
            INSERT INTO USERS (user_id, username, gender, age) VALUES
            ('U01', 'ALEX', '男', 22),
            ('U02', 'BELLA', '女', 20),
            ('U03', 'CHRIS', '男', 25),
            ('U04', 'DIANA', '女', 28),
            ('U05', 'EDWARD', '男', 30),
            ('U06', 'FIONA', '女', 24),
            ('U07', 'GEORGE', '男', 35),
            ('U08', 'HANNAH', '女', 19),
            ('U09', 'IAN', '男', 27),
            ('U10', 'JANE', '女', 32)
        """)

        # Insert sample games
        cursor.execute("""
            INSERT INTO GAMES (game_id, title, developer) VALUES
            ('G01', 'PixelQuest', 'RetroSoft'),
            ('G02', 'CyberRacer', 'NeonLab'),
            ('G03', 'SpaceShooter', 'GalacticGames'),
            ('G04', 'StrategyEmpire', 'EmpireBuilders'),
            ('G05', 'AdventureIsland', 'IslandStudios'),
            ('G06', 'ActionHero', 'FightClub'),
            ('G07', 'SimCity', 'Maxis'),
            ('G08', 'PuzzleMaster', 'BrainGames'),
            ('G09', 'HorrorNight', 'SpookyStudios'),
            ('G10', 'SportsChamp', 'AthleticGames')
        """)

        # Insert sample gametags (now includes both genres and tags)
        cursor.execute("""
            INSERT INTO GAMETAGS (game_id, tag_id) VALUES
            ('G01', 1),  -- RPG
            ('G01', 11), -- 像素風
            ('G01', 12), -- 劇情導向
            ('G02', 2),  -- Racing
            ('G02', 13), -- 動作
            ('G03', 3),  -- 射擊
            ('G03', 13), -- 動作
            ('G04', 4),  -- 策略
            ('G04', 14), -- 多人
            ('G05', 5),  -- 冒險
            ('G05', 12), -- 劇情導向
            ('G06', 6),  -- 動作
            ('G06', 13), -- 動作
            ('G06', 14), -- 多人
            ('G07', 7),  -- 模擬
            ('G07', 15), -- 單人
            ('G07', 18), -- 休閒
            ('G08', 8),  -- 益智
            ('G08', 15), -- 單人
            ('G08', 17), -- 教育
            ('G09', 9),  -- 恐怖
            ('G09', 15), -- 單人
            ('G10', 10), -- 運動
            ('G10', 14), -- 多人
            ('G10', 16)  -- 競技
        """)

        # Insert sample reviews
        cursor.execute("""
            INSERT INTO REVIEWS (user_id, game_id, rating, comment) VALUES
            ('U01', 'G01', 4, '畫面很懷舊但好玩！'),
            ('U02', 'G01', 5, '超級喜歡這個遊戲！'),
            ('U03', 'G01', 3, '還可以，但有點難上手。'),
            ('U04', 'G02', 3, '還不錯，但有點難控制。'),
            ('U05', 'G02', 4, '賽車遊戲的經典。'),
            ('U06', 'G02', 5, '畫面和速度都很棒！'),
            ('U07', 'G03', 4, '射擊感覺很爽！'),
            ('U08', 'G03', 5, '太空主題很酷。'),
            ('U09', 'G03', 3, '控制有點難，但很有挑戰性。'),
            ('U10', 'G04', 5, '策略深度很棒。'),
            ('U01', 'G04', 4, '需要動腦，但很有趣。'),
            ('U02', 'G04', 5, '多人策略遊戲的首選。'),
            ('U03', 'G05', 4, '冒險故事很吸引人。'),
            ('U04', 'G05', 3, '畫面不錯，但劇情有點老套。'),
            ('U05', 'G05', 5, '島嶼探險很有樂趣！'),
            ('U06', 'G06', 5, '動作場面很刺激！'),
            ('U07', 'G06', 4, '英雄主題很吸引人。'),
            ('U08', 'G06', 5, '打鬥系統很流暢。'),
            ('U09', 'G07', 4, '模擬城市建設很有趣。'),
            ('U10', 'G07', 5, '經典遊戲，永遠不會過時。'),
            ('U01', 'G07', 4, '建築規劃很有挑戰。'),
            ('U02', 'G08', 3, '益智遊戲需要動腦。'),
            ('U03', 'G08', 4, '適合全家一起玩。'),
            ('U04', 'G08', 2, '有點太簡單了。'),
            ('U05', 'G09', 2, '太恐怖了，受不了。'),
            ('U06', 'G09', 1, '完全不敢玩，心理陰影。'),
            ('U07', 'G09', 3, '恐怖元素適中。'),
            ('U08', 'G10', 4, '運動遊戲很逼真。'),
            ('U09', 'G10', 5, '競技場景很刺激。'),
            ('U10', 'G10', 4, '多人對戰很有趣。')
        """)

        connection.commit()
        print("Sample data inserted successfully!")

    except Exception as e:
        connection.rollback()
        print(f"Error inserting sample data: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    seed_database()