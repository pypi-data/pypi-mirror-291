from . import dbUtils


def executeCommand(self):
    query = '''UPDATE encryptedCurrent
    SET
    arena = "committed"
    WHERE 1=1
    ;
    '''
    return dbUtils.renderSqlQuery(self, query, vals=None)
# executeCommand()


def alterEncTable(self):
    query = '''ALTER TABLE encryptedCurrent
    ADD 
    arena_before_commit VARCHAR(16) DEFAULT "init"
    ;
    '''
    return dbUtils.renderSqlQuery(self, query, vals=None)
# alterEncTable()


def createEncTable(self):
    query = '''CREATE TABLE IF NOT EXISTS encryptedCurrent(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path VARCHAR(255) UNIQUE NOT NULL,
    hash_value VARCHAR(255) NOT NULL,
    children TEXT NOT NULL,
    type VARCHAR(16) NOT NULL,
    arena VARCHAR(16) DEFAULT "init",
    arena_before_commit VARCHAR(16) DEFAULT "init",
    deleted_at DATETIME DEFAULT NULL,

    created_at DATETIME DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at DATETIME DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
    );
    '''
    return dbUtils.renderSqlQuery(self, query, vals=None)


def createEncTableIndex(self):
    query = '''
    CREATE INDEX IF NOT EXISTS path
    ON encryptedCurrent (path, hash_value, children, type, arena, created_at, updated_at);
    '''
    return dbUtils.renderSqlQuery(self, query, vals=None)


def dropEncTable(self):
    query = '''
    DROP TABLE IF EXISTS encryptedCurrent;
        '''
    return dbUtils.renderSqlQuery(self, query, vals=None)


def deleteEncData(self, path):
    sqlQuery = f'''UPDATE encryptedCurrent
    SET
    arena = "deleted",
    deleted_at = (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at = (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
    WHERE
    path = "{path}";
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)
# deleteEncData("test/mind.txt", "14efr$", "", "file")


def updateEncData(self, path, hashValue, children="", type="", arena="init", arenaBeforeCommit=None):
    sqlQuery = f'''UPDATE encryptedCurrent
    SET
    hash_value = "{hashValue}",
    children = "{children}",
    type = "{type}",
    arena = "{arena}",
    arena_before_commit = "{arenaBeforeCommit}",
    deleted_at = NULL,
    updated_at = (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
    WHERE
    path = "{path}";
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)
# updateEncData("test/mind.txt", "14efr$", "", "file")


def insertEncData(self, path, hashValue, children="", type="", arena="init", arenaBeforeCommit="init"):
    sqlQuery = f'''INSERT INTO encryptedCurrent(
    path,
    hash_value,
    children,
    type,
    arena,
    arena_before_commit
    )
    VALUES(
    "{path}",
    "{hashValue}",
    "{children}",
    "{type}",
    "{arena}",
    "{arenaBeforeCommit}"
    );
    '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)
# insertEncData("test/mind.txt", "14efr$", "", "file")
# insertEncData("test/nest/", "r45h65", "", "folder")


def fetchEncData(self, path=None, relaxed=False):
    dStatement = 'AND deleted_at IS NULL' if relaxed == False else ''
    # print("dStatement: ", relaxed, dStatement)
    if(path != None):
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        children AS children,
        type AS type,
        arena AS arena,
        arena_before_commit AS arenaBeforeCommit,
        deleted_at AS deletedAt
        FROM encryptedCurrent
        WHERE path = "{path}"
        {dStatement}
        ;
        '''
    else:
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        children AS children,
        type AS type,
        arena AS arena,
        arena_before_commit AS arenaBeforeCommit,
        deleted_at AS deletedAt
        FROM encryptedCurrent
        WHERE
        'apple'='apple'
        {dStatement}
        ;
        '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)

# print(fetchEncData("test/nest/"))
# print(fetchEncData())


def fetchEncDataPathRegexp(self, pathLike=None):
    if(pathLike != None):
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        children AS children,
        type AS type,
        arena AS arena,
        arena_before_commit AS arenaBeforeCommit
        FROM encryptedCurrent
        WHERE path LIKE "%{pathLike}%"
        AND deleted_at IS NULL
        ;
        '''
    else:
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        children AS children,
        type AS type,
        arena AS arena,
        arena_before_commit AS arenaBeforeCommit
        FROM encryptedCurrent
        WHERE
        AND deleted_at IS NULL
        ;
        '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def fetchEncDataPathRegexpStart(self, pathLike=None):
    if(pathLike != None):
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        children AS children,
        type AS type,
        arena AS arena,
        arena_before_commit AS arenaBeforeCommit
        FROM encryptedCurrent
        WHERE path LIKE "{pathLike}%"
        AND deleted_at IS NULL
        ;
        '''
    else:
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        children AS children,
        type AS type,
        arena AS arena,
        arena_before_commit AS arenaBeforeCommit
        FROM encryptedCurrent
        WHERE
        AND deleted_at IS NULL
        ;
        '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def fetchEncData10(self, path=None):
    if(path != None):
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        children AS children,
        type AS type,
        arena AS arena
        FROM encryptedCurrent
        WHERE path = "{path}"
        AND deleted_at IS NULL
        LIMIT 10
        ;
        '''
    else:
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        children AS children,
        type AS type,
        arena AS arena
        FROM encryptedCurrent
        WHERE
        AND deleted_at IS NULL        
        LIMIT 10;
        '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def fetchEncDataCommitted(self, path=None):
    if(path != None):
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        children AS children,
        type AS type,
        arena AS arena,
        arena_before_commit AS arenaBeforeCommit
        FROM encryptedCurrent
        WHERE path = "{path}"
        AND
        arena = "committed"
        AND deleted_at IS NULL        
        ;
        '''
    else:
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        children AS children,
        type AS type,
        arena AS arena,
        arena_before_commit AS arenaBeforeCommit
        from encryptedCurrent
        WHERE
        arena = "committed"
        AND deleted_at IS NULL
        ;        
        '''
    return dbUtils.renderSqlQuery(self, sqlQuery, vals=None)


def printEncDataOrganised(self, path=None):
    if(path != None):
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        type AS type,
        arena AS arena,
        arena_before_commit AS arenaBeforeCommit
        FROM encryptedCurrent
        WHERE path = "{path}"
        AND deleted_at IS NULL        
        ;
        '''
    else:
        sqlQuery = f'''
        SELECT
        path AS path,
        hash_value AS hashValue,
        type AS type,
        arena AS arena,
        arena_before_commit AS arenaBeforeCommit
        FROM encryptedCurrent
        AND deleted_at IS NULL
        ;        
        '''
    rsq = dbUtils.renderSqlQuery(self, sqlQuery, vals=None)
    for row in rsq:
        print(row)
        print()
    return []


# Initialize: done via root __init__.py file
# createEncTable(self)
# createEncTableIndex(self)

# Hard-Initialize: not-done anywhere
# dropEncTable()
# createEncTable()
# createEncTableIndex()
