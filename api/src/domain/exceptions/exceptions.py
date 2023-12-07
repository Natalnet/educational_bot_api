from datetime import date


class UserNotFoundException(Exception):
    def __init__(self):
        super().__init__('Usuario nao encontrado')


class InvalidDateRegistrarPresencaException(Exception):
    def __init__(self, today: date):
        self.today = today
        super().__init__(f'Presença ja cadastrada na data {self.today}')


class TurmaNotFoundException(Exception):
    def __init__(self):
        super().__init__('Turma nao encontrada')


class MinitesteNotFoundException(Exception):
    def __init__(self):
        super().__init__('Miniteste nao encontrado')

