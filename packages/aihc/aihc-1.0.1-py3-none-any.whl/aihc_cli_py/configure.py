import configparser
import os
from .aihc_argumentparser import config_file

host_dict = {
    'cn-beijing' : 'aihc.bj.baidubce.com',
    'cn-baoding' : 'aihc.bd.baidubce.com',
}


# 保存配置
def save_config(access_id, access_key, region, username, password):
    """保存配置到文件"""
    config_dir = config_file.parent
    if not config_dir.exists():
        os.makedirs(config_dir)

    config = configparser.ConfigParser()
    config.read(config_file)

    if not config.has_section('default'):
        config.add_section('default')
    if not config.has_section('image-repo'):
        config.add_section('image-repo')

    if access_id is not None:
        config.set('default', 'access_id', access_id)
    if access_key is not None:
        config.set('default', 'access_key', access_key)
    if region is not None:
        config.set('default', 'region', region)
        config.set('default', 'host', host_dict[region])
    else:
        if not config.has_option('default', 'region'):
            config.set('default', 'region', 'cn-beijing')
            config.set('default', 'host', host_dict['cn-beijing'])

    if username is not None:
        config.set('image-repo', 'username', username)
    if password is not None:
        config.set('image-repo', 'password', password)

    with open(config_file, 'w') as configfile:
        config.write(configfile)

    return "Configuration saved to: ~/.aihc/config"


def get_ak_sk(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    try:
        ak = config.get('default', 'access_id')
        sk = config.get('default', 'access_key')
        host = config.get('default', 'host')
    except (configparser.NoSectionError, configparser.NoOptionError):
        return None, None, None

    return ak, sk, host


def get_username_password(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    try:
        username = config.get('image-repo', 'username')
        password = config.get('image-repo', 'password')
    except (configparser.NoSectionError, configparser.NoOptionError):
        return None, None

    return username, password

