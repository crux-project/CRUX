import xmltodict
import os
import sys
import xml.etree.ElementTree as ET
import json
import pymongo

# sys.path.append('../model/peakfinding/temp/peak_finding/')
# import peaklist

datadir = "../testdata"
PathWrap = lambda fil: os.path.join(datadir, fil)
# xrdml_file = PathWrap("MnO2_Unmilled_Air_InitialScan.xrdml")
# output = PathWrap("pkauto.txt")
# p_gsas2 = PathWrap("p_gsas2.txt")


def xml2json(xrdml_file):
    f = open(xrdml_file, mode='r', encoding='utf-8')
    xpars = xmltodict.parse(f.read())
    output = xrdml_file[:-6] + '.json'
    save2json(output, xpars)
    return output


def save2json(output, dic):
    with open(output, "w") as outfile:
        json.dump(dic, outfile, indent=4)


def json2dic(json_file):
    f = open(json_file)
    res = f.read()
    f.close()
    dic = json.loads(res)

    return dic


# Add peak list to JSON
def add_peak(pos, int, json_dic):
    peak_pos = " "
    peak_pos = peak_pos.join(pos)
    peak_int = " "
    peak_int = peak_int.join(int)

    dic_peak = {"xrdMeasurements": {"peaks": {"positions": peak_pos, "intensities": peak_int}}}
    newdic = dict(dic_peak, **json_dic)
    for key in newdic.keys():
        if key in dic_peak:
            newdic[key] = dict(newdic[key], **dic_peak[key])
    save2json(xrdml_file[:-6] + '.json', newdic)


# Output specified item(s)/tag&values in xrdml to txt
# Data Card -> data_loc -> xrdml file -> get data -> output to .txt
def find_in_xml(xrdml_file, items, output_file=PathWrap("result.txt")):
    result = {}
    tree = ET.parse(xrdml_file)
    root = tree.getroot()

    for item in items:
        XPath = ".//{*}" + item
        result[item] = root.find(XPath).text

    f = open(output_file, 'w')
    for key, value in result.items():
        f.write('{k} :{v}\n'.format(k=key, v=value))
    f.close()


def scan_dict(dic, path="", keys=[], paths=[]):
    for key in dic:
        p = path + "/" + key
        keys.append(key)
        paths.append(p)
        if type(dic[key]) == dict:
            scan_dict(dic[key], p, keys, paths)
    return keys, paths


def dict_set(dic, path, value):
    """
    :param dic: Input dictionary.
    :param path: path to the item to be changed: "/.../.../...".
    :param value: value to be set.
    :return:
    """
    path = path.split("/")
    key = path[-1]
    for item in path[1:-1]:
        dic = dic[item]
    dic[key] = value


def import_to_mongodb(data, collection):
    """
    :param data: dict or JSON file
    :param collection: collection to import
    :return:
    """
    client = pymongo.MongoClient('localhost')
    db = client['crux']
    collection = db[collection]

    if type(data) not in (dict, list):
        with open(data) as f:
            data = json.load(f)

    if isinstance(data, list):
        instance = collection.insert_many(data)
        return instance.inserted_ids
    else:
        instance = collection.insert_one(data)
        return instance.inserted_id

    #client.close()


def get_path(folder):
    """
    Get paths of all XRDML files in folder.
    :param folder: path of the input folder.
    :return: a list of paths.
    """
    paths = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file == '.DS_Store':
                continue
            paths.append(os.path.join(root, file))

    return paths


# def main():
    # Output specified item(s) in xrdml file
    # find_in_xml(xrdml_file, ["commonPosition", "intensities"])

    # Transfer XRDML to JSON
    # json_file = xml2json(xrdml_file)

    # # Get peak list
    # json_dic = json2dic(json_file)
    # peak_pos_sp, peak_int_sp = peaklist.auto_finding(json_dic, output)

    # # Add peak list to JSON
    # add_peak(peak_pos_sp, peak_int_sp, json_dic)

    # # Validate peaks with GSAS-II
    # peaklist.val_with_gsas2(p_gsas2, peak_pos_sp, peak_int_sp)


# if __name__ == "__main__":
#     main()
