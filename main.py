# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os.path


class Test_generator:
    """
    ERROR CODES:
    -1 - Ошибка касаемо содержимого json файла
    -2 - Ошибка открытия файла (не то расширение, или не сущ., или на входе не строка с адр/словарь с данными)
    """
    class JSONFormatException(Exception):
        pass

    class FileTypeException(Exception):
        pass

    class Data_checker:
        TYPE_WORD = None
        CONNECTION_WORD = None
        VERSION_WORD = None
        CONTENT_WORD = None
        NET_WORD = None
        COMPONENT_WORD = None
        PIN_WORD = None
        data = None

        def __init__(self, data=None,
                     type_word="type",
                     connection_word="connection",
                     version_word="version",
                     content_word="contents",
                     net_word="net",
                     component_word="component",
                     pin_word="pin"):
            """
            JSON structure
            {
            "VERSION_WORD": 1.0,
            "TYPE_WORD": "Plate",
            "CONTENT_WORD": [
            {
                "NET_WORD": "ABC1",
                "CONNECTION_WORD": [
                    {
                        "COMPONENT_WORD": "D1",
                        "PIN_WORD": "6"
                    },...
                ]
            },
                ...
            ]
        {
            :param data: json dict
            """
            if data is None:
                data = {}
            self.data = data
            self.TYPE_WORD = type_word
            self.CONNECTION_WORD = connection_word
            self.VERSION_WORD = version_word
            self.CONTENT_WORD = content_word
            self.NET_WORD = net_word
            self.COMPONENT_WORD = component_word
            self.PIN_WORD = pin_word

        def __data_select(self, data=None):
            """
            data select (between init or method input)
            :param data: json dict
            :raise JSONFormatException (if data is not dict or None)
            :return:
            """
            if data is None:
                return self.data
            elif type(data) is dict:
                return data
            else:
                self.__gen_exception("Wrong datatype (data in check_version)")

        def check_version(self, data=None):
            """
            Check VERSION_WORD key in json dict
            :param data: json data
            :return: version value
            """
            temp = self.__data_select(data)
            if self.VERSION_WORD in temp.keys():
                return temp[self.VERSION_WORD]
            else:
                self.__gen_exception("No \"" + self.VERSION_WORD + "\" field in json")

        def check_type(self, data=None):
            """
            Check TYPE_WORD key in JSON dict
            :param data: json dict
            :return: type_value
            """
            temp = self.__data_select(data)
            if self.TYPE_WORD in temp.keys():
                return temp[self.TYPE_WORD]
            else:
                self.__gen_exception("No \"" + self.TYPE_WORD + "\" field in json")

        def __gen_exception(self, string):
            """
            raise JSONFormatException
            :param string: msg
            :raise JSONFormatException
            """
            raise Test_generator.JSONFormatException(string)

        def __check_word(self, key, dictionary=None):
            """
            check key in dictionary
            if dictionary is not specified will take json dict (from init)
            :return: dictionary[key]
            :raise:JSONFormatException
            """
            if dictionary is None:
                dictionary = self.data
            if key not in dictionary.keys():
                self.__gen_exception("No \"" + key + "\" field in json")
            else:
                return dictionary[key]

        def check_content(self, data=None):
            """
            check CONTENT_WORD key, and it's value of json dict
            :param data: json dict
            :return: no return value
            :raise JSONFormatException
            """
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

        def check(self, data=None):
            self.check_type(data)
            self.check_version(data)
            self.check_content(data)

    plate_data = None
    zhgut_data = None
    folder_flag = False
    error_code = 0

    def __init__(self, plate, zhgut):
        # plate init
        self.plate_init(plate)
        self.zhgut_init(zhgut)

    def plate_init(self, plate):
        # На вход подали данные
        if type(plate) == dict:
            self.plate_data = plate
        elif type(plate) == list:
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
                raise self.FileTypeException("Cannot find file/dir")
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
                raise self.FileTypeException("Cannot find file")
        else:
            raise self.FileTypeException("Garbage in zhgut input (not dict or str)")

    def __check_dic(self,data=dict):
        checker = self.Data_checker(data)
        try:
            checker.check()
            return True
        except self.JSONFormatException as e:
            print(e)
            self.error_code = -1
            return False

    def __check_address(self, address):
        res = []
        if type(address) == str:
            if os.path.isdir(address):
                for dr in os.listdir(address):
                    abs_path = os.path.join(address, dr)
                    if os.path.isfile(abs_path):
                        if os.path.splitext(abs_path)[1] == ".json":
                            with open(abs_path) as file:
                                if not self.__check_dic(json.load(file)):
                                    print("Error with file: " + abs_path)
                                else:
                                    res.append(json.load(file))
            elif os.path.isfile(address):
                if os.path.splitext(address)[1] == ".json":
                    with open(address) as file:
                        if not self.__check_dic(json.load(file)):
                            print("Error with file: " + address)
                        else:
                            res.append(json.load(file))

    def get_data(self, data=None):
        """
        Check input data(list, dict, str) and create list of json dict
        If data is empty it will take plata_data from init
        :return: list of json dict
        """
        res = []
        if data is None:
            data = self.plate_data
        if type(data) == list:
            for item in data:
                if type(item) == dict:
                    if self.__check_dic(item):
                        res.append(item)
                if type(item) == str:
                    self.__check_address(item)
        elif type(data) == dict:
            if self.__check_dic(data):
                res.append(data)
        elif type(data) == str:
            res.append(self.__check_address(data))
        else:
            self.error_code = -2
            print("False type of input")

        # if not self.folder_flag:
        #     try:
        #         checker.check_type(self.plate_data)
        #         checker.check_version(self.plate_data)
        #         checker.check_content(self.plate_data)
        #     except self.JSONFormatException as e:
        #         print(e)
        #         self.error_code = -1

    def find_plate(self):



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test = Test_generator("F:\\Python projects\\Иванычев_sdfЛ1.json", "F:\\Python projects\\Иванычев_ИВТ-32_Л1.json")
    test.check_data()
    print()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
