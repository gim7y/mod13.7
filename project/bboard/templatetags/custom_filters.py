from django import template

register = template.Library()

bannedList = ['идиот', 'придурок', 'черт', 'козел']

@register.filter(name='censor')  # ms - лаконично
def hide_forbidden(value):
    words = value.split()
    result = []
    for word in words:
        if word in bannedList:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)


# @register.filter(name='censor')  # No 0
# def censor(val, arg):
#     bannedList = ['идиот', 'придурок', 'черт', 'козел']
#     text = val
#     result = ''
#
#     for word in bannedList:
#         data = text.lower().replace(word, arg * len(word))
#         text = data
#
#     for i in range(len(val)):
#         if val[i] != text[i]:
#             result += text[i].upper()
#         else:
#             result += text[i]
#
#     return result
