
if_not_exists = '''
                                    CREATE TABLE IF NOT EXISTS usersdata(
                                        uid INTEGER PRIMARY KEY AUTOINCREMENT,
                                        username TEXT,
                                        password TEXT
                                    );
                                    CREATE TABLE IF NOT EXISTS userstasks(
                                        username TEXT,
                                        tid INTEGER PRIMARY KEY AUTOINCREMENT,
                                        date TIMESTAMP,
                                        content TEXT,
                                        steps TEXT,
                                        status TEXT,
                                        status_time TIMESTAMP
                                        );
                                '''
# con = sqlite3.connect("database/database.db")
# cur = db.cursor()
# username_container = [username]
# user_info = [username, password]
# user_input = (username, password)