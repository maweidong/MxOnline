import string
from random import choice


def generate_random(random_length, type):
    """
    生成验证码 0:纯数字  1：数字+字符  2：数字+字符+特殊字符
    :return:
    """
    if type == 0:
        random_seed = string.digits
    elif type == 1:
        random_seed = string.digits + string.ascii_letters
    elif type == 2:
        random_seed = string.digits + string.ascii_letters + string.punctuation
    random_str = []
    while (len(random_str) < random_length):
        random_str.append(choice(random_seed))
    return ''.join(random_str)


if __name__ == '__main__':
    code = generate_random(4, 0)

    print(code)
