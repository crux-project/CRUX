import os


# Download metadata/datacard of dataset from Kaggle
def download(dataset):
    command = "kaggle datasets metadata " \
              + dataset \
              + " -p /Volumes/YING/CRUX/Kaggle/results/" \
              + dataset.replace("/", "\:")
    os.system(command)


def main():
    # Read datasets from datalist.txt
    f = open("../resources/datalist.txt")
    datasets = f.read().splitlines()

    # Download datacards for each dataset
    for dataset in datasets:
        download(dataset)
    f.close()


if __name__ == "__main__":
    main()
