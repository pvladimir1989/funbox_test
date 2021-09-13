from urllib.parse import urlparse


def clean_links(links: list) -> list:
    clean_lst = []

    for link in links:
        parsed = urlparse(link)
        lnk = parsed.netloc or parsed.path
        clean_lst.append(lnk)

    return clean_lst


