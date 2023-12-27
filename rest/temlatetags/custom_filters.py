from django import template


register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.


SWEAR_WORDS = [
    'апездал', 'апездошенная', 'блядь', 'блядство', 'выебон', 'выебать', 'вхуюжить', 'гомосек', 'долбоёб', 'ебло',
    'еблище', 'ебать', 'ебическая сила', 'ебунок', 'еблан', 'ёбнуть', 'ёболызнуть', 'ебош', 'заебал', 'заебатый',
    'злаебучий', 'заёб', 'колдоебина', 'манда', 'мандовошка', 'мокрощелка', 'наебка', 'наебал',
    'наебаловка', 'напиздеть', 'отъебись', 'охуеть', 'отхуевертить', 'опизденеть', 'охуевший', 'отебукать', 'пизда',
    'пидарас', 'пиздатый', 'пиздец', 'пизданутый', 'поебать', 'поебустика', 'проебать', 'подзалупный', 'пизденыш',
    'припиздак', 'разъебать', 'распиздяй', 'разъебанный', 'сука', 'сучка', 'трахать', 'уебок', 'уебать', 'угондошить',
    'уебан', 'хитровыебанный', 'нахуй', 'хуй', 'хуйня', 'хуета', 'хуево', 'хуесос', 'хуеть', 'хуевертить', 'хуеглот',
    'хуистика', 'членосос', 'членоплет', 'шлюха'
]

@register.filter()
def censor(value):
    text = str(value)
    for word in SWEAR_WORDS:
        text = text.replace(word[1:], "*" * (len(word)-1))
    return text
