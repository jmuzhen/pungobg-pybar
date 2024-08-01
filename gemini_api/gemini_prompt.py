SYSTEM_PROMPT_PATH = "prompts/system_prompt.txt"


def get_system_prompt():
    return get_system_file(SYSTEM_PROMPT_PATH)


def get_system_file(FILE_PATH):
    with open(FILE_PATH, "r") as file:
        return file.read()
