import base64
import urllib.parse


def user_directory_path(instance, filename):
    """Сохраняет файл по заданному пути."""
    return f"{instance.directory}/{filename}"


def about_project_path(instance, filename):
    """Сохраняет фото О Проекте по заданному пути"""
    return f"{instance.developer.latin_name}/{instance.directory}/{filename}"


def encode_decode_values(value: str):
    """Кодируем и декодируем значение."""
    try:
        return urllib.parse.quote(
            base64.b64encode(value.encode("UTF-8")).decode("UTF-8")
        )
    except AttributeError:
        return None


async def correct_phone(phone: str):
    """Возвращаем телефон в нужном формате."""
    phone_number = "".join(filter(str.isdigit, phone))
    len_phone = len(phone_number)

    if len_phone not in [10, 11]:
        return None

    if phone_number[0] == "8" or (len_phone == 10 and phone_number[0] != "7"):
        phone_number = "7" + phone_number[-10:]
    return phone_number if len(phone_number) == 11 else None

