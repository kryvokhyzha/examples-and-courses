import numpy as np
import pandas as pd
import iml
from tqdm import tqdm


def calculate_top_contributors(
        base_value, shap_values, features=None, feature_names=None,
        use_abs=False, return_df=False, n_features=5,
):
    """ Adapted from the SHAP package for visualizing the contributions of features towards a prediction.
        https://github.com/slundberg/shap
        Args:
            base_value: float base value
            shap_values: np.array of floats
            features: pandas.core.series.Series, the data with the values
            feature_names: list, all the feature names/ column names
            use_abs: bool, if True, will sort the data by the absolute value of the feature effect
            return_df: bool, if True, will return a pandas dataframe, else will return a list of feature, effect, value
            n_features: int, the number of features to report on. If it equals -1 it will return the entire dataframe
        Returns:
            if return_df is True: returns a pandas dataframe
            if return_df is False: returns a flattened list by name, effect, and value
        """
    assert not type(shap_values) == list, "The shap_values arg looks looks multi output, try shap_values[i]."
    assert len(shap_values.shape) == 1, "Expected just one row. Please only submit one row at a time."

    shap_values = np.reshape(shap_values, (1, len(shap_values)))
    instance = iml.Instance(np.zeros((1, len(feature_names))), features)
    link = iml.links.convert_to_link('identity')

    # explanation obj
    expl = iml.explanations.AdditiveExplanation(
        base_value,                                      # base value
        np.sum(shap_values[0, :]) + base_value,          # this row's prediction value
        shap_values[0, :],                               # matrix
        None,
        instance,                                        # <iml.common.Instance object >
        link,                                            # 'identity'
        iml.Model(None, ["output value"]),               # <iml.common.Model object >
        iml.datatypes.DenseData(np.zeros((1, len(feature_names))), list(feature_names))
    )

    # Get the name, effect and value for each feature, if there was an effect
    features_ = {}
    for i in range(len(expl.data.group_names)):
        if expl.effects[i] != 0:
            features_[i] = {
                "effect": ensure_not_numpy(expl.effects[i]),
                "value": ensure_not_numpy(expl.instance.group_display_values[i]),
                "name": expl.data.group_names[i]
            }

    effect_df = pd.DataFrame([v for k, v in features_.items()])

    if use_abs:  # get the absolute value of effect
        effect_df['effect'] = effect_df['effect'].apply(np.abs)
        effect_df.sort_values('effect', ascending=False, inplace=True)
    else:
        effect_df.sort_values('effect', ascending=False, inplace=True)
    if not n_features == -1:
        effect_df = effect_df.head(n_features)
    if return_df:
        return effect_df.reset_index(drop=True)
    else:
        list_of_info = list(zip(effect_df.name, effect_df.effect, effect_df.value))
        effect_list = list(sum(list_of_info, ()))  # flattens the list of tuples
        return effect_list


def create_prediction_factors_df(
        base_value, shap_values, X, feature_names,
        n_features, use_abs,
):
    """Takes in the report df, contribs, previous eval df, and the model
    Args:
        base_value: float base value
        shap_values: numpy matrix
        X: pandas DataFrame
        feature_names: List of feature names
        n_features: number of top features to select
        use_abs: bool, if True, will sort the data by the absolute value of the feature effect
    Returns:
        pd.DataFrame of the factors
    """

    factors = []
    for i in tqdm(range(X.shape[0])):
        vals = calculate_top_contributors(
            base_value=base_value, shap_values=shap_values[i, :], features=X.iloc[i, :],
            feature_names=feature_names, n_features=n_features, use_abs=use_abs,
        )
        factors.append(vals)
    columns = [item for idx in range(len(vals) // 3) for item in (f'F{idx}', f'F{idx}_effect', f'F{idx}_value')]
    df = pd.DataFrame(factors, columns=columns)
    return df


def ensure_not_numpy(x):
    """Helper function borrowed from the iml package"""
    if isinstance(x, bytes):
        return x.decode()
    elif isinstance(x, np.str):
        return str(x)
    elif isinstance(x, np.generic):
        return float(np.asscalar(x))
    else:
        return x


def get_feature_class_distance(
        base_values, shap_values, feature_names, X_test,
        unique_y, pred_label, y_test=None,
        use_abs=False, n_features=None
):
    factors_df = {}
    if n_features is None:
        n_features = len(feature_names)

    for class_id in unique_y:
        t = create_prediction_factors_df(
            base_values[class_id], shap_values[:, class_id, :],
            X_test, feature_names, n_features, use_abs=use_abs,
        )
        t = t[list(filter(lambda x: 'effect' in x, t.columns))].sum(axis=1)
        factors_df[f'total_effect_class_{class_id}'] = t.copy()

    factors_df = pd.DataFrame(factors_df)
    factors_df['prediction'] = pred_label
    if y_test is not None:
        factors_df['target'] = y_test
        factors_df['miss_clf'] = (pred_label != y_test)

    factors_df['distance'] = factors_df.apply(
        lambda x: np.min(
            x['total_effect_class_{0}'.format(int(x['prediction']))] -
            np.asarray([
                x[f'total_effect_class_{int(idx)}']
                for idx in list(filter(lambda item: item != x['prediction'], unique_y))
            ])
        ), axis=1)
    return factors_df
