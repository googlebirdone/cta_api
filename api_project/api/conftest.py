import yaml
import pytest
import os
import time

# 动态生成日志文件
# @pytest.fixture(scope="session", autouse=True)
# def manage_logs(request):
#     """Set log file name same as test name"""
#     now = time.strftime("%Y-%m-%d %H-%M-%S")
#     log_name = 'api/log/' + now + '.logs'
#
#     request.config.pluginmanager.get_plugin("logging-plugin") \
#         .set_log_path(os.path.join(log_name))


def pytest_generate_tests(metafunc):
    """ generate (multiple) parametrized calls to a test function."""
    if "param" in metafunc.fixturenames:
        metafunc.parametrize("param",
                             metafunc.cls.test_data,
                             scope="class")
