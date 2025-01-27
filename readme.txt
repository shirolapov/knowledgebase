Для тестового задания я использовал ЯП Python 3.6 и вэб фреймворк
Django 1.11. Данный фреймворк я выбрал потомучто почти весь функционал для выполнения
этого тестового задания есть в нём "из коробки".

Самое крупное дополнение для Django которое здесь используется это
"django-wysiwyg-redactor" для удобства форматирования статей.

В качестве БД здесь использован Postgresql. Я выбрал именно эту СУБД так как
это одна из самых распространённых Open Source субд. У неё очень
большое сообшество разработчиков. Хорошо сделанная документация. Одно из главных
отличий этой СУБД от MySQL это полнотекстовый поиск который скорее всего
понадобиться при наполнение базы знаний статьями.

Для разработки и развёртывания я использовал Docker. Так как он позволяет
разрабатывать, тестировать и развёртывать приложения не зависимо от
окружения. Что очень удобно для распределённых груп разработчиков.

Фронтенда в этом приложении по минимуму. В качетве CSS фреймворка я использовал
Bootstrap из-за его распространнённости и хорошей документации. Его главный
недостаток это его большой размер. Но это можно компенсировать при помощи
минификации и разбиения фронтенда на "бандлы" при помощи инструментов WebPack и
uglifyjs. В данном приложении для простоты эти инструменты не используються.

Логика приложения: В первую очередь, с помошью CLI создаёться суперпользователь.
Суперпользователь может создавать, увольнять и редактировать
операторов. Операторы не могут увольнять, создавать или редактировать себя или
другого оператора.

Операторы могут создавать статьи и редактировать свои статьи. Чужие статьи
редактировать нельзя. Суперпользователь может редактировать любые статьи через
админпанель.

Операторы могут видеть любые статьи. Неавторизованный пользователь может видеть
только статьи без метки "внутренний".

Структура БД. Я не стал менять уже встроенную в фреймворк структуру данных
пользователей, сессий так как она полностью подходила под поставленные
задачи. Все модели данных используют только встроенную в фреймворк ORM. Мной
написана одна модель - articles. Articles состоит из полей:
    id: первичный ключь по умолчанию,
    author: внешний ключь к модели данных пользователей, содержит ссылку на
объект пользователя.
    title: Заголовок статьи. Обязательное поле.
    short_text: Короткий текст. Необязательный атрибут.
    text: Главный текст статьи. В представлении выводиться как
HTML. Обязательное поле.
    internal: Обозначение внутренней статьи. По умолчанию TRUE.
    datetime_created: Время создания, после изменения данных не изменяется.
    datetime_modified: Время последней модификации статьи.

Все данные храняться в одной базе данных. Кэш данных не используется.

Требования:
    CentOS-7 или Debian-9 или Ubuntu14.10+
    Docker
    Docker-compose(для удобства развёртывания)

Для того чтобы развернуть приложение необходимо:
    Находясь в директории с приложением ввести следующие команды:

    docker-compose build
    docker-compose up -d
    docker exec -ti knowledgebase_web_1 python manage.py migrate
    docker exec -ti knowledgebase_web_1 python manage.py collectstatic --noinput
    docker exec -ti knowledgebase_web_1 python manage.py createsuperuser

    Название контейнера knowledgebase_web_1 может меняться в зависимости от
    названия директории в которой расположено данное приложение. Чтобы изнать
    точное название контйнера введите docker ps. По умолчанию докер называет
    контейнеры "имя директори + web_1"

    И последовательно ответить на вопросы мастера создания
    суперпользователя. После чего можно переходить в браузере на
    http://localhost:8080 и пользоваться приложением.

    Для работы на продакшн сервере необходимо внести изменения в файл
    "knowledgebase\knowledgebase\settings.py"

    В ALLOWED_HOSTS добавить доменное имя сервера.
    Изменить DEBUG на False
    В DATABASES ввести данные для доступа к базе данных (если используется
    стороння база данных)

В папке examplesconfs есть примеры конфигурационных файлов для разных окружений:

    docker-compose-without-bd-and-nginx: Внешняя база данных, на сервере уже
    есть вэб сервер (например вэб сервер обслуживает несколько приложений на
    хосте).

    docker-compose-without-bd:Внешняя база данных. Например если хост
    обслуживает только один сайт, но БД на другом хосте.

    В данных примерах uwsgi настроен на http порт. Порт используеться
    8000. Чтобы изменить порт измените в файле конфигурации docker-compose
    директиву "ports:- "8000:8000"" на "ports: - "yourport:8000""
