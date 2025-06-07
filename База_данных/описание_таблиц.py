# Описание структуры таблиц базы данных
# TABLES — словарь с SQL-запросами для создания таблиц

TABLES = {
    'офицеры': '''
        CREATE TABLE IF NOT EXISTS офицеры (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            имя TEXT NOT NULL,
            фамилия TEXT NOT NULL,
            отчество TEXT,
            звание_id INTEGER,
            должность_id INTEGER,
            подразделение_id INTEGER,
            состояние_сод INTEGER DEFAULT 0,
            состояние_псод INTEGER DEFAULT 0,
            FOREIGN KEY (звание_id) REFERENCES звания (id),
            FOREIGN KEY (должность_id) REFERENCES должности (id),
            FOREIGN KEY (подразделение_id) REFERENCES подразделения (id)
        )
    ''',
    'курсанты': '''
        CREATE TABLE IF NOT EXISTS курсанты (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            имя TEXT NOT NULL,
            фамилия TEXT NOT NULL,
            отчество TEXT,
            звание_id INTEGER,
            должность_id INTEGER,
            подразделение_id INTEGER,
            год_набора INTEGER NOT NULL,
            состояние_сод INTEGER DEFAULT 0,
            состояние_псод INTEGER DEFAULT 0,
            FOREIGN KEY (звание_id) REFERENCES звания (id),
            FOREIGN KEY (должность_id) REFERENCES должности (id),
            FOREIGN KEY (подразделение_id) REFERENCES подразделения (id)
        )
    ''',
    'звания': '''
        CREATE TABLE IF NOT EXISTS звания (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            наименование TEXT NOT NULL,
            категория TEXT NOT NULL,
            сокращение TEXT,
            CONSTRAINT check_категория CHECK (категория IN ('курсант', 'офицер', 'общее'))
        )
    ''',
    'должности': '''
        CREATE TABLE IF NOT EXISTS должности (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            наименование TEXT NOT NULL UNIQUE,
            категории TEXT NOT NULL CHECK (
                json_valid(категории) AND 
                json_array_length(категории) > 0
            )
        )
    ''',
    'подразделения': '''
        CREATE TABLE IF NOT EXISTS подразделения (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            наименование TEXT NOT NULL,
            абривиатура TEXT,
            тип_подразделения_id INTEGER,
            FOREIGN KEY (тип_подразделения_id) REFERENCES типы_подразделений (id)
        )
    ''',
    'типы_подразделений': '''
        CREATE TABLE IF NOT EXISTS типы_подразделений (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            наименование TEXT NOT NULL UNIQUE
        )
    ''',
    'иерархия_подразделений': '''
        CREATE TABLE IF NOT EXISTS иерархия_подразделений (
            родительское_подразделение_id INTEGER,
            дочернее_подразделение_id INTEGER,
            FOREIGN KEY (родительское_подразделение_id) REFERENCES подразделения (id),
            FOREIGN KEY (дочернее_подразделение_id) REFERENCES подразделения (id),
            PRIMARY KEY (родительское_подразделение_id, дочернее_подразделение_id)
        )
    ''',
    'история_перемещения_сотрудников': '''
        CREATE TABLE IF NOT EXISTS история_перемещения_сотрудников (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            сотрудник_id INTEGER NOT NULL,
            сотрудник_type TEXT NOT NULL,
            change_type TEXT NOT NULL,
            звание_id INTEGER,
            должность_id INTEGER,
            подразделение_id INTEGER,
            дата_начала DATE NOT NULL,
            дата_окончание DATE,
            FOREIGN KEY (звание_id) REFERENCES звания (id),
            FOREIGN KEY (должность_id) REFERENCES должности (id),
            FOREIGN KEY (подразделение_id) REFERENCES подразделения (id)
        )
    ''',
    'приказы': '''
        CREATE TABLE IF NOT EXISTS приказы (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            дата_создания DATE NOT NULL,
            дата_регистрации DATE,
            номер_регистрации TEXT,
            исполнитель_id INTEGER NOT NULL,
            руководитель_id INTEGER NOT NULL,
            название TEXT NOT NULL,
            основание TEXT NOT NULL,
            тип_приказа TEXT NOT NULL,
            список_лиц_согласования TEXT,
            FOREIGN KEY (исполнитель_id) REFERENCES офицеры (id),
            FOREIGN KEY (руководитель_id) REFERENCES офицеры (id)
        )
    ''',
    'список_нарядов_в_приказе': '''
        CREATE TABLE IF NOT EXISTS список_нарядов_в_приказе (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            начало_дата_время DATETIME NOT NULL,
            конец_дата_время DATETIME NOT NULL,
            приказ_id INTEGER NOT NULL,
            FOREIGN KEY (приказ_id) REFERENCES приказы (id)
        )
    ''',
    'назначения_в_наряд': '''
        CREATE TABLE IF NOT EXISTS назначения_в_наряд (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            список_нарядов_в_приказе_id INTEGER NOT NULL,
            офицер_id INTEGER,
            курсант_id INTEGER,
            тип_наряда_id INTEGER NOT NULL,
            пост_id INTEGER NOT NULL,
            начало_дата_время DATETIME NOT NULL,
            конец_дата_время DATETIME NOT NULL,
            FOREIGN KEY (список_нарядов_в_приказе_id) REFERENCES список_нарядов_в_приказе (id),
            FOREIGN KEY (офицер_id) REFERENCES офицеры (id),
            FOREIGN KEY (курсант_id) REFERENCES курсанты (id),
            FOREIGN KEY (тип_наряда_id) REFERENCES типы_нарядов (id),
            FOREIGN KEY (пост_id) REFERENCES посты (id),
            CHECK ((офицер_id IS NULL AND курсант_id IS NOT NULL) OR (офицер_id IS NOT NULL AND курсант_id IS NULL))
        )
    ''',
    'посты': '''
        CREATE TABLE IF NOT EXISTS посты (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            наименование TEXT NOT NULL,
            дежурный BOOLEAN NOT NULL DEFAULT 0,
            дежурный_кол INTEGER NOT NULL DEFAULT 0,
            дежурный_офицер BOOLEAN NOT NULL DEFAULT 0,
            дежурный_курсант BOOLEAN NOT NULL DEFAULT 0,
            дневальный BOOLEAN NOT NULL DEFAULT 0,
            дневальный_кол INTEGER NOT NULL DEFAULT 0
        )
    ''',
    'типы_нарядов': '''
        CREATE TABLE IF NOT EXISTS типы_нарядов (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            наименование TEXT NOT NULL
        )
    ''',
}
