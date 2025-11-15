# ----- USERS ----- #
SQL_SELECT_ALL_USER = """
SELECT id, username, password
FROM users
"""


SQL_SELECT_USER_BY_ID="""
SELECT id
FROM users
WHERE id=?
"""

SQL_INSERT_USER ="""
INSERT INTO users(username,password)
VALUES (?,?)
"""

SQL_UPDATE_USER ="""
UPDATE users
SET username=?, password=?
Where id=?
"""

SQL_DELETE_USER ="""
DELETE FROM users
WHERE id=?
""" 


# ----- EXPENSES ----- #
SQL_SELECT_ALL_EXPENSES = """
SELECT *
FROM expenses
"""


SQL_SELECT_EXPENSES_BY_ID="""
SELECT *
FROM expenses
WHERE user_id=?
"""

SQL_INSERT_EXPENSES ="""
INSERT INTO expenses( id, title, description, amount, date, category)
VALUES (?,?,?,?,?,?)
"""

SQL_UPDATE_EXPENSES ="""
UPDATE expenses
SET id=?, title=?, description=?, amount=?, date=?, category=?
Where user_id=?
"""

SQL_DELETE_EXPENSES ="""
DELETE FROM expenses
WHERE id=?
"""