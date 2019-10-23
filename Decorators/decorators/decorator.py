from datetime import datetime


def log_decorator(log_path):
    def log_decor(function):
        def logger(*args, **kwargs):
            arg_string = str()
            data = datetime.today()
            ret = function(*args, **kwargs)
            function_name = function.__name__
            for arg in args:
                arg_string += f'{arg} '
            for name, value in kwargs.items():
                arg_string += f'{name}: {value}; '
            if not arg_string:
                func_string = f'Функция "{function_name}" исполнялась {data} без аргументов и вернула "{ret}"\n'
            else:
                func_string = f'Функция "{function_name}" исполнялась {data} с аргументами {arg_string.rstrip()} и вернула "{ret}"\n'

            with open(log_path, mode='a', encoding='utf-8') as file:
                file.write(func_string)

        return logger

    return log_decor
