def files_as_text(file_contents):
    """Turns {path: content} into one text block with line numbers."""
    text = ""
    for path, content in file_contents.items():
        text += f"### File: {path}\n"
        for number, line in enumerate(content.split("\n"), start=1):\
            text += f"{number}: {line}\n"
        text += "\n"
        return text