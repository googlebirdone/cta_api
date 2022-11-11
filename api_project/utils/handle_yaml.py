import yaml
import os


class HandleYaml:
    def __init__(self):
         pass

    def read_yaml(self, file):
        try:
            with open(file, encoding="utf8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            return f"发生位置错误{e},请检查输入内容"

    def write_yaml(self, file, model, data):
        try:
            with open(file, model, encoding="utf8") as f:
                yaml.safe_dump(data, f, allow_unicode=True)
        except Exception as e:
            return f"发生位置错误{e},请检查输入内容"

