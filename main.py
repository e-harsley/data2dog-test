import json

open_symbols = ['[', '{', '{', '(']
close_symbols = [']', '}', '}', ')']


class BaseGenerator:

    def __init__(self):
        self.data = {}
        self.spacing = " "
        self.data_types = [list, set, dict, tuple]
        self.open_symbol = ""
        self.indent = 0
        self.close_symbol = ""
        self.schema_res = " "

    def init_data(self, data):
        self.data = data
        return self.data

    def get_type(self, data) -> str:
        data = data
        return type(data)

    def get_close_open_symbols(self, type: str) -> (str, str):
        zip_symbol = zip(open_symbols, close_symbols)
        symbols = list(zip_symbol)
        type_index = self.data_types.index(type) if type in self.data_types else 2

        self.open_symbol, self.close_symbol = symbols[type_index]
        return self.open_symbol, self.close_symbol

    def open_symbol_(self, indent: int) -> str:
        return f'{self.spacing * indent}{self.open_symbol}'

    def close_symbol_(self, indent: int) -> str:
        return f'{self.spacing * indent}{self.close_symbol}'

    def add_key(self, key: str, indent: int) -> str:
        return f'!{key}!:'

    def add_value(self, value: str, indent: int) -> str:
        return f'!{value}!,'

    def generate_data(self, key: str, type: str):
        self.schema_res += self.add_key(key=key, indent=0)
        self.schema_res += self.add_value(value=type, indent=1)
        self.schema_res += self.add_key(key="tag", indent=0)
        self.schema_res += self.add_value(value=key, indent=1)
        self.schema_res += self.add_key(key="description", indent=0)
        self.schema_res += self.add_value(value=f"Please input {key}", indent=1)
        self.schema_res += self.add_key(key="required", indent=0)
        self.schema_res += self.add_value(value="false", indent=1)



class SchemaGen(BaseGenerator):

    def get_non_data_type(self, data):

        self.schema_res = f"{self.open_symbol_(0)}"
        self.schema_res += self.add_key(key="type", indent=self.indent)
        self.schema_res += self.add_value(value=data.__class__.__name__, indent=0)
        self.schema_res += self.add_key(key="tag", indent=self.indent)
        self.schema_res += self.add_value(value=data.__class__.__name__, indent=0)
        self.schema_res += self.add_key(key="description", indent=self.indent)
        self.schema_res += self.add_value(value=data.__class__.__name__ + " is not required", indent=0)
        self.schema_res += self.add_key(key="required", indent=self.indent)
        self.schema_res += self.add_value(value="false", indent=0)
        self.schema_res += f"{self.close_symbol_(0)}"

    def read_json_file(self, filename):
        with open(filename, mode='rt') as file:
            # data = json.load(file)
            return file.read()

    def write_json_file(self, data, filename):
        with open(filename, mode="w") as write_file:
            write_file.write(data)


    def make_schema(self, file_to_read_from):
        file = self.read_json_file(file_to_read_from)
        data = json.loads(file)
        message = data.get("message")
        response = self.generate_schema(message)
        data = response.replace("!:", '":')
        data = data.replace("!", '"')
        data = data.replace(",}", '},')
        data = data.replace(',}}', '}},')
        data = data.replace(',}', '},')
        data = data.replace(':{{', ':{')
        data = json.dumps(data)
        data_1 = json.loads(data)
        self.write_json_file(data_1, "example.json")


    def generate_schema(self, data):
        data_type = self.get_type(data)
        self.get_close_open_symbols(data.__class__.__name__)
        if data_type in self.data_types:
            self.schema_res = f'{self.open_symbol_(0)}'

            if isinstance(data, dict):
                for key, value in data.items():
                    self.schema_res += f'{self.add_key(key=key, indent=2)}'
                    self.schema_res += f'{self.generate_schema(value)}'
            else:
                if type is set:
                    return self.schema_res[:1] + (data.pop().__class__.__name__ if len(data) else None) +self.close_symbol

                else:
                    if len(data) > 0:
                        if all(isinstance(d, type(data[0])) for d in data[1:]) and type(data[0]) not in self.data_types:
                            print(">>>>>>>>>>>.....",type(data[0]),data[0].__class__.__name__)
                            # return self.get_non_data_type(data[0].__class__.__name__)
                            return self.schema_res[:-1]  +  self.add_key(key="tag", indent=self.indent) +\
                                             self.add_value(value=data.__class__.__name__, indent=0)  + \
                                             self.add_key(key="description", indent=self.indent) +  \
                                            self.add_value(value=data.__class__.__name__  + " of " +  data[0].__class__.__name__, indent=0) + \
                                             self.add_key(key="required", indent=self.indent) + \
                                   self.add_value("false",
                                                  indent=0) +  self.close_symbol
                        else:
                            for value in data:
                                self.schema_res  += f'{self.generate_schema(value)}'
                    else:
                        return self.schema_res[:-1]  + self.add_key(key="tag", indent=self.indent) + \
                               self.add_value(value=data.__class__.__name__, indent=0) + \
                               self.add_key(key="description", indent=self.indent) + \
                               self.add_value(value=data.__class__.__name__,
                                              indent=0) + \
                               self.add_key(key="required", indent=self.indent) + \
                               self.add_value("false",
                                              indent=0) + self.close_symbol

            self.schema_res += f'{self.close_symbol_(0)}'

        else:
            self.get_non_data_type(data)

        return self.schema_res


d = SchemaGen()

s = d.make_schema("data/data_1.json")

print(s)







