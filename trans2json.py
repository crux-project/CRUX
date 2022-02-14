import xmltodict
import pandas as pd
import json


def xml2json(xmlfile):
    f = open(xmlfile, mode='r', encoding='utf-8')
    xpars = xmltodict.parse(f.read())
    output = xmlfile[:-6] + '.json'
    save2json(output, xpars)
    return output


# def csv2json(input, output):
#     # TODO CSV
#
#
# def asc2json(input, output):
#     # TODO ASC
#
#
# def xy2json(input, output):
#     # TODO XY
#
#
# def txt2json(input, output):
#     # TODO TXT


def xlsx2json(xlsefile, output):
    df = pd.read_excel(xlsefile, sheet_name='Heating to 650 KNN-M')
    df.drop(df.columns[[0]], axis=1, inplace=True)
    df.set_index('Angles', inplace=True)
    dic = df.to_dict()
    save2json(output, dic)


def save2json(output, dic):
    with open(output, "w") as outfile:
        json.dump(dic, outfile, indent=4)


def main():
    xmlfile = "./test/input/MnO2_Unmilled_Air_25to1100øC_1.XRDML"
    xml2json(xmlfile)

    # xlsefile = "./test/input/ExcelCompilation_KNN-M.xlsx"
    # xlse_output = "./test/output/KNN-M_xlsx.json"
    # xlsx2json(xlsefile, xlse_output)


if __name__ == "__main__":
    main()
