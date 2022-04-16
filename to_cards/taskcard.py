import argparse
import utils


def task_card():
    parser = argparse.ArgumentParser(description='Generate a Task Card.')

    parser.add_argument("taskName",
                        metavar="task_name",
                        help="Name of the task"),

    parser.add_argument("-if", "--input_format",
                        dest="inputFormat",
                        help="File format of the input, e.g., xrdml and csv.")

    parser.add_argument("-of", "--output_format",
                        dest="outputFormat",
                        help="File format of the input, e.g., txt and csv.")

    parser.add_argument("-ip", "--input_parameters",
                        nargs='+',
                        dest="inputParameters",
                        help="Parameters needed for this task.")

    parser.add_argument("-op", "--output_parameters",
                        nargs='+',
                        dest="outputParameters",
                        help="Parameters to be outputted by this task.")

    args = parser.parse_args()

    return vars(args)


def main():
    # Generate a task card.
    taskcard = task_card()

    # Import the generated task card to MongoDB.
    collection = "taskcard"
    utils.import_to_mongodb(taskcard, collection)


if __name__ == "__main__":
    main()


