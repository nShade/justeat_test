from json_checker import Checker, CheckerError


def assert_json(template, json, error_annotation):
    try:
        Checker(template, soft=True).validate(json)
    except CheckerError as validation_error:
        raise AssertionError(f'{error_annotation}\n{validation_error}')

