from enum import Enum


class ValidationError(str, Enum):
    """Перечисляет общие сообщения об ошибках при валидации с проектами."""

    project_name_already_exist = 'Проект с таким именем уже существует!'
    project_not_found = 'Проект не найден!'
    project_full_amout_not_valid = (
        'Нельзя установить значение full_amount '
        'меньше уже вложенной суммы.'
    )
    project_already_invested = (
        'В проект внесены средства, невозможно {}.'
    )
    project_closed_or_fully_invested = (
        'Проект собрал средства или был закрыт, '
        'нельзя удалять.'
    )
