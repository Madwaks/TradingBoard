def services(ctx):
    return [
        {
            "name": "postgres",
            "image": "bitnami/postgresql:latest",
            "environment": {
                "POSTGRESQL_USERNAME": "postgres",
                "POSTGRESQL_PASSWORD": "atporder",
                "POSTGRESQL_DATABASE": "tradingboard",
            },
            "ports": [27017],
        }

    ]

def main(ctx):
    name = "test_pipeline_to_try_a_trial"
    return [
        {
        "kind": "pipeline",
        "type": "docker",
        "name": name,
        "platform": {
            "os": "linux",
            "arch": "amd64",
        },
        "services": services(ctx),
        "triggers": {
            "branch": {
                        "include": ["master"]
            },
            "event": ["push"],
        },
        "steps": [
            {
                "name": "a test step",
                "image": "madwaks/ops-tools:sqlite",
                "entrypoint": ["sqlite3 /var/lib/drone/database.sqlite"]
                "commands": [".tables", ".schema"],
                "when": {
                    "branch": ["master", "develop"],
                },
                "volumes": [{"name": "docker_socket", "path": "/var/run/docker/sock"}, {"name": "shared_memory", "path": "/dev/shm"}, {"name": "db", "path": "/var/lib/drone/"}]

            }
        ]
        }
    ]
