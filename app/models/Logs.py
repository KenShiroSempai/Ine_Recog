import csv


class Logs:
    def __init__(self, file_path):
        self.file_path = file_path

    def visit(self, log):
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(log)

    def save_logs(self, logs):
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(logs)

    def Bitacora(self):
        pass
