import sqlite3

conn = sqlite3.connect('scores.db')
cursor = conn.cursor()

cursor.execute('''
create table if not exists scores (
    score integer      
)
''')

total_score = 0
high_score = 0

def add_score(amount):
    global total_score
    total_score += amount

def get_score():
    global total_score
    return total_score

def set_score(s=0):
    global total_score
    total_score = s

def add_score_to_db():
    global total_score
    global cursor
    global conn
    cursor.execute('insert into scores (score) values (?)', (total_score,))
    conn.commit()

def get_high_score():
    global cursor
    global high_score
    cursor.execute('select max(score) from scores')
    high = cursor.fetchone()
    if high and high[0] is not None:
        cursor.execute('delete from scores where score < ?', (high[0],))
    return high[0] if high and high[0] is not None else 0

def close_db():
    global conn
    conn.close()
