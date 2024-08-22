import json


class JSON:
    def stringify(data):
        # Remove callable objects from the data. Python doesn't do this
        # automatically.
        def remove_callables(obj):
            if isinstance(obj, dict):
                return {
                    k: remove_callables(v) for k, v in obj.items() if not callable(v)
                }
            elif isinstance(obj, list):
                return [remove_callables(item) for item in obj]
            else:
                return obj

        cleaned_data = remove_callables(data)
        return json.dumps(cleaned_data)

    def parse(data):
        return json.loads(data)
