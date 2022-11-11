import yaml
import pytest
import os


# @pytest.fixture()
# def read_multi_yaml(request):
#     global multi_list
#     for yaml_file in request.param:
#         multi_list.extend(yaml.safe_load(open(yaml_file, encoding="utf8")))
#     return multi_list

def pytest_generate_tests(metafunc):
    """ generate (multiple) parametrized calls to a test function."""
    if "param" in metafunc.fixturenames:
        metafunc.parametrize("param",
                             metafunc.cls.test_data,
                             scope="class")
