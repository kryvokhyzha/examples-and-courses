from libs import *


def get_description(df: pd.DataFrame, id_cols='id') -> None:
    """
        Usage Example:
            get_description(df, id_cols=Id_col)
    """
    if isinstance(id_cols, list):
        for col in id_cols:
            if col not in df.columns:
                raise KeyError('DataFrame df doesn`t contain `{col}` column!'.format(col=col))

    summary = (df[[i for i in df.columns if i not in id_cols]].describe().transpose().reset_index())

    summary = summary.rename(columns = {"index" : "feature"})
    summary = np.around(summary,3)

    val_lst = [summary['feature'], summary['count'],
               summary['mean'],summary['std'],
               summary['min'], summary['max'],
               summary['25%'], summary['50%'],
               summary['75%']]

    trace  = go.Table(header=dict(values=summary.columns.tolist(),
                                    line=dict(color = ['#506784']),
                                    fill=dict(color = ['#119DFF']),
                                   ),
                      cells=dict(values=val_lst,
                                    line=dict(color = ['#506784']),
                                    fill=dict(color = ["lightgrey",'#F5F8FF'])
                                   ),
                      columnwidth = [200,60,100,100,60,60,80,80,80])
    layout = go.Layout(dict(title = "Variable Description"))
    figure = go.Figure(data=[trace],layout=layout)
    py.iplot(figure)


def percentile_based_outlier(df: pd.DataFrame, threshold=95) -> None:
    diff = (100 - threshold) / 2
    minval, maxval = np.percentile(df, [diff, 100 - diff])
    return (df < minval) | (df > maxval)


def have_null(df: pd.DataFrame) -> None:
    """
        If this function returns true then there are null values in the data frame and false means there are none
    """
    return df.isnull().values.any()


def number_of_missing_values(df: pd.DataFrame) -> None:
    """
        This function returns the total number of missing values across different columns
    """
    return df.isnull().sum()


def IQR(df: pd.DataFrame) -> None:
    """
        IQR = Q3 −  Q1
    """
    return df.quantile(0.75) - df.quantile(0.25)


def intitial_eda_checks(df: pd.DataFrame) -> None:
    """
        1. Take a dataframe.
        2. Check if there is duplicates.
        3. Check if there is nulls.
    """

    # keep=False - marke all duplicates as True
    if len(df[df.duplicated(keep=False)]) > 0:
        print(df[df.duplicated(keep=False)])
        df.drop_duplicates(keep='first', inplace=True)
        print('Warning! df has been mutated!')
    else:
        print('No duplicates found.')

    if df.isnull().sum().sum() > 0:
        mask_total = df.isnull().sum().sort_values(ascending=False) 
        total = mask_total[mask_total > 0]

        mask_percent = df.isnull().mean().sort_values(ascending=False) 
        percent = mask_percent[mask_percent > 0] 

        missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    
        print(f'Total and Percentage of NaN:\n {missing_data}')
    else: 
        print('No NaN found.')


def view_columns_w_many_nans(df: pd.DataFrame, missing_percent=.9) -> None:
    """
        1. Checks which columns have over specified percentage of missing values.
        2. Takes df, missing percentage.
        3. Returns columns as a list.
    """
    mask_percent = df.isnull().mean()
    series = mask_percent[mask_percent > missing_percent]
    columns = series.index.to_list()
    print(columns) 
    return columns


def drop_columns_w_many_nans(df: pd.DataFrame, missing_percent=.9) -> None:
    """
        Define a function that will drop the columns whose missing value bigger than missing_percent
    """
    series = view_columns_w_many_nans(df, missing_percent=missing_percent)
    list_of_cols = series.index.to_list()
    df.drop(columns=list_of_cols)
    print(list_of_cols)
    return df


def histograms_numeric_columns(df: pd.DataFrame, numerical_columns: list) -> None:
    """
        1. Take df, numerical columns as list.
        2. Return group histagrams.
    """
    f = pd.melt(df, value_vars=numerical_columns) 
    g = sns.FacetGrid(f, col='variable',  col_wrap=4, sharex=False, sharey=False)
    g = g.map(sns.distplot, 'value')
    return g


