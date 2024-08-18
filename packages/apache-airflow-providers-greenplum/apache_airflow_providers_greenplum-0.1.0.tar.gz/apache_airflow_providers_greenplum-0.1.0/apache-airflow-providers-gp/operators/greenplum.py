from typing import Any, Dict, Optional, Union
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from hooks.greenplum import GreenplumHook

class GreenplumOperator(BaseOperator):
    """
    Executes SQL code in Greenplum database using a custom hook.
    """
    @apply_defaults
    def __init__(
        self,
        sql: str,
        gp_conn_id: str = 'gp_default',
        parameters: Optional[Dict[str, Any]] = None,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.sql = sql
        self.gp_conn_id = gp_conn_id
        self.parameters = parameters

    def execute(self, context: Any) -> Any:
        self.log.info('Executing SQL: %s', self.sql)
        hook = GreenplumHook(gp_conn_id=self.gp_conn_id)
        try:
            result = hook.run(self.sql, parameters=self.parameters)
            return result
        except Exception as e:
            self.log.error(f"Failed to execute SQL: {e}")
            raise
