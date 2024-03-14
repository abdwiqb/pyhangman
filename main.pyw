from tkinter import *
import random
import pygame
import json

with open('words.json', 'r') as f:
    WORD_LIST = json.loads(f.read())

MAX_STRIKES = 7
WIN_WIDTH = 550
WIN_HEIGHT = 430

FONT_NAME = 'consolas'
BG_C = '#000'
TEXT_C = '#FFF'
WRONG_C = '#F00'
RIGHT_C = '#0F0'
HINT_C = '#777'
BUTTON_C = '#333'

pygame.mixer.init()

correct_sound = pygame.mixer.Sound('sounds\\correct.wav')
strike_sound = pygame.mixer.Sound('sounds\\strike.wav')
win_sound = pygame.mixer.Sound('sounds\\win.wav')
loss_sound = pygame.mixer.Sound('sounds\\loss.wav')
button_sound = pygame.mixer.Sound('sounds\\button.wav')

word = random.choice(list(WORD_LIST.keys()))
word_hints = WORD_LIST.get(word)
last_word = word

correct = []
strikes = []
hints = []

win = Tk()
win.geometry(f'{WIN_WIDTH}x{WIN_HEIGHT}')
win.resizable(False, False)
win.title('Hangman')
win.config(bg=BG_C)

hint_label = Label(text='No Hints Taken', font=(FONT_NAME, 12), bg=BG_C, fg=HINT_C)
hint_label.pack(side='top', pady=(30, 0))

main_frame = Frame(bg=BG_C)
main_frame.pack()

striked_label = Label(main_frame, text='No Strikes', font=(FONT_NAME, 16), bg=BG_C, fg=WRONG_C)
striked_label.pack(pady=(80, 20))

word_label = Label(main_frame, text='_'*len(word), font=(FONT_NAME, 16), bg=BG_C, fg=TEXT_C)
word_label.pack(pady=20)

button_frame = Frame(bg=BG_C)
button_frame.pack(pady=20)

reset_button = Button(button_frame, text='NEW WORD', font=(FONT_NAME, 14), bg=BUTTON_C, fg=TEXT_C,
                      command=lambda:new_word())
reset_button.grid(row=0, column=0, padx=10)

hint_button = Button(button_frame, text='GET HINT', font=(FONT_NAME, 14), bg=BUTTON_C, fg=TEXT_C,
                     command=lambda:get_hint())
hint_button.grid(row=0, column=1, padx=10)


# funcs
def new_word():

    global correct, strikes, hints, word_hints, word, last_word
    
    while word == last_word:
        word = random.choice(list(WORD_LIST.keys()))
    last_word = word
    word_hints = WORD_LIST.get(word)
    
    correct = []
    strikes = []
    hints = []
    button_sound.play()
    hint_label.config(text='No Hints Taken')
    striked_label.config(text='No Strikes', fg=WRONG_C)
    word_label.config(text='_'*len(word), fg=TEXT_C)


def get_hint():

    global hints, hint_label, word_hints

    button_sound.play()

    if check_guesses() == None:
        for i in word_hints:
            if i in hints:
                continue
            hints.append(i)
            hint_label.config(text=', '.join(hints))
            break
    else:
        hint_label.config(text='Click \"NEW WORD\" to restart')


def update_mainf():
    
    if not strikes:
        striked_label.config(text='No Strikes')
    else:
        striked_label.config(text=', '.join(strikes))

    shown_label = []
    for i in word:
        if i in correct:
            shown_label.append(i)
        else:
            shown_label.append('_')

    word_label.config(text=''.join(shown_label))


def check_guesses():
    
    global word, correct, strikes

    if len(strikes) >= MAX_STRIKES:
        striked_label.config(text='You didnt get the word')
        word_label.config(text=f'{word}', fg=WRONG_C)
        loss_sound.play()
        return False
    for c in word:
        if c not in correct:
            return None
    striked_label.config(text='You got the word right!', fg=RIGHT_C)
    word_label.config(text=f'{word}', fg=RIGHT_C)
    win_sound.play()
    return True


def take_guess(key):
    
    global word, correct, strikes

    char = key.char

    if char in correct or char in strikes:
        return None
    if check_guesses() == None:
        if char in word:
            correct.append(char)
            correct_sound.play()
        else:
            strikes.append(char)
            strike_sound.play()
        update_mainf()
        check_guesses()


def main():
    
    for k in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
        win.bind(f'<{k}>', lambda k=k:take_guess(k))

    win.mainloop()


if __name__ == '__main__':
    main()
