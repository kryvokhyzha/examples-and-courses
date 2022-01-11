char_line = u'\u2500'
char_lcorner_top = u'\u250C'
char_rcorner_top = u'\u2510'
char_lside = u'\u251C'
char_rside = u'\u2524'
char_top = u'\u252C'
char_bot = u'\u2534'
char_cross = u'\u253C'
char_lcorner_bot = u'\u2514'
char_rcorner_bot = u'\u2518'


def top_rule(width, ncols):
    return char_lcorner_top + char_top.join([char_line * width for i in range(ncols)]) + char_rcorner_top


def bot_rule(width, ncols):
    return char_lcorner_bot + char_bot.join([char_line * width for i in range(ncols)]) + char_rcorner_bot


def mid_rule(width, ncols):
    return char_lside + char_cross.join([char_line * width for i in range(ncols)]) + char_rside


def fmt_row(row, width, loffset):
    return "|" + "|".join([str(cell).ljust(width - loffset).rjust(width) for cell in row]) + "|"
