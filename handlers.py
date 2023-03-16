import pandas as pd
import numpy as np
from fastapi import Request, HTTPException


class CompensationDataHandler:
    def __init__(self, data_path: str):
        self.dataset = self._preprocess_data(data_path)
        self.dataset_cols = list(self.dataset.columns)
        self.fixed_params = ['sort', 'fields']

    @staticmethod
    def _preprocess_data(data_path: str) -> pd.DataFrame:
        '''
        Preprocessing:
         - remove "NaN"
        '''
        df = pd.read_csv(data_path)
        df = df.replace({np.nan: None})
        return df

    def _filter_fields(self, df: pd.DataFrame, fields: str) -> pd.DataFrame:
        fields = self._validate_columns_exist(fields)
        return df[fields]

    def _process_conditional_param(self, df: pd.DataFrame, param_k: str, param_v: str) -> pd.DataFrame:
        # TODO: create WHERE filters, e.g. ?salary[gte]=120000&primary_location=Portland
        raise NotImplementedError

    def _sort_values(self, df: pd.DataFrame, sort_cols: str) -> pd.DataFrame:
        sort_cols = self._validate_columns_exist(sort_cols)
        return df.sort_values(by=sort_cols)  # TODO: sort order not implemented, default - ASC

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
        if fields := query_params.pop('fields'):
            df = self._filter_fields(df, fields)
        return df.to_dict(orient='records')
