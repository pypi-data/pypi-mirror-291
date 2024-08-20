from . import dbUtils


def executeCommand(self):
    query = '''UPDATE users
    SET
    username = "user259"
    WHERE 1=1
    ;
    '''
    return dbUtils.renderSqlQuery(self, query, vals=None)
# executeCommand()


def createAdminTable(self):
    query = '''CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hashed VARCHAR(255) NOT NULL,
    password_salt VARCHAR(255) NOT NULL,

    created_at DATETIME DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at DATETIME DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
    );
    '''
    return dbUtils.renderSqlQuery(self, query, vals=None)


def createPasswordsTable(self):
    query = '''CREATE TABLE IF NOT EXISTS passwords(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) NOT NULL,
    pnumber INTEGER UNIQUE NOT NULL,
    password_hashed TEXT NOT NULL,
    password_salt TEXT NOT NULL,

    created_at DATETIME DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at DATETIME DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
    );
    '''
    return dbUtils.renderSqlQuery(self, query, vals=None)


def insertAdminData(self, username, passwordSalt, passwordHashed):
    sqlQuery = f'''INSERT INTO users(
    username,
    password_salt,
    password_hashed
    )
    VALUES(
    "{username}",
    "{passwordSalt}",
    "{passwordHashed}"
    );
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def insertPasswordData(self, pnumber, username, passwordSalt, passwordHashed):
    sqlQuery = f'''INSERT INTO passwords(
    username,
    pnumber,
    password_salt,
    password_hashed
    )
    VALUES(
    "{username}",
    "{pnumber}",
    "{passwordSalt}",
    "{passwordHashed}"
    );
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def updateAdminData(self, username, passwordSalt, passwordHashed):
    sqlQuery = f'''UPDATE users
    SET
    password_salt = "{passwordSalt}",
    password_hashed = "{passwordHashed}"
    WHERE
    username = "{username}";
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def updatePasswordData(self, username, pnumber, passwordSalt, passwordHashed):
    sqlQuery = f'''UPDATE passwords
    SET
    username = "{username}",
    password_salt = "{passwordSalt}",
    password_hashed = "{passwordHashed}"
    WHERE
    pnumber = "{pnumber}"
    ;
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def fetchAdminData(self, username=None):
    sqlQuery = f'''
    SELECT
    username,
    password_salt AS passwordSalt,
    password_hashed AS passwordHashed
    FROM users
    WHERE username = "{username}";
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def fetchAllAdminData(self):
    sqlQuery = f'''
    SELECT
    username,
    password_salt AS passwordSalt,
    password_hashed AS passwordHashed
    FROM users
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def fetchPasswordCount(self, username):
    sqlQuery = f'''
    SELECT
    COUNT(*) as count
    FROM passwords
    WHERE username = '{username}'
    ;
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def fetchPasswordData(self, username, pnumber):
    sqlQuery = f'''
    SELECT
    username,
    pnumber,
    password_salt AS passwordSalt,
    password_hashed AS passwordHashed
    FROM passwords
    WHERE username = '{username}'
    AND pnumber = {pnumber}
    ;
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def deletePasswordData(self, lastPNumber):
    sqlQuery = f'''
    DELETE FROM passwords
    WHERE
    pnumber >= {lastPNumber}
    ;
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)

# createAdminTable() # initialize via root __init__.py
