# Created by asorova

from parser.categorizer import get_config, read_data
import os
import json


def product_matches_claims(product_claims, selected_claims):
    for claim in selected_claims:
        if claim in product_claims:
            return True
    return False


def select_column_for_prediction(cleared_data, prediction):
    if prediction == 'demand':
        return cleared_data[['Event Date', 'Sub-Category', 'Event', 'Region']].dropna(how='any')
    elif prediction == 'price':
        return cleared_data[['Event Date', 'Sub-Category', 'Event', 'Euro Price/Kg']].dropna(how='any')
    else:
        raise Exception("Wrong prediction type. Use prediction=demand or prediction=price")


# return data which matches certain claim
def save_corresponding_dataframe(config_file, claim, prediction):
    config = get_config(config_file)
    df = read_data(config)
    claims_file = config['popular_claims_file']
    file_dir = config['directory_from']
    full_claims_file = os.path.join(file_dir, claims_file)
    matching_data_file = config['data_matching_claim_file']
    save_to = os.path.join(file_dir, matching_data_file)
    try:
        with open(full_claims_file) as f:
            claims = json.load(f)
    except OSError as er:
        raise Exception(
            f'Can not open file {full_claims_file}: {str(er)}. Please use categorizer to categorize claims.')

    # shouldn't be possible to select wrong claim
    if claim not in claims:
        raise Exception(f'There is no "{claim}" claim. Please select another claim.')

    selected_claims = claims[claim]
    df['match'] = df['claims_processed'].apply(
        lambda product_claims: product_matches_claims(product_claims, selected_claims))

    df = df[df['match'] == True]
    df = select_column_for_prediction(df, prediction)
    df.to_csv(save_to)


# demand - for claims prediction, price - for price prediction
if __name__ == "__main__":
    save_corresponding_dataframe('./../config.yaml', 'recyclable packaging', 'demand')
