from scrapper.models import Profile


def ident_provider(email: str):
    not_identified = 'UNKNOWN'
    providers = {
        'YANDEX': ['ya.ru', 'yandex.ru'],
        'MAIL': ['mail.ru', 'inbox.ru', 'bk.ru', 'list.ru'],
        'GOOGLE': ['gmail.com'],
        'RAMBLER': ['rambler.ru'],
    }

    if not email:
        return None

    for provider_name, provider_domains in providers.items():
        for domain in provider_domains:
            if domain in email:
                return provider_name

    return not_identified
