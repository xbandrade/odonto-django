from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def calculate_val_cpf(val):
    result = 0
    mult = 2
    while val > 0:
        remainder = val % 10
        result += remainder * mult
        mult += 1
        val //= 10
    digit = 11 - result % 11
    return digit if digit < 10 else 0


def calculate_val_cnpj(val):
    result = 0
    mult = 2
    while val > 0:
        remainder = val % 10
        result += remainder * mult
        mult += 1
        if mult == 9:
            mult = 2
        val //= 10
    digit = 11 - result % 11
    return digit if digit < 10 else 0


def valid_cpf(cpf):
    val = cpf // 100
    result = calculate_val_cpf(val)
    if result == (cpf // 10) % 10:
        val = cpf // 10
        result = calculate_val_cpf(val)
        if result == cpf % 10:
            return
    raise ValidationError(
        (_('Please, enter a valid CPF')), code='invalid'
    )


def valid_cnpj(cnpj):
    val = cnpj // 100
    result = calculate_val_cnpj(val)
    if result == (cnpj // 10) % 10:
        val = cnpj // 10
        result = calculate_val_cnpj(val)
        if result == cnpj % 10:
            return
    raise ValidationError(
        (_('Please, enter a valid CPF')), code='invalid'
    )


def cpf_validator(str_id):
    try:
        id = int(str_id)
    except ValueError:
        raise ValidationError(
            (_('Invalid CPF')), code='invalid'
        )
    if len(str_id) == 11:
        valid_cpf(id)
    elif len(str_id) == 14:
        valid_cnpj(id)
    else:
        raise ValidationError(
            (_('Invalid CPF')), code='invalid'
        )
