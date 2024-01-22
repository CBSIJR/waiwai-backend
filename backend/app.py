import argparse
from .configs import Production, Development
import uvicorn

environments = {
    'prod': Production,
    'dev': Development
}


def start():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-env', '--environment', type=str, choices=environments.keys(),
                        help='Project environment')
    args = parser.parse_args()
    settings: Production | Development = environments[args.environment]()

    uvicorn.run("backend.waiwai:app", **settings.load())
