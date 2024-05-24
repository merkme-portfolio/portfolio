import re


def find_pep_number(exp):
    return re.search(r'PEP (\d+)', exp).group(1)


def get_pep_name(exp):
    return exp.split(' – ')[-1]