def boxplots_categorical_columns(df: pd.DataFrame, categorical_columns: list, dependant_variable: str) -> None:
    """
        1. Take df, a list of categorical columns, a dependant variable as str.
        2. Return group boxplots of correlations between categorical varibles and dependant variable.
    """
    def boxplot(x, y, **kwargs):
        sns.boxplot(x=x, y=y)
        x=plt.xticks(rotation=90)

    f = pd.melt(df, id_vars=[dependant_variable], value_vars=categorical_columns)
    g = sns.FacetGrid(f, col='variable',  col_wrap=2, sharex=False, sharey=False, height=10)
    g = g.map(boxplot, 'value', dependant_variable)
    return g


def heatmap_numeric_w_dependent_variable(df: pd.DataFrame, dependent_variable: str) -> None:
    """
        Generate a heatmap of dependent variable's correlation with y
    """
    plt.figure(figsize=(8, 10))
    g = sns.heatmap(df.corr()[[dependent_variable]].sort_values(by=dependent_variable), 
                    annot=True, 
                    cmap='coolwarm', 
                    vmin=-1,
                    vmax=1) 
    return g


def high_corr_w_dependent_variable(df: pd.DataFrame, dependent_variable: str, corr_value: float) -> None:
    """
        Get a dataframe of independant varibles that are highly (e.g. abs(corr) > 0.4) with dependent varible
    """
    temp_df = df.corr()[[dependent_variable]].sort_values(by=dependent_variable, ascending=False)
    mask_1 = abs(temp_df[dependent_variable]) > corr_value
    return temp_df.loc[mask_1]


def high_corr_among_independent_variable(df: pd.DataFrame, dependent_variable: str, corr_value: float) -> None:
    """
        1. Check correlation among independant varibles.
        2. To see which two features have strong corr with each ohter.
    """
    df_corr = df.drop(columns=[dependent_variable]).corr()
    corr_dict = df_corr.to_dict()
    temp_dict = {key_1: {key_2 : value 
                         for key_2, value in imbeded_dictionary.items() 
                         if abs(value) < 1 and abs(value) > corr_value}
                for key_1, imbeded_dictionary in corr_dict.items()}
    return {k:v for k, v in temp_dict.items() if v}


def categorical_to_ordinal_transformer(categories: list) -> None:
    """
    Returns a function that will map categories to ordinal values based on the
    order of the list of `categories` given.

    Example:
        If categories is ['A', 'B', 'C'] then the transformer will map 
        'A' -> 0, 'B' -> 1, 'C' -> 2.
    """
    return lambda categorical_value: categories.index(categorical_value)


def transform_categorical_to_numercial(df: pd.DataFrame, categorical_numerical_mapping) -> None:
    """
        1. Transform categorical columns to numerical columns
        2. Take a df, a dictionary 
        3. Return df
    """
    transformers = {k: categorical_to_ordinal_transformer(v) 
                    for k, v in categorical_numerical_mapping.items()}
    new_df = df.copy()
    for col, transformer in transformers.items():
        new_df[col] = new_df[col].map(transformer).astype('int64')
    return new_df


def dummify_categorical_columns(df: pd.DataFrame) -> None:
    """
        Dummify all categorical columns
    """
    categorical_columns = df.select_dtypes(include="object").columns
    return pd.get_dummies(df, columns=categorical_columns, drop_first=True)


def conform_columns(df_reference: pd.DataFrame, df: pd.DataFrame) -> None:
    """
        Drop columns in df that are not in df_reference
    """
    to_drop = [c for c in df.columns if c not in df_reference.columns]
    return df.drop(to_drop, axis=1)


import statsmodels.api as sm
from io import StringIO
def extract_individual_summary_table_statsmodel(X, y, table_number) -> None:
    """
        Extract individual summary table from statsmodel.summary

        1. Take X_test, y_test, and table_number
        2. Return a df
    """
    X = sm.add_constant(X)
    y = y
    model = sm.OLS(y,X).fit()
    summary_df = StringIO(model.summary().tables[table_number].as_csv())
    meta_df = pd.read_csv(summary_df)
    return meta_df
