import argparse
import sys
from streamlit_code.web import cli as stcli



if __name__ == '__main__':
    # use argparse to get the flags
    parser = argparse.ArgumentParser()
    parser.add_argument('--server_port', default=None, type=str, help='add port to run the app. for example: --server_port 8501')
    args = parser.parse_args()
    sys.argv = ["streamlit", "run", "basic_version.py",
                # "--server.headless", "true",
                # "global.developmentMode", "false",
                ]
    if args.server_port:
        sys.argv.append("--server.port")
        sys.argv.append(args.server_port)

    sys.exit(stcli.main())