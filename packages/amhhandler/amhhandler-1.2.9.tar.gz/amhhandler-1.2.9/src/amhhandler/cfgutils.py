#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ================================
# Author: nbyue
# Date: 2024/3/12 19:57
# Path: .../AmhHandler/src/amhhandler
# File: cfgutils.py
# Describe:
# ================================


import sys
import os

from configparser import ConfigParser


class ConfigUtils(object):
    def __init__(self, config_file, encode="utf-8"):
        if os.path.exists(config_file):
            self.__cfg_file = config_file
        else:
            # 此处做其他异常处理或创建配置文件操作
            sys.exit("配置文件不存在!")
        self.__config = ConfigParser()
        self.__config.read(config_file, encoding=encode)

    # 获取配置文件的所有section
    def get_sections(self):
        return self.__config.sections()

    # 获取指定section的所有option
    def get_options(self, section_name):
        if self.__config.has_section(section_name):
            return self.__config.options(section_name)
        else:
            raise ValueError(section_name)

    # 获取指定section下option的value值
    def get_option_value(self, section_name, option_name):
        if self.__config.has_option(section_name, option_name):
            return self.__config.get(section_name, option_name)

    # 获取指定section下的option的键值对
    def get_all_items(self, section):
        if self.__config.has_section(section):
            return self.__config.items(section)

    # 打印配置文件所有的值
    def print_all_items(self):
        for section in self.get_sections():
            print("[" + section + "]")
            for K, V in self.__config.items(section):
                print(K + "=" + V)

    # 增加section
    def add_new_section(self, new_section):
        if not self.__config.has_section(new_section):
            self.__config.add_section(new_section)
            self.__update_cfg_file()

    # 增加指定section下option
    def add_option(self, section_name, option_key, option_value):
        if self.__config.has_section(section_name):
            self.__config.set(section_name, option_key, option_value)
            self.__update_cfg_file()

    # 删除指定section
    def del_section(self, section_name):
        if self.__config.has_section(section_name):
            self.__config.remove_section(section_name)
            self.__update_cfg_file()

    # 删除指定section下的option
    def del_option(self, section_name, option_name):
        if self.__config.has_option(section_name, option_name):
            self.__config.remove_option(section_name, option_name)
            self.__update_cfg_file()

    # 更新指定section下的option的值
    def update_option_value(self, section_name, option_key, option_value):
        if self.__config.has_option(section_name, option_key):
            self.add_option(section_name, option_key, option_value)

    # 私有方法:操作配置文件的增删改时，更新配置文件的数据
    def __update_cfg_file(self):
        with open(self.__cfg_file, "w") as f:
            self.__config.write(f)
