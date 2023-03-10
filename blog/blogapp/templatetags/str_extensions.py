from django.template import Library
from django.template.defaultfilters import stringfilter
register = Library()
def capitalize(inputstr):
    return inputstr.capitalize()

def del_word(inputstr):
    return inputstr.replace(inputstr, f'<del>{inputstr}</del>')
def superoutput(inputstr):
    # Главная страница
    # ГлАвНаЯ СтРаНиЦа
    # result = []
    # for i in range(len(inputstr)):
    #     letter = inputstr[i]
    #     if i % 2 == 0:
    #         letter = letter.upper()
    #     result.append(letter)
    # return ''.join(result)

    #
    return ''.join([inputstr[i].upper() if i % 2 == 0 else inputstr[i] for i in range(len(inputstr))])

register.filter('del_word', del_word)
register.filter('capitalize', capitalize)
register.filter('sup', superoutput)