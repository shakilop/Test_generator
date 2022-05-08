# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os.path


class Test_generator:

    class JSONFormatException(Exception):
        pass

    class FileTypeException(Exception):
        pass

    class Data_checker:
        TYPE_WORD = "type"
        CONNECTION_WORD = "connection"
        VERSION_WORD = "version"
        CONTENT_WORD = "contents"
        NET_WORD = "net"
        COMPONENT_WORD = "component"
        PIN_WORD = "pin"

        def __init__(self, data=None):
            if data is None:
                data = {}
            self.data = data

        def __data_select(self, data=None):
            if data is None:
                return self.data
            elif type(data) is dict:
                return data
            else:
                self.__gen_exception("Wrong datatype (data in check_version)")

        def check_version(self, data=None):
            temp = self.__data_select(data)
            if self.VERSION_WORD in temp.keys():
                return temp[self.VERSION_WORD]
            else:
                self.__gen_exception("No \"" + self.VERSION_WORD + "\" field in json")

        def check_type(self, data=None):
            temp = self.__data_select(data)
            if self.TYPE_WORD in temp.keys():
                return temp[self.TYPE_WORD]
            else:
                self.__gen_exception("No \"" + self.TYPE_WORD + "\" field in json")

        def __gen_exception(self, string):
            raise Test_generator.JSONFormatException(string)

        def __check_word(self, word, dictionary=None):
            if dictionary is None:
                dictionary = {}
            if word not in dictionary.keys():
                self.__gen_exception("No \"" + word + "\" field in json")

        def check_content(self, data=None):
            temp = self.__data_select(data)
            if self.CONTENT_WORD in temp.keys():
                # В листе как минимум 1 соеденение
                if len(temp[self.CONTENT_WORD]) > 0 and type(temp[self.CONTENT_WORD]) is list:
                    # Проверим каждую запись на наличие необходимых полей и "висящих проводов"
                    for record in temp[self.CONTENT_WORD]:
                        # Проверка что запись в листе это словарь
                        if type(record) is dict:
                            # Проверка наличия поля net и connection
                            self.__check_word(self.NET_WORD, record)
                            self.__check_word(self.CONNECTION_WORD, record)
                            # Проверим что под connection есть лист с как-минимум 2-мя записями
                            if type(record[self.CONNECTION_WORD]) is list and len(record[self.CONNECTION_WORD]) > 1:
                                for connection in record[self.CONNECTION_WORD]:
                                    if type(connection) is not dict:
                                        self.__gen_exception("Not dict in \"" + self.CONNECTION_WORD + "\" list")
                                    # Проверка наличия поля component и pin
                                    self.__check_word(self.COMPONENT_WORD, connection)
                                    self.__check_word(self.PIN_WORD, connection)
                            else:
                                self.__gen_exception(
                                    "\"" + self.CONNECTION_WORD + "\" is empty(<2) or incorrect")
                        else:
                            self.__gen_exception("Not dict in \"" + self.CONTENT_WORD + "\" list")
                else:
                    self.__gen_exception("\"" + self.CONTENT_WORD + "\" is empty or incorrect")
            else:
                self.__gen_exception("No \"" + self.CONTENT_WORD + "\" field in json")

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
        # На вход подали данные
        if type(plate) == dict:
            self.plate_data = plate
        # На вход подали адресс
        elif type(plate) == str:
            # string is directory
            if os.path.isdir(plate):
                self.folder_flag = True
            # string is file (path)
            elif os.path.isfile(plate):
                if os.path.splitext(plate)[1] == ".json":
                    with open(plate) as json_file:
                        self.plate_data = json.load(json_file)
                else:
                    raise self.FileTypeException("Plate: Wrong filetype(" + os.path.splitext(plate)[1] +
                                                 "). Must be .json")
        else:
            raise self.FileTypeException("Garbage in plate input (not dict or str)")

    def zhgut_init(self, zhgut):
        if type(zhgut) == dict:
            self.zhgut_data = zhgut
        elif type(zhgut) == str:
            if os.path.isfile(zhgut):
                if os.path.splitext(zhgut)[1] == ".json":
                    with open(zhgut) as zhgut_file:
                        self.zhgut_data = json.load(zhgut_file)
                else:
                    raise self.FileTypeException("Zhgut: Wrong filetype(" + os.path.splitext(zhgut)[1] +
                                                 "). Must be .json")
        else:
            raise self.FileTypeException("Garbage in zhgut input (not dict or str)")

    def check_data(self):
        checker = self.Data_checker()
        if not self.folder_flag:
            try:
                checker.check_type(self.plate_data)
                checker.check_version(self.plate_data)
                checker.check_content(self.plate_data)
            except self.JSONFormatException as e:
                print(e)
                self.error_code = -1



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test = Test_generator("F:\\Python projects\\Иванычев_sdfЛ1.json", "F:\\Python projects\\Иванычев_ИВТ-32_Л1.json")
    test.check_data()
    print()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
