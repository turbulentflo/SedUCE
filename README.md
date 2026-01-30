# The SedUCE model

The SedUCE (**Sed**iment **U**n**C**ertainty **E**stimation) model provides uncertainty estimates on current and historical suspended sediment load (SSL) observations, based on seven methodological factors (related to both the sampling process and the load derivation process) and catchment area.  

The model, along with a Python script to apply it, are available on [this repository](https://github.com/turbulentflo/Sandbox). 

For information on model training and development, please refer to the accompanying [journal article](). 

## Content of the repository

The repository includes the following files:

* The trained model (*seduce_model*)
* A Python script for applying the model (*seduce.py*)
* An example input csv file with ficticious SSL observations (*example_input_ssl.csv*)
* An example output csv file with model predictions (*example_output_predictions.csv*)

## Getting started

SedUCE was tested with `python = 3.8`, `pandas = 2.0.3`, and `catboost = 1.2.7`. We recommend using conda to manage dependencies. Pleease make sure to install [Conda](https://www.anaconda.com/docs/getting-started/miniconda/main) before proceeding. 


Create an environment:

```python
conda create --name seduce -y python=3.8
conda activate seduce
```

You can run the model from python using the `seduce.run_seduce` function:
```python
from seduce import run_seduce
run_seduce("example_input_ssl.csv", "example_output_predictions.csv")
```

Alternatively, you can run the model from a command prompt:
```bash
python seduce example_input_ssl.csv example_output_predictions.csv
```

## Input variables

The provided implementation requires 9 input variables to produce uncertainty estimates on suspended sediment load (SSL) observations. A description of each is provided below. For a more detailed breakdown, please refer to Tables 2 and 3 of the accompanying [manuscript]().

VARIABLE | DESCRIPTION | OPTIONS
-----|-----|-----
Scheme | Type of measurement distribution over a year | 1 = random <br> 2 = time-stratified <br>3 = flow-stratified
Frequency | Number of sampled days per year <br>Units: days yr<sup>-1</sup> | 6 (\~bi-monthly sampling) <br>12 (\~monthly sampling) <br>25 (\~bi-weekly sampling) <br>50 (\~weekly sampling) <br>200 (\~alternate day sampling) <br>365 (daily sampling)
Q_error | Percent error on discharge (Q) measurements <br>due to sampling method and/or equipment. <br>Value represents the standard deviation, assuming no bias and a normal distribution. | [0, ∞[ <br>*Model was trained with values 0, 5, 10, and 50\**
SSC_error | Percent error on suspended sediment <br>concentration (SSC) measurements due to <br>sampling method and/or equipment. <br>Value represents the standard deviation, assuming no bias and a normal <br>distribution. | [0, ∞[ <br>*Model was trained with values 0, 10, 35, and 100\**
LC_method | Load calculation method used for deriving SSL <br>from Q and SSC measurements | 1 = mean sediment discharge of samples<br>2 = mean SSC of samples x mean Q of samples<br>3 = mean SSC of samples x mean daily Q<br>4 = Q-weighted mean SSC of samples x mean daily Q<br>5 = log-linear rating curve<br>6 = log-linear rating curve with Ferguson correction factor<br>7 = rating curve with non-linear regression
MP_length | Length of the measuring period <br>Units: yrs | [1, ∞[ <br>*Model was trained with values 1, 3, 5, 10, 15, and 20\**
IA_method | Interannual aggregation method used to derive long-term SSL | 0 = not applicable (if MP_length = 1) <br>1 = average of annual SSLs <br>2 = pooling samples from all years
Confidence_interval | Probability that the true SSL falls within the <br>generated range of SSL or error values <br>Units: %  |[1, 100]
Area | Upstream area at the measurement location <br>Units: km<sup>2</sup> | ]0, ∞[ <br>*Model was trained with catchments ranging from 7 to 475,000 km<sup>2</sup>\**
SSL_obs <br>*(optional)* |  Observed suspended sediment load value. If using the <br>provided Python script to run SedUCE, this <br>field will be used to convert the predicted <br>error to a corresponding SSL value. <br>Units: t yr<sup>-1</sup> | [0, ∞[

\*If using values substantially outside of this range, interpretation of model outcome should be made with caution.

## Output variables

The provided implementation of the model outputs 4 columns: 

VARIABLE | DESCRIPTION
-----|-----
Percentile_low | Lower percentile bound of the uncertainty range. Based on the given confidence interval.
Percentile_high | Upper percentile bound of the uncertainty range. Based on the given confidence interval.
SSL_error_pred_low | Estimated SSL error corresponding to the lower percentile bound
SSL_error_pred_high | Estimated SSL error corresponding to the upper percentile bound
SSL_pred_low | If SSL_obs is given. Lower bound of the expected SSL range. <br> Units: t yr<sup>-1</sup>
SSL_pred_high | If SSL_obs is given. Upper bound of the expected SSL range. <br> Units: t yr<sup>-1</sup>

## License

This software is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contact

For questions or feedback regarding SedUCE, please contact turbulentflo(at)protonmail.com

## Citation

If using SedUCE in your research/work, please provide reference to the following publication: 

