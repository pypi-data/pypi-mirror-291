# Python-клиент для Mirapolis Virtualroom

## Клиент находится в разработке!

### Особенности

Клиент полностью асинхронный с поддержкой валидации Pydantic. Требуется Python 3.12 или выше. Основан на `aiohttp` и `pydantic`.
> Сделан на основе [официальной документации](https://support.mirapolis.ru/mira-support/#&step=1&name=%5B01004%5D%5BИнструкция%5D%5BОписание+API%5D%5BUSER%5D%5BF%5D%5B2_44%5D&doaction=Go&s=IZ8RV4AEFDzTTMKY9PgS&id=69&type=mediapreview).

### Установка

```console
$ pip install mirapolis-virtualroom
```

### Использование
```Python
from mirapolis_virtualroom.virtualroom_api import VirtualRoom
import asyncio
import logging


# Инициализация клиента
mirapolis_api = VirtualRoom(
    app_id="test",
    secret_key="secret_key",
    base_link="https://v1234.vr.mirapolis.ru/mira"
)


async def main():
    # Получение списка мероприятий
    measures = await mirapolis_api.get_measures(
        limit=10, # Количество на одной странице
        offset=40, # Сдвиг страницы
    )
    for measure in measures:
        # Полный вывод
        print(repr(measure))
        # Краткий вывод (строка)
        print(measure)
        # Получение названия
        print(measure.mename)
    # Получение общего количества мероприятий
    print(f"{measures.count=}")


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    asyncio.run(main())
```
