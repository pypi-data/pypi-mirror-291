import os


def save_file(text, filename):
    with open(filename, "w") as file:
        file.write(text)


def read_b3text(text: str, data=None):
    if data:
        for k, v in data.items():
            t = "{{{" + k + "}}}"
            if t in text:
                text = text.replace(t, str(v))
    return text


def read_b3file(filename: str, data=None):
    with open(filename, "r") as file:
        text = file.read()
    return read_b3text(text, data=data)


def copy_b3file(srcfile: str, destfile: str, data=None, mode=None, owndata=None):
    text = read_b3file(srcfile, data=data)
    save_file(text, destfile)
    if mode:
        os.chmod(destfile, mode)
    if owndata:
        os.chown(destfile, **owndata)
    return destfile
