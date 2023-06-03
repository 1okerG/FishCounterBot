import asyncio
import os
import datetime
import subprocess

from sqlalchemy import text

# project_root = os.getcwd()

# backup_folder = os.path.join(project_root, 'backup')
# backup_filename = f"backup_{datetime.date.today()}.sql"
# backup_path = os.path.join(backup_folder, backup_filename)

def backup_postgresql_db(database_uri):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.sql"

    project_root = os.getcwd()

    backup_folder = os.path.join(project_root, 'db', 'backup')

    backup_path = os.path.join(backup_folder, backup_file)

    # Создаем команду для создания резервной копии
    backup_command = [
        'pg_dump',
        database_uri,
        '-f',
        backup_path
    ]

    try:
        # Выполняем команду для создания резервной копии
        subprocess.run(backup_command, check=True)
        print("Резервная копия базы данных успешно создана.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании резервной копии: {str(e)}")


# print(f'2     2{backup_folder}2      2')