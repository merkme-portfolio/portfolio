from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

PROJECT_NAME = 'QRKot'
SPREADSHEET_TITLE = '{}. Отчёт от {}'
SHEET_TITLE = 'Лист1'
SHEETID = 0
REPORT_ROWS = 100
REPORT_COLUMNS = 11


def now_date_time() -> str:
    format = '%Y/%m/%d %H:%M:%S'
    return datetime.now().strftime(format)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    spreadsheet_body = {
        'properties': {
            'title': SPREADSHEET_TITLE.format(PROJECT_NAME, now_date_time()),
            'locale': 'ru_RU'
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': SHEETID,
                    'title': SHEET_TITLE,
                    'gridProperties': {
                        'rowCount': REPORT_ROWS,
                        'columnCount': REPORT_COLUMNS
                    }
                }
            }
        ]
    }

    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }

    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str,
    charity_projects: list[CharityProject],
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        [SPREADSHEET_TITLE.format(PROJECT_NAME, now_date_time())],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
    ]

    for project in charity_projects:
        time_difference = project.close_date - project.create_date
        new_row = [
            project.name,
            str(time_difference),
            project.description
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


async def spreadsheets_list(wrapped_services: Aiogoogle):
    service = await wrapped_services.discover('drive', 'v3')
    response = await wrapped_services.as_service_account(
        service.files.list(
            q='mimeType="application/vnd.google-apps.spreadsheet"'
        )
    )
    return [file for file in response['files'] if PROJECT_NAME in file['name']]


async def spreadsheets_clear_disk(
    wrapped_services: Aiogoogle,
    save_last: bool = False
):
    service = await wrapped_services.discover('drive', 'v3')
    spreadsheets_qrkot = await spreadsheets_list(wrapped_services)
    extra_info = ''
    if spreadsheets_qrkot:
        if save_last:
            spreadsheets_qrkot.pop()
            extra_info = ' Последний отчёт сохранён.'
        for spreadsheet in spreadsheets_qrkot:
            await wrapped_services.as_service_account(
                service.files.delete(fileId=spreadsheet['id'])
            )
        return f'Выполнена очистка файлов проекта {PROJECT_NAME}.{extra_info}'
    return 'Диск пуст.'