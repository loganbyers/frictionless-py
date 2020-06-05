from goodtables import validate


# Blacklisted Value


def test_validate_blacklisted_value():
    report = validate(
        'data/table.csv',
        extra_checks=[('rules/blacklisted-value', {'fieldName': 'id', 'blacklist': [2]})],
    )
    assert report.flatten(['rowPosition', 'fieldPosition', 'code']) == [
        [3, 1, 'rules/blacklisted-value'],
    ]


def test_validate_blacklisted_value_task_error():
    report = validate(
        'data/table.csv',
        extra_checks=[
            ('rules/blacklisted-value', {'fieldName': 'bad', 'blacklist': [2]})
        ],
    )
    assert report.flatten(['rowPosition', 'fieldPosition', 'code']) == [
        [None, None, 'task-error'],
    ]


def test_validate_blacklisted_value_many_rules():
    source = [
        ['row', 'name'],
        [2, 'Alex'],
        [3, 'John'],
        [4, 'mistake'],
        [5, 'error'],
        [6],
    ]
    report = validate(
        source,
        extra_checks=[
            ('rules/blacklisted-value', {'fieldName': 'row', 'blacklist': [10]}),
            ('rules/blacklisted-value', {'fieldName': 'name', 'blacklist': ['mistake']}),
            ('rules/blacklisted-value', {'fieldName': 'row', 'blacklist': [10]}),
            ('rules/blacklisted-value', {'fieldName': 'name', 'blacklist': ['error']}),
        ],
    )
    assert report.flatten(['rowPosition', 'fieldPosition', 'code']) == [
        [4, 2, 'rules/blacklisted-value'],
        [5, 2, 'rules/blacklisted-value'],
        [6, 2, 'missing-cell'],
    ]


def test_validate_blacklisted_value_many_rules_with_non_existent_field():
    source = [
        ['row', 'name'],
        [2, 'Alex'],
    ]
    report = validate(
        source,
        extra_checks=[
            ('rules/blacklisted-value', {'fieldName': 'row', 'blacklist': [10]}),
            ('rules/blacklisted-value', {'fieldName': 'bad', 'blacklist': ['mistake']},),
        ],
    )
    assert report.flatten(['rowPosition', 'fieldPosition', 'code']) == [
        [None, None, 'task-error'],
    ]
