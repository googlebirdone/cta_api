from api_project.utils.handle_yaml import HandleYaml
from api_project.utils.utils import Utils
import requests
import pytest,  allure, logging, os


class TestMakeRequest:

    test_data = []
    token = None
    root_path = r"D:\Code\api_project\resource"
    for yaml_file in os.listdir(root_path):
        if yaml_file.endswith("list.yaml"):
            test_data.extend(HandleYaml().read_yaml(os.path.join(root_path, yaml_file)))

    # def test_login(self, param):
    #     print(param)
    #     r = requests.session().request(**param["request"])
    #     print(r.text)
    # @pytest.mark.parametrize("read_multi_yaml", test_data)
    @allure.title("{param[name]}")
    def test_request(self, param):

        host_port = "192.168.103.11"
        global token
        url = eval(param.get("request").get("url"))
        # print(url)
        method = param.get("request").get("method")
        header = param.get("request").get("headers")
        data = param.get("request").get("body")
        params = param.get("request").get("params")
        name = param.get("request").get("name")
        response = param.get("response")
        if header.get("token") is not None:
            header.update({"token": token[0]})
            logging.info(f"****{header}")

        res = Utils.request_with_type(method, url, header=header, data=data, params=params)
        if response.get("extract") is not None:
            token = Utils.load_token(response.get('extract'), res.json())

        Utils.validate_value_assume(response, res)
        # Utils.validate_value_assume(response.get("status"), res.status_code)
        # if isinstance(response.get("text"), dict):
        #     Utils.validate_value_assume(response.get("text").get("msg"), res.json().get("msg"))
        #     if isinstance(response.get("text").get('data'), dict):
        #         for k, v in response.get("text").get('data').items():
        #             if k.startswith("$"):
        #                 Utils.validate_value_assume(v, Utils.json_path(res.json(), k))


if __name__ == "__main__":
    pytest.main(["make_request.py", "-s", "-v", "--alluredir", "../report", "--clean-alluredir"])
