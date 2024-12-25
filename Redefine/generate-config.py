# pip install ruamel.yaml
import json
import os

import requests
from ruamel.yaml import YAML


def update_config(old, new):
    for key, value in new.items():
        if isinstance(value, dict) and value is not None:
            update_config(old.get(key, {}), value)  # 如果是字典，递归遍历
        else:
            old[key] = value  # 如果是基本类型，直接更新 config


if __name__ == "__main__":
    yaml = YAML(typ='rt')
    with open("./_config.yml", "r", encoding="utf8") as f1:
        blog_config = yaml.load(f1)

    with open("./_config.redefine.yml", "r", encoding="utf8") as f1:
        theme_config = yaml.load(f1)
        home_banner_subtitle_text = theme_config.get("home_banner", {}).get("subtitle", {}).get("text", [])
        result = requests.get("https://api.bd3qif.com/api/v3/getNowDateInfoStr")
        if result.status_code == 200:
            home_banner_subtitle_text.append(result.json().get('date', None))

    with open("./config.json", "r", encoding="utf8") as file:
        my_config = json.load(file)

    for config in my_config.get("configs", []):
        config.get('theme-config', {}).get('home_banner', {}).get('subtitle', {})['text'] = home_banner_subtitle_text
        path_dir = config.get("blog-url", ".")
        os.makedirs(path_dir, exist_ok=True)
        update_config(blog_config, config.get("blog-config", dict()))
        file_path = os.path.join("./", path_dir, my_config.get("config-name", "_config.yml"))
        yaml.dump(blog_config, open(file_path, "w", encoding="utf8"))
        update_config(theme_config, config.get("theme-config", dict()))
        file_path = os.path.join("./", path_dir, my_config.get("theme-config-name", "_config.redefine.yml"))
        yaml.dump(theme_config, open(file_path, "w", encoding="utf8"))
