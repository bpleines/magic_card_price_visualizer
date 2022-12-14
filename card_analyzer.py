import pathlib
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector as col_selector
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, OrdinalEncoder

class CardAnalyzer:
    """Class to store cards dataframe used for analysis"""
    def __init__(self):
        self.df = self.ingest_set_data()

    def address_missing_data(self):
        self.check_structure()
        self.df.dropna(how='any', inplace=True)
        self.check_structure()

    def check_structure(self):
        print(self.df.isnull().sum())
        print(self.df[self.df['artist'].isnull()])
        print(self.df.shape)
        print(self.df.dtypes)

    def check_numeric_value_bounds(self):
        for column in ['cmc', 'release_year', 'price']:
            print(f"{column} MIN {self.df[column].min()}")
            print(f"{column} MAX {self.df[column].max()}")

    def fix_types(self):
        self.df['cmc'] = self.df['cmc'].astype(int)
        self.df['release_year'] = self.df['release_year'].astype(int)
        self.df['price'] = self.df['price'].astype(float)
        self.check_structure()
        self.check_numeric_value_bounds()
        # Gleemax has a cmc of 1000000 which really throws off usefulness
        self.df = self.df[self.df['cmc'] < 17]
        self.check_structure()
        self.check_numeric_value_bounds()

    def ingest_set_data(self):
        csv_file_path = f"{pathlib.Path(__file__).parent.absolute()}/magic_card_csv_files_by_set"
        csv_files_list = [join(csv_file_path, csv_file) for csv_file in listdir(csv_file_path) if isfile(join(csv_file_path, csv_file))]
        df = pd.concat((pd.read_csv(csv_file) for csv_file in csv_files_list), ignore_index=True)
        return df

    def make_pipeline(self,
                      # by default drop name and image columns for analysis at they are unique to a card
                      drop_columns=['name', 'image'],
                      scaler=StandardScaler(),
                      encoder=OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1),
                      model=LinearRegression()
        ):
        df_copy = self.df.copy(deep=True).drop(drop_columns, axis=1)
        dfy = df_copy['price']
        dfx = df_copy.drop(['price'], axis=1)
        print(f"ALL Columns considered {dfx.columns}")
        categorical_cols_obj = col_selector(dtype_include=object)
        categorical_features = categorical_cols_obj(df_copy)
        print(f"Categorical features: {categorical_features}")
        int_cols_obj = col_selector(dtype_include="int64")
        numeric_features = int_cols_obj(df_copy)
        print(f"Numeric features: {numeric_features}")
        np.random.seed(0)
        preprocessor = ColumnTransformer(
            transformers=[
               ('num', scaler, numeric_features),
               ('cat', encoder, categorical_features)
            ]
        )
        regression = make_pipeline(preprocessor, model)
        xtrain, xtest, ytrain, ytest = train_test_split(dfx,
                                                        dfy,
                                                        test_size=0.2,
                                                        random_state=0
        )
        regression.fit(xtrain, ytrain)
        y_hat = regression.predict(xtest)
        y_predict = regression.predict(xtrain)
        mse_test = mean_squared_error(ytest, y_hat)
        mse_train = mean_squared_error(ytrain, y_predict)
        print(f"mse test {mse_test}")
        print(f"mse train {mse_train}")
        print(f"mse ratio {mse_test/mse_train}")
        print(f"relative difference is: {np.abs(mse_train-mse_test)/mse_train}")
        print(f"r-squared test {r2_score(ytest, y_hat)}")
        print(f"r-squared train {r2_score(ytrain, y_predict)}")

    def pairplot(self):
        sns.pairplot(self.df)
        plt.show()

analyzer = CardAnalyzer()
analyzer.address_missing_data()
analyzer.fix_types()
analyzer.pairplot()
