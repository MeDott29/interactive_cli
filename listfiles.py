from openai import OpenAI

client = OpenAI()

from typing import List, Any

def get_files(limit: int = 5) -> List[Any]:
    files = client.files.list()
    files = files.data
    files = sorted(files, key=lambda x: x.created_at, reverse=True)
    return files[:limit]