def renderSqlQuery(self, sqlQuery, vals=None):
    cursor = self.connections.connection.execute(sqlQuery)
    self.connections.connection.commit()
    entries = []
    for row in cursor:
        entries.append(dict(row))
    return entries


ERROR = object()


def sanitize_characters(string, replace_invalid_with=ERROR):
    for character in string:
        point = ord(character)

        if point == 0:
            if replace_invalid_with is ERROR:
                raise ValueError("SQLite identifier contains NUL character.")
            else:
                yield replace_invalid_with
        elif 0xD800 <= point <= 0xDBFF:
            if replace_invalid_with is ERROR:
                raise ValueError(
                    "SQLite identifier contains high-surrogate character.")
            else:
                yield replace_invalid_with
        elif 0xDC00 <= point <= 0xDFFF:
            if replace_invalid_with is ERROR:
                raise ValueError(
                    "SQLite identifier contains low-surrogate character.")
            else:
                yield replace_invalid_with
        elif 0xFDD0 <= point <= 0xFDEF or (point % 0x10000) in (0xFFFE, 0xFFFF):
            if replace_invalid_with is ERROR:
                raise ValueError(
                    "SQLite identifier contains non-character character.")
            else:
                yield replace_invalid_with
        else:
            yield character


def quote_identifier(identifier, replace_invalid_with=ERROR):
    sanitized = "".join(sanitize_characters(identifier, replace_invalid_with))
    return "\"" + sanitized.replace("\"", "\"\"") + "\""
