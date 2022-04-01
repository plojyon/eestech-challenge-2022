import os
from csv import reader
import threading
from typing import List

from utils.utils import convert_date_to_seconds, convert_json_data_to_dataframe, evaluate, read_json


class RunWithTimeout(object):
    """
    This class is used for running a function in a seperate thread with
    predfined timeout.
    """

    def __init__(self, function, args):
        self.function = function
        self.args = args
        self.answer = None

    def worker(self):
        self.answer = self.function(*self.args)

    def run(self, timeout):
        """
        Runs the function with timeout.
        :param timeout: time in seconds
        :return: test
        """
        thread = threading.Thread(target=self.worker)
        thread.start()
        thread.join(timeout)
        return self.answer


def get_from_csv(file):
    """
    Reads from the specified csv file.
    :param file: test
    :return: test
    """
    csv_reader = reader(file)
    _ = next(csv_reader)
    for feature in csv_reader:
        yield feature


def run_live_prediction(file, model):
    with open(file, 'r') as f:
        previous_prediction = None
        amplitude = []
        end_periods = []
        for feature in get_from_csv(f):
            runner = RunWithTimeout(model.predict, (feature,))
            prediction = runner.run(10)
            if previous_prediction is None:
                previous_prediction = prediction
            elif previous_prediction != prediction:
                amplitude.append(int(previous_prediction))
                end_periods.append(convert_date_to_seconds(feature[0]))
                previous_prediction = prediction
        if len(amplitude) == 0:
            amplitude.append(int(previous_prediction))
            end_periods.append(convert_date_to_seconds('2022-03-07 23:59:50'))
    return {"file_name": os.path.basename(file), "end_periods": end_periods, "leakages": amplitude}


def evaluate_json(prediction_json, true_json):
    set_one = {p['file_name'] for p in prediction_json['prediction_results']}
    set_two = {p['file_name'] for p in true_json['prediction_results']}

    if len(set_one.union(set_two)) != len(set_one):
        raise "Filenames do not match or there is a missing prediction file"

    true_data = convert_json_data_to_dataframe(true_json)
    predicted_data = convert_json_data_to_dataframe(prediction_json)
    return evaluate(true_data, predicted_data)


def generate_live_predictions(files: List, model) -> dict:
    return {'prediction_results': [run_live_prediction(file, model) for file in files]}


def evaluate_live(csv_files, true_results_json_file, model):
    prediction_json = generate_live_predictions(csv_files, model)
    true_json = read_json(true_results_json_file)
    return evaluate_json(prediction_json, true_json)


if __name__ == '__main__':
    from leak_detection import LeakDetection

    print(evaluate_live(['data.csv'], 'solution.json', LeakDetection()))
