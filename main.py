# test webhook

def main():
    user_age = 25
    user_name = "John"
    page = 2

    print(f"User age: {user_age}")


class UserAge:
    def __init__(self, age):
        self.age = age

    def get_age(self):
        return self.age

    def set_age(self, age):
        self.age = age

    def set_credit_card(self, cc):
	self.credit_card = cc

    def __str__(self):
        return f"User age: {self.age}"
