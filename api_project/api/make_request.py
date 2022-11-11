from api_project.utils.handle_yaml import HandleYaml
from api_project.utils.utils import Utils
import requests
import pytest, yaml, allure, logging, os


class TestMakeRequest:

    session = requests.Session()
    test_data = []
    root_path = r"D:\Code\api_project\resource"
    for yaml_file in os.listdir(root_path):
        if yaml_file.endswith(".yaml"):
            test_data.extend(HandleYaml().read_yaml(os.path.join(root_path, yaml_file)))

    # def test_login(self, param):
    #     print(param)
    #     r = requests.session().request(**param["request"])
    #     print(r.text)
    # @pytest.mark.parametrize("read_multi_yaml", test_data)
    @allure.title("{param[name]}")
    def test_request(self, param):
        print(param)
        url = param.get("request").get("url")
        method = param.get("request").get("method")
        header = param.get("request").get("headers")
        data = param.get("request").get("body")
        params = param.get("request").get("params")
        name = param.get("request").get("name")
        response = param.get("response")

        # @allure.title(name)
        # def test_make_request():
        if method == "GET":
            res = TestMakeRequest.session.request(method, url, params=params)
        else:
            if "json" in header.get("Content-Type"):
                res = TestMakeRequest.session.request(method, url, headers=header, json=data)
            else:
                res = TestMakeRequest.session.request(method, url, headers=header, data=data)

        pytest.assume(res.status_code == response.get("status"))
        if type(response.get("text")) == dict:
            logging.info(f'接口结果:{res.json().get("msg")} VS 接口预期:{response.get("text").get("msg")}')
            assert res.json().get("msg") == response.get("text").get("msg")


if __name__ == "__main__":
    pytest.main(["make_request.py", "-s", "-v", "--alluredir", "../report", "--clean-alluredir"])
