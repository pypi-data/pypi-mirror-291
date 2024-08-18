from typing import Any, Dict, Optional
import psycopg2
from airflow.hooks.base import BaseHook
from airflow.utils.decorators import apply_defaults

class GreenplumHook(BaseHook):
    """
    Custom hook for Greenplum database access using psycopg2.
    """

    @apply_defaults
    def __init__(self, gp_conn_id: str = 'gp_default', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.gp_conn_id = gp_conn_id

    def get_conn(self) -> psycopg2.extensions.connection:
        """
        Retrieves the connection object from the connection ID.
        :return: psycopg2 connection object
        """
        conn_id = self.gp_conn_id
        conn = self.get_connection(conn_id)
        try:
            connection = psycopg2.connect(
                user=conn.login,
                password=conn.password,
                host=conn.host,
                port=conn.port,
                database=conn.schema
            )
            return connection
        except Exception as e:
            self.log.error(f"Failed to connect to Greenplum: {e}")
            raise

    def set_autocommit(self, conn: psycopg2.extensions.connection, autocommit: bool) -> None:
        """
        Enable or disable autocommit for the given connection.
        :param conn: The connection.
        :param autocommit: The connection's autocommit setting.
        """
        conn.autocommit = autocommit

    def get_autocommit(self, conn: psycopg2.extensions.connection) -> bool:
        """
        Get autocommit setting for the provided connection.
        :param conn: The connection.
        :return: connection autocommit setting.
        :rtype: bool
        """
        return conn.autocommit

    def run(self, sql: str, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a SQL command.
        :param sql: The SQL command to execute.
        :param parameters: Optional parameters for SQL command.
        :return: Result of the SQL command execution.
        """
        conn = self.get_conn()
        try:
            self.set_autocommit(conn, True)
            with conn.cursor() as cursor:
                cursor.execute(sql, parameters)
                # Check if the SQL command produces results
                if cursor.description:  # If cursor.description is not None, it means there are results
                    result = cursor.fetchall()  # Fetch all results
                    return result
                else:
                    # For commands like CREATE TABLE, RETURN nothing or a message
                    return "Command executed successfully, no results to fetch."
        except Exception as e:
            self.log.error(f"Failed to execute SQL command: {e}")
            raise
        finally:
            conn.close()
