import argparse
import stargate_libs


def main():
    arg_parser = argparse.ArgumentParser(description="Transfers data from an excel file to a database")
    arg_parser.add_argument('-f', '--file', type=str, required=False, help='file name and path to process')
    arg_parser.add_argument('-d', '--db', type=str, required=False,
                            help='database configuration to utilize')
    arg_parser.add_argument('-t', '--table', type=str, required=False, help='name of the target table')
    arg_parser.add_argument('-p', '--password', type=str, required=False, help="database user account password")
    arg_parser.add_argument('-s', '--sheet', type=str, required=False, help='name of worksheet where data resides')
    arg_parser.add_argument('--uuid', action=argparse.BooleanOptionalAction, required=False, help="add uuid column flag")
    arg_parser.add_argument('--upper', action=argparse.BooleanOptionalAction, required=False, help="normalize column names to uppercase flag")
    arg_parser.add_argument('--lower', action=argparse.BooleanOptionalAction, required=False, help="normalize column names to lowercase flag")
    arg_parser.add_argument('--if-exists',
                            type=str,
                            required=False,
                            help="How to behave if table exists",
                            choices=['fail', 'append', 'replace'])
    arg_parser.add_argument('--config', type=str,
                            help='path to configuration json file, if not specified default [$HOME/.stargate/config.json] will be used')
    argz = arg_parser.parse_args()

    interface = stargate_libs.Interface(argz)
    interface.start()


if __name__ == "__main__":
    main()

