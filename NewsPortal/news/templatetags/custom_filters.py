from django import template


register = template.Library()

@register.filter()
def censor(value):
    bad_word = ['дура', 'дурак', 'редиска']
    for word in bad_word:
        value = value.lower().replace(word, '*'*len(word))
    return value

# text = 'Этот РеДиска сдаст нас при первом шухере'
# t = censor(text)
# print(t)