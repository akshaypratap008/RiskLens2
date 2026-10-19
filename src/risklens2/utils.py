from pathlib import Path
import yaml

def load_prompt(file_path: str) -> dict:
    with open(file_path, "r") as file:
        prompt = yaml.safe_load(file)
        return prompt