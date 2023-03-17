import re

import pandas as pd
import numpy as np
from fastapi import Request, HTTPException


class CompensationDataHandler:
    def __init__(self, data_path: str):
        self.dataset = self._preprocess_data(data_path)
        self.dataset_cols = list(self.dataset.columns)
        self.fixed_params = ['sort', 'fields']
        self.numeric_columns = [
            "Total Base Salary in 2018 (in USD)",
            "Total Bonus in 2018 (cumulative annual value in USD)",
            "Total Stock Options/Equity in 2018 (cumulative annual value in USD)"
        ]
        self.datetime_columns = ['Timestamp']
        self.param_pattern = r'\[\w+\]'
        self.known_params = ['lt', 'lte', 'gt', 'gte', 'ne', 'eq']

    @staticmethod
    def _preprocess_data(data_path: str) -> pd.DataFrame:
        """
        Preprocessing:
         - remove "NaN"
         - cast "Timestamp" column to proper data type
        """
        df = pd.read_csv(data_path)
        df = df.replace({np.nan: None})
        df = df.dropna()
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df

    def _df_where(self, df: pd.DataFrame, col_name: str, param: str, value: str) -> pd.DataFrame:
        self._validate_columns_exist(col_name)
        try:
            if col_name in self.numeric_columns:
                value = pd.to_numeric(value)
            elif col_name in self.datetime_columns:
                value = pd.to_datetime(value)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f'Requested value {value} does not match data type of column {col_name}: {df[col_name].dtype}; '
                       f'exception: {e}'
            )
        match param:
            case 'eq':
                df = df[df[col_name] == value]
            case 'gt':
                df = df[df[col_name] > value]
            case 'gte':
                df = df[df[col_name] >= value]
            case 'lt':
                df = df[df[col_name] < value]
            case 'lte':
                df = df[df[col_name] <= value]
            case 'ne':
                df = df[df[col_name] != value]
        return df

    def _filter_fields(self, df: pd.DataFrame, fields: str) -> pd.DataFrame:
        fields = self._validate_columns_exist(fields)
        return df[fields]

    def _process_conditional_param(self, df: pd.DataFrame, param_k: str, param_v: str) -> pd.DataFrame:
        if found_param := re.findall(self.param_pattern, param_k):
            # trying to extract comparison parameter from query, e.g. salary[gte] -> parameter "gte"
            if len(found_param) > 1:
                raise HTTPException(status_code=400, detail=f'Invalid filter parameter(s): {found_param}')
            else:
                found_param = found_param[0]

                # split() used over strip() since it causes bug with case like param_k = 'Company Name[gte]'
                # which turns into 'Company Nam' after stripping '[gte]'
                column = param_k.split(found_param)[0]
                self._validate_columns_exist(column)
                found_param = found_param.strip('[]')
                if found_param not in ['eq', 'ne'] and column not in self.numeric_columns + self.datetime_columns:
                    # do not allow operators such as 'gte', 'lte' for non-numeric or non-datetime columns
                    raise HTTPException(
                        status_code=400,
                        detail=f'Column {column} does not support comparison operators'
                    )
                if found_param not in self.known_params:
                    raise HTTPException(
                        status_code=400,
                        detail=f'Unknown filter parameter: {found_param}; valid values: {self.known_params}'
                    )
                else:
                    df = self._df_where(df, column, found_param, param_v)
        else:
            # no parameter present in query - by default assume parameter as "equals to"
            df = self._df_where(df, param_k, 'eq', param_v)
        return df

    def _sort_values(self, df: pd.DataFrame, sort_cols: str) -> pd.DataFrame:
        # TODO: different sort orders are not implemented, default - ASC
        sort_cols = self._validate_columns_exist(sort_cols)
        return df.sort_values(by=sort_cols)

    def _validate_columns_exist(self, columns: str) -> list[str]:
        columns = columns.split(',')
        unknown_cols = [col for col in columns if col not in self.dataset_cols]
        if unknown_cols:
            raise HTTPException(status_code=404, detail=f'Unknown column(s): {", ".join(unknown_cols)}')
        else:
            return columns

    def handle(self, request: Request) -> list[dict]:
        df = self.dataset
        query_params = dict(request.query_params)
        conditional_params = {k: v for k, v in query_params.items() if k not in self.fixed_params}
        for param_k, param_v in conditional_params.items():
            df = self._process_conditional_param(df, param_k, param_v)

        if sort_cols := query_params.get('sort'):
            df = self._sort_values(df, sort_cols)

        # select subset of fields/columns
        if fields := query_params.get('fields'):
            df = self._filter_fields(df, fields)
        return df.to_dict(orient='records')
