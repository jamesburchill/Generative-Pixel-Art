"""
James C. Burchill - September 6, 2021
This script takes a TEXT file and generates PIXEL ART from it.
The file must be called "source.txt" and placed in the _data folder.
The program uses the number of characters to calculate the size of the art (the max x/y dimensions.)
It randomly generates/assigns RBG colours to various character sets - these are later used to DRAW the pixel art.
The program will generate 1 JPG image or as many as you ask for. The art file is saved into the project root.
"""

import sys
import pygame
import datetime
import random
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Book:

    def __init__(self):

        self.book_file: str = "./src/_data/source.txt"

        # open the _data and start crunching the TEXT _data (see below)
        with open(self.book_file) as f:
            try:
                self.characters: str = f.read()  # reads in entire text file into one big string
            except:
                raise RuntimeError("[ERROR] Couldn't find/read source file ...")

        # Assume the _data's length is the square, and each character are the points
        # Getting the SQRT will give you an even XY coord for use.
        # eg. if the total character count was 1600, then the image would be 40 x 40 pixels.
        self.xy: int = int(math.sqrt(len(self.characters)))

        # set the RGB values for the 'pen' (BLACK)
        self.pen_red: int = 0
        self.pen_green: int = 0
        self.pen_blue: int = 0

        self.Upper: dict = {}
        self.Lower: dict = {}
        self.Number: dict = {}
        self.Other: dict = {}

    def generate_colours(self):

        """Assign an RGB value to each letter & number
            Upper A-Z / Lower a-z / Numbers 0-9 / Others
        """
        upper_letters: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower_letters: str = "abcdefghijklmnopqrstuvwxyz"
        numbers: str = "0123456789"
        others: str = "~!@#$%^&*()_+=-][}{\|'/;:?.>,<"

        # uncomment the next line to use the number of common words as the seed - the _data drives the randomness!
        #random.seed(len(self.most_common_words))

        for UL in upper_letters:
            RGB: list = []
            for r in range(3):
                RGB.append(random.randint(0, 255))
            self.Upper[UL] = RGB

        for LL in lower_letters:
            RGB: list = []
            for r in range(3):
                RGB.append(random.randint(0, 255))
            self.Lower[LL] = RGB

        for NN in numbers:
            RGB: list = []
            for r in range(3):
                RGB.append(random.randint(0, 255))
            self.Number[NN] = RGB

        for OO in others:
            RGB: list = []
            for r in range(3):
                RGB.append(random.randint(0, 255))
            self.Other[OO] = RGB

    def get_pen_colour(self, c):
        # find 'c' in lists. Get RGB values for 'pen'
        if c in self.Upper:
            return self.Upper[c]
        elif c in self.Lower:
            return self.Lower[c]
        elif c in self.Number:
            return self.Number[c]
        elif c in self.Other:
            return self.Other[c]
        else:
            # Can't MATCH the character so set the colour to WHITE
            return WHITE

def main(b: Book):

    pygame.init()

    SIZE = width, height = b.xy, b.xy
    SCREEN = pygame.display.set_mode(SIZE)
    SCREEN.fill(WHITE)

    n = input("How many versions would you like to generate? Enter a number or press [ENTER] for 1 > ")
    if n == '':
        n = 1
    else:
        n = int(n)
    for g in range(n):
        print(f'[PROCESSING IMAGE {g+1}]' + '.'*(g+1))

        # THE MAIN DOT PRINTING LOOP
        x,y = 0,0
        b.generate_colours() # generate the colours for the characters

        for CHAR in b.characters:
            if x < b.xy:
                x += 1
            else:
                y += 1
                x = 0
            COLOUR = b.get_pen_colour(CHAR)
            # set RADIUS between 1 and 4 pixels (feel free to change these values for fun)
            RADIUS = random.randint(1,4)
            if COLOUR == WHITE: # make not matched chars bigger white dots ... sometimes!
                RADIUS = random.randint(0,3)
            # Draw the dot (actually it's a teeny circle!) on the SCREEN at x,y with RADIUS
            pygame.draw.circle(SCREEN, COLOUR, (x, y), RADIUS)
        # When the loop is done, save the image to file.
        pygame.image.save(SCREEN, "GENART-" + str(datetime.datetime.now()) + ".jpg")
    # END OF LOOP
    print("Done!")

if __name__ == "__main__":
    b = Book() # create a book object and read in the ./_data/course.txt file for prcessing
    main(b)