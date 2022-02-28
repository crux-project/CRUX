import xmltodict
import json
import os
import sys
sys.path.append('../peak_finding/')
import peaklist

datadir = "../data/peaklist"
PathWrap = lambda fil: os.path.join(datadir, fil)

xrdml_file = PathWrap("MnO2_Unmilled_Air_InitialScan.xrdml")
output = PathWrap('pkauto.txt')
p_gsas2 = PathWrap('p_gsas2.txt')


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


def main():
    # Transfer xrdml to json and get peak list
    json_file = xml2json(xrdml_file)
    json_dic = json2dic(json_file)
    peak_pos_sp, peak_int_sp = peaklist.auto_finding(json_dic, output)

    # Add peak list to JSON
    dic_peak = {"xrdMeasurements": {"peaks": {"positions": peak_pos_sp, "intensities": peak_int_sp}}}
    newdic = dict(dic_peak, **json_dic)
    for key in newdic.keys():
        if key in dic_peak:
            newdic[key] = dict(newdic[key], **dic_peak[key])
    save2json(xrdml_file[:-6] + '.json', newdic)

    # Validate with GSAS-II
    peaklist.val_with_gsas2(p_gsas2, peak_pos_sp, peak_int_sp)


if __name__ == "__main__":
    main()
