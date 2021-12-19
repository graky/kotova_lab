import os
import re
from itertools import zip_longest


def is_valid_menu_choice(menu_item, *args):
    if menu_item.isdigit() and int(menu_item) in args:
        return True
    return False


def add_line(path, fields_number):

    if fields_number > 1:
        new_line = input(
            f"Введите строку для добавления, содержащую {fields_number} полей, разделенных символом '|'"
            f"\nДля возврата на предыдущий уровень меню введите /back\n"
        )
    else:
        new_line = input(
            "Введите строку для добавления, содержащую произвольное количество полей, разделенных символом '|'"
            "\nДля возврата на предыдущий уровень меню введите /back\n"
        )

    if new_line == "/back":
        file_processing(path)
    if len(new_line.split("|")) == fields_number or fields_number < 2:
        with open(path, "a", encoding="utf-8") as file:
            file.write(new_line + "\n")
            file.close()
            file_processing(path)
    else:
        print("Строка содержит неверное количество полей")
        add_line(path, fields_number)


def print_line(line):
    line_list = line.split("|")
    line_list = list(
        map(
            lambda x: x.split("\n"),
            map(
                lambda line_: re.sub("(.{15})", "\\1\n", line_.strip(), 0, re.DOTALL),
                line_list,
            ),
        )
    )
    for el in line_list:
        if 15 - len(el[-1]) > 0:
            diff = 15 - len(el[-1])
            el[-1] = el[-1] + " " * diff
    line_zip = zip_longest(*line_list, fillvalue=" " * 15)
    for merged_line in line_zip:
        print(*merged_line, sep="|")
        print("_" * 20)


def one_field_search(path, field_number):
    if field_number == "/back":
        file_processing(path)
    with open(path, "r+", encoding="utf-8") as file:
        line = file.readline()
        fields_number = len(line.split("|"))
        file.close()
    if field_number.isdigit() and int(field_number) in range(1, fields_number + 1):
        search_phrase = input("Введите фразу для поиска\n")
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                if line.split("|")[int(field_number) - 1].__contains__(search_phrase):
                    print_line(line)
        file_processing(path)
    else:
        one_field_search(
            path,
            input(
                "Неправильно введенное значение номера поля. "
                "Введите числовое значение в промежутке"
                f"{list(range(1, fields_number+1))}\n"
            ),
        )


def two_fields_search(path, field_number):
    if field_number == ["/back"]:
        file_processing(path)
    with open(path, "r+", encoding="utf-8") as file:
        line = file.readline()
        fields_number = len(line.split("|"))
        file.close()
    if len(field_number) > 1:
        first_field_number, second_field_number = field_number
        fields_range = range(1, fields_number + 1)
        if (
            first_field_number.isdigit()
            and first_field_number.isdigit()
            and fields_range.__contains__(int(first_field_number))
            and fields_range.__contains__(int(second_field_number))
        ):
            search_phrase = input("Введите фразу для поиска\n")
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    if line.split("|")[int(first_field_number) - 1].__contains__(
                        search_phrase
                    ) or line.split("|")[int(second_field_number) - 1].__contains__(
                        search_phrase
                    ):
                        print_line(line)
            file_processing(path)
        else:
            two_fields_search(
                path,
                input(
                    "Неправильно введенное значение номера поля. "
                    "Введите 2 числа через пробел в промежутке"
                    f"{list(range(1, fields_number+1))}\n"
                ).split(),
            )
    else:
        two_fields_search(
            path,
            input(
                "Неправильно введенное значение номера поля. "
                "Введите 2 числа через пробел в промежутке"
                f"{list(range(1, fields_number + 1))}\n"
            ).split(),
        )


def file_processing(path):
    file_menu_item = input(
        "Выберите действие с файлом:\n1. Показать содержимое\n2. Добавить запись"
        "\n3. Поиск по одному полю"
        "\n4. Поиск по двум полям"
        "\n5. Выход в главное меню\nДля ответа введите цифру пункта\n"
    )
    if is_valid_menu_choice(file_menu_item, 1, 2, 3, 4, 5):
        file_menu_item = int(file_menu_item)
        if file_menu_item == 1:
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    print_line(line)
            file_processing(path)
        if file_menu_item == 2:
            with open(path, "r+", encoding="utf-8") as file:
                line = file.readline()
                fields_number = len(line.split("|"))
                file.close()
            add_line(path, fields_number)
        if file_menu_item == 3:
            one_field_search(
                path,
                input(
                    "Введите номер поля, по которому осуществляется поиск"
                    "\nДля возврата на предыдущий уровень меню введите /back\n"
                ),
            )
        if file_menu_item == 4:
            two_fields_search(
                path,
                input(
                    "Введите номера поля, по которому осуществляется поиск числами через пробел"
                    "\nДля возврата на предыдущий уровень меню введите /back\n"
                ).split(),
            )
        if file_menu_item == 5:
            start_menu()


def open_existing_file(path):
    if path == "/back":
        start_menu()
    if os.path.isfile(path):
        name, extension = os.path.splitext(path)
        if extension == ".txt":
            file_processing(path)
        else:
            open_existing_file(
                input("Укажите путь до существующего файла с расширением .txt\n")
            )
    else:
        open_existing_file(
            input("Укажите путь до существующего файла с расширением .txt\n")
        )


def create_new_file(path):
    if path == "/back":
        start_menu()
    if os.path.exists(path) and os.path.isdir(path):
        file_name = input("Введите имя нового файла БЕЗ расширения\n")
        path_to_new_file = f"{path}/{file_name}.txt"
        open(path_to_new_file, "w+").close()
        open_existing_file(path_to_new_file)
    else:
        create_new_file(input("Укажите путь до существующей директории\n"))


def start(menu_item):
    if is_valid_menu_choice(menu_item, 1, 2, 3):
        menu_item = int(menu_item)
        if menu_item == 1:
            existing_db_path = input(
                "Укажите путь для открытия файла\n"
                "Для возврата на предыдущий уровень меню введите /back\n"
            )
            open_existing_file(existing_db_path)
        elif menu_item == 2:
            new_db_path = input(
                "Укажите директорию инициализации нового файла\n"
                "Для возврата на предыдущий уровень меню введите /back\n"
            )
            create_new_file(new_db_path)
        elif menu_item == 3:
            exit()
    else:
        start(
            input(
                "Укажите валидный пункт меню. Пункт меню выбирается вводом цифры пункта\n"
            )
        )


def start_menu():
    start_menu_input = input(
        "Выберите действие:\n1. Открыть существующий файл базы данных"
        "\n2. Создать новый файл базы данных"
        "\n3. Закрыть программу\n"
        "Для ответа введите цифру пункта\n"
    )
    start(start_menu_input)


start_menu()
