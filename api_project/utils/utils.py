from jsonpath import jsonpath


class Utils:
    @classmethod
    def json_path(cls, json_object, expr):
        return jsonpath(json_object, expr)
