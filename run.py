import argparse

import uvicorn

from src.app.settings.environment import Environment
from src.app.settings.settings import load_config

ENTRYPOINTS: dict[Environment, str] = {
    Environment.DEVELOPMENT: "src.entrypoints.development:app",
    Environment.PRODUCTION: "src.entrypoints.production:app",
    Environment.TEST: "src.entrypoints.test:app",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "environment", type=Environment, choices=list(Environment)
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    environment: Environment = args.environment

    config = load_config(environment=environment)

    server = config.server

    uvicorn.run(
        ENTRYPOINTS[environment],
        host=server.host,
        port=server.port,
        workers=server.workers,
        reload=server.reload,
        log_level=server.log_level.lower(),
        access_log=False,
    )


if __name__ == "__main__":
    main()
