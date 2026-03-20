import json

def pretty_json(data):
    """
    Pretty-print JSON data with indentation.
    Safely converts Python dict/list to formatted JSON string.
    """
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        return f"Invalid JSON data: {e}"