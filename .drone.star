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
    name = "publish_pipeline"
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
            "event": ["push", "pull_request"],
        },
        "steps": [
            {
                "name": "publish image",
                "image": "plugins/docker",
                "settings": {
                    "username": {"from_secret": "DOCKER_USERNAME"},
                    "password": {"from_secret": "DOCKER_PASSWORD"},
                    "repo": "tradingboard",
                    "tags": "test_tag"
                }
                "when": {
                    "branch": ["master", "develop"],
                },
                "volumes": [{"name": "docker_socket", "path": "/var/run/docker/sock"}, {"name": "shared_memory", "path": "/dev/shm"}, {"name": "db", "path": "/var/lib/drone/"}]

            }
        ]
        }
    ]
