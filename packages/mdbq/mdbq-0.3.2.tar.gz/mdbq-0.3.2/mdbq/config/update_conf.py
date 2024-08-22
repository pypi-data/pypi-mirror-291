# -*- coding: UTF-8 –*-
import platform
import getpass
import configparser
import os
from urllib import parse


class UpdateConf:
    """
    读取配置文件信息
    理论上，在本程序的根目录需要有一个文件夹 support/.myconf 配置文件放在其下
    """
    def __init__(self, filename):
        if platform.system() == 'Darwin':
            path = os.path.join('/Users', getpass.getuser(), '数据中心/自动0备份/py/数据更新/support')
        elif platform.system() == 'Windows':
            path = os.path.join('C:\\同步空间\\BaiduSyncdisk\\自动0备份\\py\\数据更新\\support')
        else:
            path = os.path.join('/Users', getpass.getuser(), 'support')
        self.path = path
        self.filename = filename
        self.conf_file = os.path.join(self.path, self.filename)
        self.config = None
        self.section = 'database'


    def read_conf(self, option, value):
        if not os.path.exists(self.conf_file):
            print(f'缺少配置文件')
            return
        self.config = configparser.ConfigParser()
        self.config.read(self.conf_file, 'UTF-8')
        res = self.config.get('database', option)
        print(res)

    def update_config(self, option, new_value):
        """ 更新配置文件 """
        with open(self.conf_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        config = configparser.ConfigParser(allow_no_value=True)  # 读取配置（不包括注释和空白行）
        config.read_string(''.join(line for line in lines if not line.strip().startswith('#') and line.strip()))
        in_section = False  # 标记是否在当前section内

        with open(self.conf_file, 'w', encoding='utf-8') as file:  # 写入更新后的配置文件
            for line in lines:
                if line.strip().startswith('[') and line.strip().endswith(']'):  # 检查是否是section的开始
                    section_name = line.strip()[1:-1]
                    if section_name == self.section:
                        in_section = True
                    file.write(line)
                    continue
                if in_section and '=' in line:  # 如果在section内，检查是否是配置项
                    option_name, _, _ = line.strip().partition('=')
                    if option_name.strip() == option:
                        file.write(f"{option} = {new_value}\n")  # 更新配置项
                        continue
                file.write(line)  # 如果不是配置项或不在section内，则保留原样（包括注释和空白行）

            if not config.has_option(self.section, option):  # 如果配置项没有在当前section中找到，则添加它
                for i, line in enumerate(lines):  # 假设我们要在section的末尾添加配置项
                    if line.strip().startswith(f'[{self.section}]'):
                        file.write(f"{option} = {new_value}\n")  # 写入配置项到section之后
                        break
                else:
                    # 如果section不存在，则在文件末尾添加新的section和配置项
                    file.write(f"\n[{self.section}]\n{option} = {new_value}\n")


if __name__ == '__main__':
    # w = UpdateConf(filename='.copysh_conf')
    # w.update_config(option='ch_record', new_value='false')
    pass
