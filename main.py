# Created by asorova
import sys
import argparse
import yaml
import os
import json
from parser.merge_and_inspect import parse_and_clean
from parser.categorizer import recreate_categories
from parser.data_selector import save_corresponding_dataframe
from LSTM_prediction.preprocessing import do_analysis


def get_config(config_file):
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    return config


# return True if flag --categorize should be set to True
def get_claims(config):
    claims_file = config['popular_claims_file']
    file_dir = config['directory_from']
    full_claims_file = os.path.join(file_dir, claims_file)
    try:
        with open(full_claims_file) as f:
            claims = json.load(f)
    except OSError:
        return True, None

    return False, claims.keys()


def parse_args(args, config):
    parser = argparse.ArgumentParser(
        description="Parses, categorizes and analyses bakery products data."
    )
    parser.add_argument(
        "-p",
        "--parse",
        action="store_true",
        default=False,
        help="Whether to clean, parse and write all the data sources into one file used for the analysis. It is "
             "recommended to use if the original data was enriched with more data.",
    )
    parser.add_argument(
        "-c",
        "--categorize",
        action="store_true",
        default=False,
        help="Whether to regenerate the list of most popular claims. It is recommended to be True if the '--parse' "
             "flag is set to True. If '--parse' flag is set to False, '--categorize' flag may be set to True in case "
             "the desirable number of the most popular claims was changed in the config file."
    )
    parser.add_argument(
        "-t",
        "--type",
        default='demand',
        type=str,
        choices=['demand', 'price'],
        help="The type of predictions to make. If set to 'demand', the number of new launches (user demand) for the "
             "selected claim per month will be predicted. If set to 'price', the average price of products belonging "
             "to the selected claim per month will be predicted. "
    )
    should_categorize, claims = get_claims(config)
    parser.add_argument(
        "-cl",
        "--claim",
        type=str,
        required=True,
        choices=claims,
        help="Products containing this claim in their list of claims will be used for analysis. This claim "
             "should be one of the most popular claims. "
    )
    parser.add_argument(
        "-r",
        "--region",
        type=str,
        default='all',
        choices=['West Europe', 'East Europe', 'all'],
        help="Products in selected region will be used for analysis. If set to 'all', prediction is made for "
             "categories in both East and West regions. "
    )
    parser.add_argument(
        "-tu",
        "--tune",
        action="store_true",
        default=False,
        help="Whether to tune the model with different parameters to get the most reliable predictions. Takes more "
             "time as compared to training the model with predefined parameters. It is recommended to be True if the "
             "original data was enriched with more data and either of flags '--categorize' or '--parse' is set to "
             "True",
    )
    parser.add_argument(
        "-n",
        "--numPred",
        type=int,
        default=6,
        help="The number of data points to be predicted in the future."
    )
    return parser.parse_args(args), should_categorize


def main(args=None):
    config_file = "./config.yaml"
    config = get_config(config_file)
    args, should_categorize = parse_args(args, config)

    if should_categorize and not args.categorize:
        raise Exception('There is no file with the most popular claims! To create it you have to set --categorize '
                        'flag to True.')

    if args.parse:
        parse_and_clean(config_file)

    if args.categorize:
        recreate_categories(config_file)

    save_corresponding_dataframe(config_file, args.claim, args.type)

    # returns figure to plot on the frontend
    do_analysis(config_file, args.type, args.region, args.numPred, args.tune)


if __name__ == "__main__":
    sys.exit(main())
