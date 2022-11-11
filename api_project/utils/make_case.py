from api_project.utils.handle_yaml import HandleYaml
from api_project.utils.parser_har import ParserHar
from copy import deepcopy


class GenerateCase:
    case_dict_model = {
        "name": "",
        "request": {
            "headers": "",
            "url": "",
            "method": "",
            "body": "",
            "params": ""
        },
        "response": {}
    }

    def __init__(self, har_file):
        self.file = har_file
        self.yaml = HandleYaml()
        self.parser = ParserHar(self.file)
        self.entries = self.parser.load_log_entries()
        self.case_dict_list = []

    def make_request(self, entry, case_dict: dict):
        url = self.parser.load_url(entry)
        method = self.parser.load_method(entry)
        headers = self.parser.load_headers(entry)
        if method == "GET":
            params = self.parser.load_params(entry)
            body = ""
        else:
            body = self.parser.load_postdata(entry)
            params = ""
        case_dict.get("request")["url"] = url
        case_dict.get("request")["method"] = method
        case_dict.get("request")["headers"] = headers
        case_dict.get("request")["body"] = body
        case_dict.get("request")["params"] = params

    def make_response(self, entry, case_dict: dict, key_words: tuple):
        case_dict["response"].update(**{
            "status": entry.get("response").get("status"),
            "text": self.parser.load_response(entry)
        })

    def make_step_name(self, entry, case_dict: dict):
        url = self.parser.load_url(entry)
        case_dict["name"] = self.parser.split_url(url, r'/')

    # 想不起来当初要干啥
    def package_case_dict(self, yaml_file):
        for entry in self.entries:
            case_dict = deepcopy(GenerateCase.case_dict_model)
            url = self.parser.load_url(entry)
            if not self.parser.filter_url(url, r'^ws|static|inputdata'):
                self.make_step_name(entry, case_dict)
                self.make_request(entry, case_dict)
                self.make_response(entry, case_dict, ("ret", "msg", "data"))
                self.case_dict_list.append(case_dict)
        self.yaml.write_yaml(yaml_file, "w+", self.case_dict_list)


if __name__ == "__main__":
    generate = GenerateCase(r"D:\Code\api_project\resource\192.168.103.111_analyse.har")
    generate.package_case_dict(r"D:\Code\api_project\resource\192.168.103.111_analyse.yaml")

















