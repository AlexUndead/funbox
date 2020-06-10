import re


def get_domains(links):
    """Функция собирает и возвращает уникальные домены из ссылок"""
    if not links:
        return []

    domains = []

    for link in links:
        part_link = re.search('((ftp|http|https):\/\/)?([A-Za-z_0-9.-]+).*', link)
        if part_link:
            domain = part_link.group(3)
            domains.append(domain)

    return set(domains)
