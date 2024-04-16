## Change output path in #l97 and l100
#python3 data.py  "../../content/data_all/xrdml" &> ./3823/data2xy.txt
#
## Change Jade path in l58
#python3 groundtruth.py  "../../content/xy_all/xrdml"

# Change l97 i = start number
python3 model.py "../../../content/xy_all/xrdml" &> ./3823/input/edge.txt
