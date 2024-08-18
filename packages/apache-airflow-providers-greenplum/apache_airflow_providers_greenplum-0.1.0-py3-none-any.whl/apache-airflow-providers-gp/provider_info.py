def get_provider_info():
    return {
        "package-name": "apache-airflow-providers-greenplum",
        "name": "greenplum",
        "description": "Airflow Hook for Greenplum",
        "hook-class-names": [
            "apache-airflow-providers-gp.hooks.greenplum.GreenplumHook",
        ],
        "connection-types": [
            {'connection-type': "greenplum", 'hook-class-name': "apache-airflow-providers-gp.hooks.greenplum.GreenplumHook"}
        ],
        "extra-links": [
            "apache-airflow-providers-gp.operators.greenplum.GreenplumOperator"
        ]
    }
