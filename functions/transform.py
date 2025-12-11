# from .config.parsing import acordaos_1_config

import bs4


def last_word_from_text(element: bs4.element.Tag):
    return element.get_text().strip().split(" ")[-1]


def get_text(element: bs4.element.Tag):
    return element.get_text().strip()

