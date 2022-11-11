import yaml
import json
import sys
import re


class ParserHar:
    def __init__(self, file):
        self.file = file

    def load_log_entries(self):
        try:
            with open(self.file, encoding="utf8") as f:
                return yaml.safe_load(f).get("log").get("entries")
        except Exception as e:
            print(e)
            sys.exit(1)

    def filter_url(self, url, filter_pattern=None):
        if filter_pattern:
            pat = re.compile(filter_pattern)
            if pat.search(url):
                return pat.search(url).group()
            else:
                return None
        else:
            return filter_pattern

    def split_url(self, url, split_pattern=None):
        if not split_pattern:
            return url
        else:
            return re.split(split_pattern, url)[-1]

    def load_url(self, entry):
        return entry.get("request").get("url").split(r"?")[0]

    def load_method(self, entry):
        return entry.get("request").get("method")

    def load_headers(self, entry):
        headers = {}
        for head in entry.get("request").get("headers"):
            if head['name'] == "Content-Type":
                headers.update({head['name']: head['value']})
                return headers
            else:
                continue
        return headers

    def load_params(self, entry):
        return "&".join([f"{x['name']}={x['value']}" for x in entry.get("request").get("queryString")])

    def load_postdata(self, entry):
        try:
            if entry.get("request").__contains__("postData"):
                postData = entry.get("request").get("postData")
                if "x-www-form-urlencoded" in postData.get("mimeType"):
                    form_dict = {}
                    for data in postData.get("params"):
                        form_dict[data['name']] = data['value']
                    return form_dict
                elif "json" in postData.get("mimeType"):
                    if postData.get("text").startswith(r"{"):
                        return json.loads(postData.get("text"))
                    else:
                        return postData.get("text")
        except Exception as e:
            return None

    def load_response(self, entry):
        if entry.get("response").get("content").get("text").startswith(r"{"):
            return json.loads(entry.get("response").get("content").get("text"))
        else:
            return entry.get("response").get("content").get("text")
