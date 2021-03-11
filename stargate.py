import argparse
import io
import sys
import pathlib
import json
import stargate_libs

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Transfers data from an excel file to a database")
    arg_parser.add_argument('-f','--file', type=str, required=False, help='file name and path to process')
    arg_parser.add_argument('-d','--db', type=str, required=False, help='database target where data will be sent, this is the reference name given to the database during configuration')
    arg_parser.add_argument('-s','--sheet', type=str, required=False, help='name of worksheet where data resides')
    arg_parser.add_argument('-c','--config', type=str, help='path to configuration json file, if not specified default [$HOME/.stargate/config.json] will be used')
    argz = arg_parser.parse_args()
    interface = stargate_libs.Interface(argz)
