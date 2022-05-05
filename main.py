# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os.path


class Test_generator:

    plate_data = None
    zhgut_data = None
    folder_flag = False
    error_code = 0

    # TODO: Сделать error коды
    def __init__(self, plate, zhgut):
        # plate init
        self.plate_init(plate)
        self.zhgut_init(zhgut)

    def plate_init(self, plate):
        # TODO: Сделать проверку входных данных
        if type(plate) == dict:
            self.plate_data = plate
        elif type(plate) == str:
            # string is directory
            if os.path.isdir(plate):
                self.folder_flag = True
            # string is file (path)
            # TODO: Проверка на расширение JSON
            elif os.path.isfile(plate):
                with open(plate) as json_file:
                    self.plate_data = json.load(json_file)

    def zhgut_init(self,zhgut):
        # TODO: Сделать проверку входных данных
        if type(zhgut) == dict:
            self.zhgut_data = zhgut
        elif type(zhgut) == str:
            if os.path.isfile(zhgut):
                with open(zhgut) as zhgut_file:
                    self.zhgut_data = json.load(zhgut_file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test = Test_generator("F:\\Python projects\\Иванычев_sdfЛ1.json", "F:\\Python projects\\Иванычев_ИВТ-32_Л1.json")
    print()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
