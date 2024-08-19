import re


class Util:
    @staticmethod
    def remove_quote(data: dict) -> dict:
        result = {}
        for k, v in data.items():
            if isinstance(v, str):
                result[k] = re.sub('^"|"$', "", v)
            else:
                result[k] = v
        return result
