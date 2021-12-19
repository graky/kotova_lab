import os
import re
from itertools import zip_longest


def is_valid_menu_choice(
    menu_item, *args
):  # проверка на правильный выбор в меню, является ли выбор числом и входит ли в заданный промежуток
    if menu_item.isdigit() and int(menu_item) in args:
        return True
    return False


def add_line(path, fields_number):  # добавляем новую строку в файл

    if (
        fields_number > 1
    ):  # проверка является ли файл не пустым, если да, то строка должна содержать тоже количество полей что и другие строки
        new_line = input(
            f"Введите строку для добавления, содержащую {fields_number} полей, разделенных символом '|'"
            f"\nДля возврата на предыдущий уровень меню введите /back\n"
        )
    else:  # если нет, количество полей произвольное
        new_line = input(
            "Введите строку для добавления, содержащую произвольное количество полей, разделенных символом '|'"
            "\nДля возврата на предыдущий уровень меню введите /back\n"
        )

    if new_line == "/back":  # возвращаемся назад по команде /back
        file_processing(path)
    if (
        len(new_line.split("|")) == fields_number or fields_number < 2
    ):  # добавляем строку, если введеная строка содержит тоже количество полей, что и до этого в файле или файл новый
        with open(path, "a", encoding="utf-8") as file:
            file.write(new_line + "\n")
            file.close()
            file_processing(path)
    else:
        print("Строка содержит неверное количество полей")
        add_line(
            path, fields_number
        )  # вводим строку ещё раз, в случае несоблюдения условий


def print_line(line):  # печать одной строки из бд
    line_list = line.split("|")
    line_list = list(
        map(
            lambda x: x.split(
                "\n"
            ),  # делаем из поля список, разбивая по переносам на новую строку
            map(
                lambda line_: re.sub(
                    "(.{15})", "\\1\n", line_.strip(), 0, re.DOTALL
                ),  # оквадрачиваем строчку, делаем перенос на новую строку через каждые 15 символов
                line_list,
            ),
        )
    )
    for el in line_list:
        if (
            15 - len(el[-1]) > 0
        ):  # если последняя строчка в поле короче 15 символов, докидываем пробелов до 15
            diff = 15 - len(el[-1])
            el[-1] = el[-1] + " " * diff
    line_zip = zip_longest(
        *line_list, fillvalue=" " * 15
    )  # разбиваем поля построчно (трудно объяснить словами, если шаришь как зип работает, то поймёшь)
    for merged_line in line_zip:
        print(*merged_line, sep="|")  # печатаем каждую строку полей
        print("_" * 20)


def one_field_search(path, field_number):  # поиск по одному полю
    if field_number == "/back":  # возвращаемся назад по команде /back
        file_processing(path)
    with open(path, "r+", encoding="utf-8") as file:  # смотрим сколько полей в таблице
        line = file.readline()
        fields_number = len(line.split("|"))
        file.close()
    if field_number.isdigit() and int(field_number) in range(
        1, fields_number + 1
    ):  # проверяем входит ли номер поля по которому ищем в промежуток и является ли номер числом
        search_phrase = input(
            "Введите фразу для поиска\n"
        )  # спрашиваем фразу для поиска
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                if line.split("|")[int(field_number) - 1].__contains__(
                    search_phrase
                ):  # если искомая фраза входит, печатаем строку
                    print_line(line)
        file_processing(path)  # возвращаемся назад в предыдущее меню
    else:  # просим ввести номер поля ещё раз, в случае неправильно введенного
        one_field_search(
            path,
            input(
                "Неправильно введенное значение номера поля. "
                "Введите числовое значение в промежутке"
                f"{list(range(1, fields_number+1))}\n"
            ),
        )


def two_fields_search(path, field_number):  # поиск по двум полям
    if field_number == ["/back"]:  # возвращаемся назад по команде /back
        file_processing(path)
    with open(path, "r+", encoding="utf-8") as file:  # смотрим сколько полей в таблице
        line = file.readline()
        fields_number = len(line.split("|"))
        file.close()
    if (
        len(field_number) > 1
    ):  # проверяем, правильно ли были введены номера полей для поиска, 2 числа через пробел
        (
            first_field_number,
            second_field_number,
        ) = field_number  # переменные номеров искомых полей
        fields_range = range(
            1, fields_number + 1
        )  # промежуток, в который должны входить номера искомых полей
        if (  # проверяем, правильно ли были введены номера полей для поиска, 2 числа через пробел, являются ли они числами, входят ли в промежуток
            first_field_number.isdigit()
            and first_field_number.isdigit()
            and fields_range.__contains__(int(first_field_number))
            and fields_range.__contains__(int(second_field_number))
        ):
            search_phrase = input(
                "Введите фразу для поиска\n"
            )  # спрашиваем фразу для поиска
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    if line.split("|")[
                        int(first_field_number) - 1
                    ].__contains__(  # если искомая фраза входит в одно из двух полей, печатаем строку
                        search_phrase
                    ) or line.split(
                        "|"
                    )[
                        int(second_field_number) - 1
                    ].__contains__(
                        search_phrase
                    ):
                        print_line(line)
            file_processing(path)
        else:
            two_fields_search(  # просим ввести номера полей ещё раз, в случае неправильно введенных
                path,
                input(
                    "Неправильно введенное значение номера поля. "
                    "Введите 2 числа через пробел в промежутке"
                    f"{list(range(1, fields_number+1))}\n"
                ).split(),
            )
    else:
        two_fields_search(  # просим ввести номера полей ещё раз, в случае неправильно введенных
            path,
            input(
                "Неправильно введенное значение номера поля. "
                "Введите 2 числа через пробел в промежутке"
                f"{list(range(1, fields_number + 1))}\n"
            ).split(),
        )


