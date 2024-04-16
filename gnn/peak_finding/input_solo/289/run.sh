# Change output path in #l97 and l100
python3 data.py  "../../content/data/xrdml" &> ./289/data2xy.txt

# Change Jade path in l58
python3 groundtruth.py  "../../content/xy/xrdml"

# Change l97 i = start number
python3 model.py "../../content/xy/xrdml" &> ./289/input/edge.txt


