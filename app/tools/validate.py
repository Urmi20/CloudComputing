import re


class regex:

    def __init__(self):
        self.user_name_pattern = "^[a-zA-Z][a-zA-Z0-9-_\\.]{1,20}$"
        self.first_name_pattern = "[a-zA-Z ]{3,45}$"
        self.last_name_pattern = "^[a-zA-Z ][a-zA-Z0-9-. ]{1,100}$"
        self.email_pattern = "[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,3}$"
        self.password_pattern = "(?=^.{8,}$)((?=.*\\d)|(?=.*\\W+))(?![.\\n])(?=.*[A-Z])(?=.*[a-z]).*$"
        self.photo_title_pattern = "^[a-zA-Z ][a-zA-Z0-9-. ]{3,45}$"
        self.photo_hashtag_pattern = "\\B(\\#[a-zA-Z-_0-9 ]+\\b)(?!;)"

    def validate(self, pattern, value):
        if re.search(pattern, value):
            return value
        else:
            return False
