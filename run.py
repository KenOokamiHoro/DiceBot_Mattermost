import re
import sys
import random
import logging

from mmpy_bot.bot import Bot
from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to


@respond_to('!ping')
@listen_to('!ping')
def pong(message):
    '''It just replied pong.'''
    message.reply('pong')


@respond_to('!roll (.*)')
@listen_to('!roll (.*)')
def roll(message, expression):
    '''
    Rolling dices.
        Basic Usage:
            !roll [status]<dice>d<side>[expression]

            Roll <dice> dices with <side> sides. 
            And execute some expression for result.
    '''
    roll_re = re.compile(r'(\d+)?d(\d+)')

    try:
        selection = re.search(roll_re, expression)
        assert selection
    except AssertionError:
        message.reply(_("Inappropriate expression."))

    # Get dices and sides
    (dice, side) = [int(x or 1) for x in selection.groups()]
    expression = re.split(roll_re, expression)[-1]

    try:
        assert (dice > 0 and dice < 101 and side > 0 and side < 101)
    except AssertionError:
        message.reply(
            _("Inappropriate dice or side. (0<dice<=100, 0<side<=100)"))
    else:
        L = [0] * dice
        for i in range(dice):
            L[i] = random.randrange(1, side+1)

        if expression:
            try:
                result = [str(eval(str(x)+expression)) for x in L]
            except (ValueError, NameError) as err:
                message.reply(f"Expression execute failed:{str(err)}")
        else:
            result = [str(x) for x in L]
        message.reply(" and ".join(result))
            


if __name__ == "__main__":
    logging.basicConfig(**{
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG,
        'stream': sys.stdout,
    })
    Bot().run()
