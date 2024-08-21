import logging
import os
from collections import OrderedDict

import requests


def get_notes(path: str = '', format: str = 'application/json', server: str = 'http://192.168.1.23:27123') -> str:
    """使用Local REST API插件；取回单个note或文件夹下note名列表

    Args:
        path (str, optional): 如果给定的是文件夹（需要以`/`结尾）则返回的是文件夹下所有note名列表；如果给定的是note文件名，则返回note内容. Defaults to ''.
        format: 默认是`application/json`。可以修改成`application/vnd.olrapi.note+json`
        server (_type_, optional): _description_. Defaults to 'http://192.168.1.23:27123'.

    Returns:
        str: _description_
    """
    headers = {
        'accept': format,
        'Authorization': 'Bearer 0db9f1c1d4ad38c2d3d03377ba7513bb90613191db72ed2fd1af5f47be32d8f7',
    }

    response = requests.get(f'{server}/vault/{path}', headers=headers)
    return response.text


def remove_frontmatter_property(folder_path: str, property_name: str):
    """给定的文件夹中所有后缀为.md的文件，删除frontmatter信息中给定的property

    Args:
        folder_path (str): _description_
        property_name (str): _description_
    """
    import yaml

    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r+') as f:
                content = f.read()
                try:
                    _, frontmatter, body = content.split("---\n", 2)
                    frontmatter_dict = yaml.safe_load(frontmatter)
                    frontmatter_dict.pop(property_name)
                    updated_frontmatter = yaml.dump(frontmatter_dict, sort_keys=False,
                                                    default_flow_style=False, allow_unicode=True)
                    f.seek(0)
                    f.write("---\n{}\n---\n{}".format(updated_frontmatter, body))
                except yaml.YAMLError as exc:
                    logging.error(f"Error parsing YAML in {filename}: {exc}")
                except ValueError:
                    logging.error(f"File {filename} does not appear to have a frontmatter.")


def add_frontmatter_property(
        folder_path: str, before_property: str, property_name: str, default_value: str = ""):
    """给定的文件夹中所有后缀为.md的文件，在frontmatter信息中的before_property属性之前插入新属性

    Args:
        folder_path (str): _description_
        before_property (str): _description_
        property_name (str): _description_
        default_value (str, optional): _description_. Defaults to "".
    """
    import yaml

    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r+') as f:
                content = f.read()
                try:
                    _, frontmatter, body = content.split("---\n", 2)
                    frontmatter_dict = yaml.safe_load(frontmatter)
                    # 将字典转换为 OrderedDict
                    ordered_dict = OrderedDict(frontmatter_dict)
                    # 创建一个新的 OrderedDict，并将 "Related" 插入到指定位置
                    new_ordered_dict = OrderedDict()
                    for key, value in ordered_dict.items():
                        if key == before_property:
                            new_ordered_dict[property_name] = default_value
                        new_ordered_dict[key] = value
                    updated_frontmatter = yaml.dump(
                        dict(new_ordered_dict),
                        sort_keys=False, default_flow_style=False, allow_unicode=True)
                    f.seek(0)
                    f.write("---\n{}\n---\n{}".format(updated_frontmatter, body))
                except yaml.YAMLError as exc:
                    logging.error(f"Error parsing YAML in {filename}: {exc}")
                except ValueError:
                    logging.error(f"File {filename} does not appear to have a frontmatter.")


def append_tag_frontmatter_property(folder_path: str, tag: str) -> None:
    import yaml

    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r+') as f:
                content = f.read()
                try:
                    _, frontmatter, body = content.split("---\n", 2)
                    frontmatter_dict = yaml.safe_load(frontmatter)
                    tag_list = frontmatter_dict['tags']
                    if not tag_list:
                        tag_list = []
                    tag_list.append(tag)
                    frontmatter_dict['tags'] = tag_list
                    updated_frontmatter = yaml.dump(frontmatter_dict, sort_keys=False,
                                                    default_flow_style=False, allow_unicode=True)
                    f.seek(0)
                    f.write("---\n{}\n---\n{}".format(updated_frontmatter, body))
                except yaml.YAMLError as exc:
                    logging.error(f"Error parsing YAML in {filename}: {exc}")
                except ValueError:
                    logging.error(f"File {filename} does not appear to have a frontmatter.")
