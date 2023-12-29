import re

keyword = "age"
camel_case_keyword = keyword.capitalize()
re_keywords = f"({re.escape(keyword)}|{re.escape(camel_case_keyword)}|{re.escape(keyword.upper())})"
re_keywords_no_caps = f"({re.escape(keyword)}|{re.escape(camel_case_keyword)})"

pattern = re.compile(
    r"""
    # Matches the keyword as a standalone word
    (?<!\w){re_keywords}(?!\w)
    # Matches CamelCase occurrences of the keyword
    |(?<=[a-z]){camel_case_keyword}(?=[A-Z]|\W|\d|_|$)
    # Matches the keyword at the beginning of the string, followed by specific characters
    |(?:^{re_keywords_no_caps}(?=[A-Z]|\W|\d|_|$))
    # Matches the keyword at the beginning of the string, followed by non-word characters, digits, or underscores
    |(?:^{re_keywords}(?=\W|\d|_|$))
    # Matches the keyword surrounded by non-word characters, digits, or underscores
    |(?<=\W|\d|_){re_keywords}(?=\W|\d|_|$)
    """.format(
        re_keywords=re_keywords,
        camel_case_keyword=camel_case_keyword,
        re_keywords_no_caps=re_keywords_no_caps,
    ),
    re.VERBOSE,
)

# Test strings
test_strings = [
    "age",
    "age!",
    "user/age",
    "user#age",
    "user1age",
    "user?age",
    "3age",
    "age%",
    "age12",
    "age at",
    "print_user_age",
    "def print_user_age(self):",
    "printUserAge",
    "ageCalculator",
    "age_for_user",
    "age-user",
    "Age-user",
    "USER_AGE",
    "print_user_age_now",
    "the user age is calculated",
    "Age is calculated",
    # invalid cases
    "endage",
    "page",
    "user_page = 3",
    "page3",
    "page_user",
    "PAGES",
    "AGES",
    "PAge",
]

for test_string in test_strings:
    if match := pattern.search(test_string):
        print(f"Match found in '{test_string}':", match.group())
    else:
        print(f"No match found in '{test_string}'.")
