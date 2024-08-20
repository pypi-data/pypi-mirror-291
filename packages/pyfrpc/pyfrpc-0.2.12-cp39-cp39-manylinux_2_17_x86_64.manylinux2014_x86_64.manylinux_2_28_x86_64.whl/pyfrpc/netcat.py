# -*- coding: utf-8 -*-

from .client import FrpcClient


def main():
    import argparse

    from requests.packages import urllib3

    parser = argparse.ArgumentParser(description="FRPC netcat for interactive connection to FRPC server")
    parser.add_argument("--insecure", action='store_true', help="Do not check server's cert")
    parser.add_argument("--cert", metavar="CERT", help="Client certificate file")
    parser.add_argument("--key", metavar="KEY", help="Client key file")
    parser.add_argument("url", metavar="URL", help="URL of FRPC server to connect to")
    args = parser.parse_args()

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    cert = (args.cert, args.key) if args.cert else None
    client = FrpcClient(args.url, cert=cert, verify=(not args.insecure))

    import IPython

    IPython.start_ipython(
        argv=[],
        user_ns={
            "client": client.rpc
        }
    )
