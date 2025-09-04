from utils.connection import conn

def init_db():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE  IF NOT EXISTS users(
                user_id VARCHAR(225) PRIMARY KEY,
                user_name VARCHAR(225),
                role VARCHAR(225)
    )""") 
    conn.commit()
 
    cursor.execute("""CREATE TABLE IF NOT EXISTS contracts (
        contract_type VARCHAR(225) NOT NULL,
        contract_name VARCHAR(225),
        contract_id   VARCHAR(225) NOT NULL,
        user_id VARCHAR(225),
        inserted datetime,
        updated datetime,
        PRIMARY KEY (contract_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""")
    conn.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS clauses (
        contract_id   VARCHAR(225) NOT NULL,
        clause_id   VARCHAR(225) NOT NULL ,
        clause_heading VARCHAR(225),
        clause  TEXT,
        PRIMARY KEY (clause_id),
        FOREIGN KEY(contract_id) REFERENCES contracts(contract_id)
    )""")


    conn.commit()


# init_db()