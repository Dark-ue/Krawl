from sqlcipher3 import dbapi2

class Database:
    def __init__(self, db, passphrase):
        self.db = db
        self.conn = dbapi2.connect(db)

        self.cursor = self.conn.cursor()
        self.cursor.execute(f"PRAGMA key = '{passphrase}';")

        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()

        # profiles table
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS my_profile (
                username TEXT PRIMARY KEY,
                public_key TEXT NOT NULL,
                private_key TEXT NOT NULL
            )
            '''
        )

        # contacts table
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS my_contacts (
                peer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                peer_username TEXT UNIQUE,
                known_ip TEXT,
                public_key TEXT
            )
            '''
        )

        # messages table
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                sender TEXT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                FOREIGN KEY (contact_id) REFERENCES my_contacts (peer_id)
            )
            '''
        )

        self.conn.commit()

    def add_contact(self, username, ip_address, public_key="None"):
        try:
            cursor = self.conn.cursor()
            sql = '''
            INSERT INTO my_contacts (peer_username, known_ip, public_key)
            VALUES (?, ?, ?)
            '''
            cursor.execute(sql, (username, ip_address, public_key))
            self.conn.commit()
            return True
        except dbapi2.IntegrityError:
            print(f"Contact {username} already exists.")
            return False
        except Exception as e:
            print(f"Database error while saving contact: {e}")
            return False
