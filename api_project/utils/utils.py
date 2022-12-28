from jsonpath import jsonpath
from requests import Session
import pytest,logging


class Utils:
    session = Session()
    @classmethod
    def json_path(cls, json_object, expr):
        return jsonpath(json_object, expr)

    @classmethod
    def extract_value(cls, ):
        pass

    @classmethod
    def request_with_type(cls, *args, **kwargs):
        if "GET" in args:
            res = cls.session.request(*args, params=kwargs['params'])
        else:
            if "json" in kwargs.get('header').get("Content-Type"):
                res = cls.session.request(*args, headers=kwargs.get('header'), json=kwargs.get('data'))
            else:
                res = cls.session.request(*args, headers=kwargs.get('header'), data=kwargs.get('data'))
        return res

    @classmethod
    def load_token(cls, tips, res):
        if tips is not None:
            return Utils.json_path(res, tips)

    @classmethod
    def validate_value_assume(cls, expect_res, actual_res):
        # logging.info(f'接口预期:{expect_value} VS 接口结果:{actual_value}')
        pytest.assume(expect_res.get("status") == actual_res.status_code)
        if isinstance(expect_res.get("text"), dict):
            logging.info(f'接口预期:{expect_res.get("text").get("msg")} VS 接口结果:{actual_res.json().get("msg")}')
            pytest.assume(expect_res.get("text").get("msg") == actual_res.json().get("msg"))
            if isinstance(expect_res.get("text").get('data'), dict):
                for k, v in expect_res.get("text").get('data').items():
                    if k.startswith("$"):
                        pytest.assume(v == Utils.json_path(actual_res.json(), k))
