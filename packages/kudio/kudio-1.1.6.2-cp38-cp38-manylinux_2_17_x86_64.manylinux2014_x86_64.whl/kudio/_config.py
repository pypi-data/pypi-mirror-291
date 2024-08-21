# -*- coding: utf-8 -*-
import os
import yaml
from pprint import pprint
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

__all__ = ['kudio_params', 'load_config', 'write_config']

"""
A. 自定參數 
    1. import kudio
    2. 預設產生一個變數 kudio.kudio_params
    3. 使用者可以藉由 from kudio import kudio_params 使用此參數

    - kudio_params 包含了 kudio 運行時的所有必要參數

B. 將kudio_params 輸出 kudio.yaml ：
    >>> kudio.write_config(kudio.kudio_params) 
    或
    >>> kudio.write_config(kudio.kudio_params, file = 'kudio.yaml')

C. kudio.load_config 可以讀取任何 .yaml檔案, 輸出為一字典
    >>> _dict = kudio.load_config('kudio.yaml')

D. 若要使用 kudio.load_config 更新 kudio_params, 檔案格式須包含 kudio 運行時所需參數
    >>> kudio_params = load_config('kudio.yaml')

E. 使用者如何自定義參數？
    ** 若要使用 kudio.load_config 更新 kudio_params, 檔案格式須包含 kudio 運行時所需參數
    1. 參考 B. 使用 kudio.write_config 輸出 kudio.yaml 於當前目錄下
    2. 產生kudio.yaml後, 可對文件內參數值進行修改
    3. 重新運行python, import kudio , kudio 預設會讀取此檔名為 kudio.yaml 的檔案

F. 使用者如何在一開始讓kudio讀取指定yaml路徑？
    1. 在當前專案路徑下建立.env 
    2. 加入 kudio_config=<yaml路徑>.yaml
    3. import kudio 之後顯示 [kudio] Load → <yaml路徑>.yaml

"""


def write_config(data, file: str = 'kudio.yaml') -> None:
    """
    write yaml file

    Parameters:
        data: dict, KudioConfig

        file : str
    """
    with open(str(file), 'w') as f:
        yaml.dump(data, f)


def load_config(config_file_dir: str = 'kudio.yaml'):
    """
    load yaml file

    Parameters:
        config_file_dir : str

    Returns:
        dict


    """
    _file = Path(config_file_dir)
    if Path(_file).is_file():
        print(f"[kudio] Load → {_file.resolve()}")
        with open(str(_file), encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.UnsafeLoader)
        return data
    else:
        print("[kudio] Use Default Parameter")
        data = {
            "config": {'kudio.yaml'},
            "connections": {
                "base": {
                    'engine': 'tortoise.backends.mysql',
                    "credentials": {
                        'host': os.getenv('BASE_HOST', '127.0.0.1'),
                        'user': os.getenv('BASE_USER', 'root'),
                        'password': os.getenv('BASE_PASSWORD', '123456'),
                        'port': int(os.getenv('BASE_PORT', 3306)),
                        'database': os.getenv('BASE_DB', 'base'),
                    }
                },
            },
            "apps": {
                "base": {"models": ["models.base"], "default_connection": "base"},
                # "db2": {"models": ["models.db2"], "default_connection": "db2"},
                # "db3": {"models": ["models.db3"], "default_connection": "db3"}
            },
            'use_tz': False,
            'timezone': 'Asia/Shanghai',

            'waveform': {'type': '.wav',
                         'default_rate': 16000,
                         'common_rate': [192000, 96000, 88200, 64000, 48000, 44100,
                                         32000, 22050, 16000, 11025, 8000, 6000],
                         'resample_rate': 16000,
                         'channels': 'mono',
                         'format': '16bit'},
            'device': {'pool_max': 200, 'cpu_cores': 8},
            'train': {'overwrite': True, 'clean': 'data/train/clean'},
            'test': {'noisy': 'data/test/noisy'},
            'syn': {'overwrite': False,
                    'noise': 'data/train/noise',
                    'snr_range': [-5, 0, 5],
                    'method': 'regular',
                    'bkg_noise': 'data/backgroundnoise',
                    'snr_bkg': [5]},
            'denoise': {'overwrite': True,
                        'train': True,
                        'eval': False,
                        'method': ['ddae', 'lstm', 'acap']},
            'model': {'path': 'models',
                      'dnn_size': [512, 512, 512],
                      'NOEFE_ENH': [150, 200],
                      'DNN_ENH': 10,
                      'LSTM_ENH': 10,
                      'ACAPELLA_ENH': 10,
                      'DNN_CLA': 10,
                      'CNN_CLA': 10,
                      'sVGG_CLA': 10,
                      'LSTM_CLA': 10},
            'global': {'train': True,
                       'test': True,
                       'feature': ['mfcc', 'logspec'],
                       'classify': ['DNN', 'CNN', 'sVGG', 'LSTM'],
                       'desired_samples': 32000,
                       'advanced': False,
                       'wanted_score': 93},
            'default': {'runs_path': 'runs',
                        'denoise': ['none', 'trad', 'ddae', 'lstm', 'acap', 'wavelet', 'tradwavelet', 'noefe'],
                        'feature': ['mfcc', 'logspec'],
                        'classify': ['DNN', 'CNN', 'sVGG', 'LSTM', 'CNN1', 'CNN2']}
        }
        return KudioConfig(**data)


class KudioConfig(yaml.YAMLObject):
    """ KudioConfig
    ------------
    Return KudioConfig
    ------------

    ------------
    kcf = KudioConfig(**(data))
    for k, v in kcf.__dict__.items():
        print(k)

    kcf.connections.__dict__
    kcf.connections.base.__dict__
    kcf.connections.base.credentials.__dict__
    kcf.connections.base.credentials.host
    print(kcf.connections.base.credentials.host)
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        for key, value in self.__dict__.items():
            if isinstance(self.__dict__[key], dict):
                self.__dict__[key] = KudioConfig(**value)

    def keys(self):
        print(self.__dict__.keys())


kudio_params = load_config(os.getenv('kudio_config', 'kudio.yaml'))

if __name__ == '__main__':
    def kprint(d):
        pprint(vars(d))


    kcf = load_config(os.getenv('kudio_config', 'kudio.yaml'))
    kprint(kcf)
    kprint(kcf.connections)
    kprint(kcf.connections.base)
    kprint(kcf.connections.base.credentials)
    print(kcf.connections.base.credentials.password)
    print(kcf.connections.base.credentials.host)
