import ApiFileIO
import os


def load_sgg_codes():
    global sgg_codes
    code_file = os.path.abspath('./Resources/region_codes.bin')
    sgg_codes = ApiFileIO.read_binary_dict_in_dict(code_file)


def load_umds():
    global umds
    umd_file = os.path.abspath('./Resources/umd_infos.bin')
    umds = ApiFileIO.read_binary_list_in_dict(umd_file)

def get_sidos():
    return list(sgg_codes.keys())


def get_sggs(sido_nm):
    return list(sgg_codes[sido_nm].keys())

def get_umds():
    pass


sgg_codes = { }
umds = { }
load_sgg_codes()
load_umds()