def file_processing(path):  # меню работы с файлом
    file_menu_item = input(
        "Выберите действие с файлом:\n1. Показать содержимое\n2. Добавить запись"
        "\n3. Поиск по одному полю"
        "\n4. Поиск по двум полям"
        "\n5. Выход в главное меню\nДля ответа введите цифру пункта\n"
    )
    if is_valid_menu_choice(
        file_menu_item, 1, 2, 3, 4, 5
    ):  # проверка на правильный выбор в меню, является ли выбор числом и входит ли в заданный промежуток
        file_menu_item = int(file_menu_item)
        if file_menu_item == 1:  # печатаем всю таблицу
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    print_line(line)
            file_processing(path)
        if file_menu_item == 2:  # добавляем строку в файл
            with open(
                path, "r+", encoding="utf-8"
            ) as file:  # смотрим сколько полей в таблице
                line = file.readline()
                fields_number = len(line.split("|"))
                file.close()
            add_line(path, fields_number)  # добавляем новую строку
        if file_menu_item == 3:  # поиск по одному полю
            one_field_search(
                path,
                input(
                    "Введите номер поля, по которому осуществляется поиск"
                    "\nДля возврата на предыдущий уровень меню введите /back\n"
                ),
            )
        if file_menu_item == 4:
            two_fields_search(  # поиск по двум полям
                path,
                input(
                    "Введите номера поля, по которому осуществляется поиск числами через пробел"
                    "\nДля возврата на предыдущий уровень меню введите /back\n"
                ).split(),
            )
        if file_menu_item == 5:  # в главное меню
            start_menu()


def open_existing_file(path):  # открыть существующий файл
    if path == "/back":  # возвращаемся назад по команде /back
        start_menu()
    if os.path.isfile(path):  # проверяем есть ли файл по введенному пути
        name, extension = os.path.splitext(
            path
        )  # проверяем расширение файла, должно быть .txt
        if extension == ".txt":
            file_processing(path)  # запускаем меню работы с файлом
        else:
            open_existing_file(
                input(
                    "Укажите путь до существующего файла с расширением .txt\n"
                )  # просим ввести путь до файла ещё раз, в случае неправильно введенного
            )
    else:
        open_existing_file(
            input(
                "Укажите путь до существующего файла с расширением .txt\n"
            )  # просим ввести путь до файла ещё раз, в случае неправильно введенного
        )


def create_new_file(path):  # создаем/перезаписываем новый файл
    if path == "/back":  # возвращаемся назад по команде /back
        start_menu()
    if os.path.exists(path) and os.path.isdir(
        path
    ):  # проверяем, существует ли такая папка
        file_name = input(
            "Введите имя нового файла БЕЗ расширения\n"
        )  # вводим имя создаваемого файла
        path_to_new_file = f"{path}/{file_name}.txt"  # путь до нового файла
        open(path_to_new_file, "w+").close()  # создаем новый файл
        open_existing_file(path_to_new_file)  # запускаем меню обработки файла
    else:
        create_new_file(
            input("Укажите путь до существующей директории\n")
        )  # просим ввести путь ещё раз, если до этого был указан неправильно


def start(menu_item):
    if is_valid_menu_choice(
        menu_item, 1, 2, 3
    ):  # проверка на правильный выбор в меню, является ли выбор числом и входит ли в заданный промежуток
        menu_item = int(menu_item)
        if menu_item == 1:  # открываем существующий файл
            existing_db_path = input(
                "Укажите путь для открытия файла\n"
                "Для возврата на предыдущий уровень меню введите /back\n"
            )
            open_existing_file(existing_db_path)  # запускаем меню работы с файлом
        elif menu_item == 2:  # создаем новый файл
            new_db_path = input(  # спрашиваем директорию, в которой создать файл
                "Укажите директорию инициализации нового файла\n"
                "Для возврата на предыдущий уровень меню введите /back\n"
            )
            create_new_file(new_db_path)  # запускаем создание нового файла
        elif menu_item == 3:  # закрыть программу
            exit()  # закрываем программу
    else:
        start(  # просим выбрать в меню ещё раз, в случае неправильного выбора
            input(
                "Укажите валидный пункт меню. Пункт меню выбирается вводом цифры пункта\n"
            )
        )


def start_menu():
    start_menu_input = input(  # главное меню
        "Выберите действие:\n1. Открыть существующий файл базы данных"
        "\n2. Создать новый файл базы данных"
        "\n3. Закрыть программу\n"
        "Для ответа введите цифру пункта\n"
    )
    start(start_menu_input)  # запускаем обработку выбора в главном меню


start_menu()  # запускаем главное меню при запуске скрипта
