import os
from argparse import ArgumentParser

import pandas as pd
import catboost as cb

MODEL_PATH = os.path.join(os.path.dirname(__file__), "seduce_model")

OUTPUT_HEADER = [
    'ID',
    'Scheme',
    'Frequency',
    'Q_error',
    'SSC_error',
    'LC_method',
    'MP_length',
    'IA_method',
    'Area',
    'SSL_obs',
    'Confidence_interval',
    'Percentile_low',
    'Percentile_high',
    'SSL_error_pred_low',
    'SSL_error_pred_high',
    'SSL_pred_low',
    'SSL_pred_high'
]

# List of model input variables
X_VARIABLES = [
    'Scheme',
    'Frequency',
    'Q_error',
    'SSC_error',
    'LC_method',
    'MP_length',
    'IA_method',
    'Percentile',
    'Area'
]

# List of categorical features from model input variables
CAT_FEATURES = [
    "Scheme",
    "LC_method",
    "IA_method"
]


def run_seduce(input_path, output_path, model_path=MODEL_PATH):
    """ Run SedUCE model on input SSL observations.

    Args:
        input_csv (str): Full path to .csv file of SSL observations
        output_csv (str): Full path to .csv model output
        model_path (str): Full path to SedUCE model
    """

    # Load SSL observations as Pandas DataFrame
    df = pd.read_csv(input_path)

    df["Percentile_low"] = (100 - df["Confidence_interval"]) / 2
    df["Percentile_high"] = 100 - (100 - df["Confidence_interval"]) / 2

    for bound in ("low", "high"):
        df["Percentile"] = df["Percentile_"+bound]

        # Initialize CatBoost Pool from SSL observations dataframe
        dataset = cb.Pool(data=df[X_VARIABLES], cat_features=CAT_FEATURES)

        # Initialize CatBoostRegressor and load trained model
        cb_model = cb.CatBoostRegressor()
        cb_model.load_model(model_path)

        # Generate error predictions by applying model on SSL observations
        predictions = cb_model.predict(dataset)

        # Convert predicted log errors to normal values
        df["SSL_error_pred_"+bound] = 10 ** predictions

        # Compute SSL value associated with predicted error
        inv_bound = {"low": "high", "high": "low"}[bound]
        df["SSL_pred_"+inv_bound] = df["SSL_obs"] / df["SSL_error_pred_"+bound]

    df = df[OUTPUT_HEADER]

    # Save output as csv
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Provides error estimates on suspended sediment load (SSL) observations using the SedUCE model.")
    parser.add_argument("input_csv", type=str,
                        help="Input csv file of SSL observations")
    parser.add_argument("output_csv", type=str, help="Output csv model output")
    parser.add_argument("-m", "--model", type=str, default=MODEL_PATH,
                        help=f"SedUCE model to use (defaults to {MODEL_PATH})")
    args = parser.parse_args()
    run_seduce(
        os.path.realpath(args.input_csv),
        os.path.realpath(args.output_csv),
        model_path=os.path.realpath(args.model),
    )
