import validators


# validation url address
def validate(url: str) -> str:
    err = ''
    if not url:
        err = 'URL обязателен'
    elif len(url) > 255:
        err = 'URL превышает 255 символов'
    elif not validators.url(url):
        err = 'Некорректный URL'
    return err
