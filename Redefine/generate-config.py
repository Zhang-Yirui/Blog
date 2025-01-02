import json
import os

import requests
from ruamel.yaml import YAML
from tqdm import tqdm


def download(file_url, file_path, chunk_size=8192):
    resp = requests.head(file_url)
    resp.raise_for_status()
    file_size = int(resp.headers.get('content-length', 0))  # 获取文件大小（字节）
    with requests.get(file_url, stream=True) as resp:
        resp.raise_for_status()  # 检查请求是否成功
        with open(file_path, 'wb') as f:
            with tqdm(total=file_size, unit='B', unit_scale=True, desc="Downloading") as pbar:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    pbar.update(len(chunk))  # 更新进度条
    print(f"文件 `{file_path}` 下载完成")


def download_pandoc():
    # 获取 Pandoc 的最新版本号
    api_url = "https://api.github.com/repos/jgm/pandoc/releases/latest"
    resp = requests.get(api_url)
    resp.raise_for_status()  # 确保请求成功
    pandoc_version = resp.json().get("tag_name", "3.6")
    print(f"Pandoc 版本: v{pandoc_version}")
    file_name = f"pandoc-{pandoc_version}-1-amd64.deb"
    download_url = f"https://github.com/jgm/pandoc/releases/download/{pandoc_version}/{file_name}"
    resp = requests.head(download_url)
    resp.raise_for_status()
    url = resp.headers.get('Location', '')
    download(url, os.path.join('./', file_name))


def update_config(old, new):
    for key, value in new.items():
        if isinstance(value, dict) and value is not None:
            update_config(old.get(key, {}), value)  # 如果是字典，递归遍历
        else:
            old[key] = value  # 如果是基本类型，直接更新 config


if __name__ == "__main__":
    try:
        # 生成配置文件
        yaml = YAML(typ='rt')
        with open("_config.yml", "r", encoding="utf8") as f1:
            blog_config = yaml.load(f1)

        with open("_config.redefine.yml", "r", encoding="utf8") as f1:
            theme_config = yaml.load(f1)
            home_banner_subtitle_text = theme_config.get("home_banner", {}).get("subtitle", {}).get("text", [])
            result = requests.get("https://api.bd3qif.com/api/v3/getNowDateInfoStr")
            if result.status_code == 200:
                home_banner_subtitle_text.append(result.json().get('date', None))

        with open("config.json", "r", encoding="utf8") as file:
            my_config = json.load(file)

        for config in my_config.get("configs", []):
            config.get('theme-config', {}).get('home_banner', {}).get('subtitle', {})['text'] = home_banner_subtitle_text
            path_dir = config.get("blog-url", ".")
            os.makedirs(path_dir, exist_ok=True)
            update_config(blog_config, config.get("blog-config", dict()))
            file_path = os.path.join(path_dir, my_config.get("config-name", "_config.yml"))
            yaml.dump(blog_config, open(file_path, "w", encoding="utf8"))
            update_config(theme_config, config.get("theme-config", dict()))
            file_path = os.path.join(path_dir, my_config.get("theme-config-name", "_config.redefine.yml"))
            yaml.dump(theme_config, open(file_path, "w", encoding="utf8"))
        # 下载 Pandoc
        download_pandoc()
        github_output = os.getenv('GITHUB_OUTPUT')
        with open(github_output, "r") as f:
            for line in f:
                print(line)
            
    except Exception as e:
        print(f"配置文件解析失败: {e}")
