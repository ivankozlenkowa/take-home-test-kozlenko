import pytest
from fastapi.testclient import TestClient

from main import app


class TestCompensationData:
    client = TestClient(app)

    @pytest.mark.parametrize(
        'query_params, expected_status_code',
        (
                ({}, 200),  # no filters/parameters
                ({'Timestamp[gte]': '01/01/2024'}, 200),  # filter by single parameter
                ({'sort': 'Company Name,Timestamp'}, 200),  # sort by multiple columns
                ({'Company Name[ne]': 'Abc123'}, 200),  # "ne" operator for text column
                ({
                     'fields': 'Timestamp,Employment Type,Company Name,Total Base Salary in 2018 (in USD)',
                     'Total Base Salary in 2018 (in USD)[lte]': '24000',
                     'Timestamp[gt]': '2019-09-11T05:24:53',
                     'sort': 'Company Name'
                 }, 200),  # multiple parameters, subset of columns, sorting
                ({'fields': 'asdf_some_unknown_field'}, 404),  # unknown field yields 404
                ({'Company Name[gte]': 'abc'}, 400),  # comparison params are allowed only for numeric or date columns
        )
    )
    def test_compensation_data(self, query_params: dict, expected_status_code: int):
        resp = self.client.get('/compensation_data/', params=query_params)
        assert resp.status_code == expected_status_code, resp.json()

    def test_compensation_data_columns(self):
        resp = self.client.get('/compensation_data/columns/')
        assert resp.status_code == 200, resp.json()
