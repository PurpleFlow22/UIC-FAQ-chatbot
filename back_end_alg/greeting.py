import random

start = ['您好，很高兴为您服务。', '您好，请问有什么可以帮您？', '亲！我是您的专属服务顾问，很高兴为您服务。']
check = ['请问您还有什么问题吗？', '亲还有什么想了解的吗？']
pre = ['亲，这是我找到的回答，请查收：', '为您找到了以下回答：']
none_reply = ['找不到您所需要的答案', '抱歉，有些听不懂你说的话呢', '抱歉不太听懂，请问能换个说法再问一遍吗~']


def greet_start():
    return random.choice(start)


def greet_check():
    return random.choice(check)


def greet_pre():
    return random.choice(pre)


def greet_none_reply():
    return random.choice(none_reply)
