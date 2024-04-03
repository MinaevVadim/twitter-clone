ALLOWED_EXTENSIONS: list[str] = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


async def file_check(file_name) -> bool:
    return '.' in file_name and file_name.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
