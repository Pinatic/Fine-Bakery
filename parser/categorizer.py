import pandas as pd
from collections import Counter
import warnings
warnings.filterwarnings("ignore")
import yaml
import re
import json
import io
import os
import panel as pn
pn.extension()


def startupCheck(claims_file):
    '''
    Checks if claim_matching.json is present, creates the file if it is not present

    Author(s):
    Pieter de Jong
    '''
    if os.path.isfile(claims_file) and os.access(claims_file, os.R_OK):
        # checks if file exists
        print ("File found")
    else:
        print ("Creating file")
        with io.open(claims_file, 'w') as db_file:
            db_file.write(json.dumps({}))


def read_data(config):
    dir_to = config['directory_to']
    file_name_to = config['cleared_data_to']
    df = pd.read_csv(os.path.join(dir_to, file_name_to), parse_dates=['Event Date'])
    df = df.dropna(subset=['claims_processed'])
    df['claims_processed'] = df['claims_processed'].apply(lambda str_claims: str(str_claims).split("|"))
    return df


def get_config(config):
    with open(config, 'r') as stream:
        config = yaml.safe_load(stream)
    return config


def cleaning(df):
    '''
    Cleans the dataframe by removing rows with no claims.
    Making the Claims/Features column all lowercase.
    Removing some unwanted characters.

    Arguments:
    path           : Dataframe
    Returns:       : Dataframe

    Author(s):
    Pieter de Jong
    '''
    df = df.dropna(subset=["Claims/Features"])
    df["claims_processed"] = df["Claims/Features"].str.lower()
    df["claims_processed"] = df["claims_processed"].str.replace(",", ".").str.replace("\n", " ").str.replace("\'s", "")
    df["claims_processed"] = df["claims_processed"].str.rstrip(".").str.split("\. ")

    return df


def find_pattern(pattern, string):
    '''
    Returns each string containing pattern

    Arguments:
    Pattern        : String
    String         : String
    Returns:       : String

    Author(s):
    Pieter de Jong
    '''
    return bool(re.search(pattern, string))


def clean_nonclaims(df):
    '''
    Removes claims that contain patterns marking them non claims

    Arguments:
    df             : Dataframe
    Returns:       : Dataframe

    Author(s):
    Pieter de Jong
    '''
    all_prod_claims = []
    pattern = ": \d|kcal|kj|\dg|\d g|.org"
    for claims in df["claims_processed"]:
        claims_no_ingredients = []
        for claim in claims:
            claim = claim.lstrip()
            if not find_pattern(pattern, claim):
                claims_no_ingredients.append(claim)
        all_prod_claims.append(claims_no_ingredients)
    df["claims_processed"] = all_prod_claims
    return df


def advanced_space_split(df):
    '''
    Splits sentences where a space is missing. including when next sentence starts with a number.
    does not split abbreviations like h.u.v and ignores no.1

    Arguments:
    df             : Dataframe
    Returns:       : Dataframe

    Author(s):
    Pieter de Jong
    '''
    pattern = "\D\.\D"
    pattern2 = "\D\.\D\."
    pattern3 = "\D\.\d"
    pattern4 = "no.1"
    claims_cleaned = []
    for claims in df["claims_processed"]:
        temp_claims = claims
        for claim in claims:
            if find_pattern(pattern, claim) and not find_pattern(pattern2, claim):
                temp_claims.remove(claim)
                temp_claims.append(claim.split(".")[0])
                temp_claims.append(claim.split(".")[1])

            if find_pattern(pattern3, claim) and not find_pattern(pattern4, claim):
                temp_claims.remove(claim)
                temp_claims.append(claim.split(".")[0])
                temp_claims.append(claim.split(".")[1])
        claims_cleaned.append(temp_claims)
    df["claims_processed"] = claims_cleaned
    # to save list of string as a string in the csv file
    df['claims_processed'] = df['claims_processed'].apply(lambda list_of_str: '|'.join(list_of_str))
    return df


def claim_counter(df):
    '''
    Create list of all unique claims and a list of all claims

    Arguments:
    df             : Dataframe
    Returns:       : List of claims, List of unique claims

    Author(s):
    Pieter de Jong
    '''
    all_cleaned_unique_claims = []
    all_cleaned_claims = []
    for claims in df["claims_processed"]:
        for claim in claims:
            all_cleaned_claims.append(claim)
            if claim not in all_cleaned_unique_claims:
                all_cleaned_unique_claims.append(claim)
    return all_cleaned_claims, all_cleaned_unique_claims


def get_matches(pattern, all_cleaned_unique_claims):
    '''
    Create list of all unique claims matching certain pattern

    Arguments:
    pattern        : string
    Returns:       : List of claims matching certain pattern

    Author(s):
    Pieter de Jong
    '''
    pattern_match = []
    for claim in all_cleaned_unique_claims:
        if find_pattern(pattern, claim):
            if claim not in pattern_match:
                pattern_match.append(claim)
    return pattern_match


def get_claims(df, claims_num=10):
    '''
    Create list of all unique claims matching certain pattern

    Arguments:
    df             : Dataframe
    claims_num     : int, number of most popular claims
    Returns:       : List of claims, List of unique claims, List of most popular claims

    Author(s):
    Pieter de Jong
    '''
    all_cleaned_claims, all_cleaned_unique_claims = claim_counter(df)
    claim_amount = Counter(all_cleaned_claims)
    popular_claims = [claim[0] for claim in claim_amount.most_common()[:claims_num]]
    return all_cleaned_claims, all_cleaned_unique_claims, popular_claims


def clean_data(df):
    '''
    Clean data using several cleaning functions

    Arguments:
    df             : Dataframe
    Returns:       : df, Dataframe - Cleaned dataframe ready to be categorized

    Author(s):
    Pieter de Jong
    '''
    df = cleaning(df)
    df = clean_nonclaims(df)
    df = advanced_space_split(df)
    return df


def recreate_categories(config_file):
    '''
    Clean data using several cleaning functions

    Arguments:
    df             : Dataframe
    Returns:       : df, Dataframe - Cleaned dataframe ready to be categorized

    Author(s):
    Pieter de Jong
    '''
    config = get_config(config_file)
    df = read_data(config)

    try:
        popular_claims_num = int(config['popular_claims_num'])
    except ValueError as ve:
        print(
            f'Check the correctness of the popular_claims_num parameter - should be integer: {str(ve)}. Default value is used: popular_claims_num = 20')
        popular_claims_num = 20

    json_file = config['popular_claims_file']
    file_dir = config['directory_from']
    claims_file = os.path.join(file_dir, json_file)

    all_cleaned_claims, all_cleaned_unique_claims, popular_claims = get_claims(df, popular_claims_num)
    startupCheck(claims_file)
    claim_dict = {}
    for claim in popular_claims:
        claim_dict[claim] = get_matches(claim, all_cleaned_unique_claims)

    with open(claims_file, "w") as jsonfile:
        json.dump(claim_dict, jsonfile)


if __name__ == "__main__":
    recreate_categories("./../config.yaml")



