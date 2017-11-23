# Defines

class Defines:
    BOARD_SIZE = 19

    HOW_MANY_GAMES_TO_USE = 100000

class COLOUR:
        	EMPTY = 0
        	BLACK = 1
        	WHITE = 2

colour_names = { COLOUR.EMPTY: "Empty", COLOUR.BLACK: "Black", COLOUR.WHITE: "White"}
inverted_colour = { COLOUR.EMPTY: COLOUR.EMPTY, COLOUR.BLACK: COLOUR.WHITE, COLOUR.WHITE: COLOUR.BLACK}
