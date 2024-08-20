import sys
sys.path.append(r'E:\Other\Dev\Python\WoollySensed Software\WSS-ToolKit')

from src.WSS_ToolKit.WConfigUtils import ConfigUtils as cu


if __name__ == '__main__':
    cfg_reader = cu.BaseConfig(r'tests\config\config.cfg', use_exists_check=False).activate
    print(cfg_reader.fetch())
