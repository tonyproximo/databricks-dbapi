from databricks_dbapi import databricks
from pyhive.sqlalchemy_hive import HiveDialect


class DatabricksDialect(HiveDialect):
    @classmethod
    def dbapi(cls):
        return databricks

    def create_connect_args(self, url):
        kwargs = {
            "host": url.host,
            "port": url.port or 443,
            "database": url.database or "default",
            "user": url.username,
            "password": url.password
        }

        if url.query is not None and "http_path" in url.query:
            kwargs["http_path"] = url.query["http_path"]

        kwargs.update(url.query)
        return [], kwargs

    def get_table_names(self, connection, schema=None, **kw):
        query = "SHOW TABLES"
        if schema:
            query += " IN " + self.identifier_preparer.quote_identifier(schema)
        return [row[1] for row in connection.execute(query)]
