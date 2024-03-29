from pynput import keyboard
import time
from datetime import datetime

Snippets = {
    'hh1': '# ',
    'hh2': '## ',
    'hh3': '### ',
    'hh4': '#### ',
    '!note' : '> [!note]',
    '!tldr' : '> [!tldr]',
    '!tip' : '> [!tip]',
    '!success' : '> [!success]',
    '!question' : '> [!question]',
    '!fail' : '> [!fail]',
    '!error' : '> [!error]',
    '!bug' : '> [!bug]',
    '!example' : '> [!example]',
    '!quote' : '> [!quote]',
    '!all' : '> [!note]\n\n> [!tldr]\n\n> [!tip]\n\n> [!success]\n\n> [!question]\n\n> [!fail]\n\n> [!error]\n\n> [!bug]\n\n> [!example]\n\n> [!quote]\n\n'
}

typing_word = []

def logging(log):
    with open ('log','a') as file:
        file.write(f'{log}\n')
        file.close()
    
def replace_word(key, snippet):
    try:
        # Delete Key
        for e in range (len(key) + 1):
            time.sleep(0.05)
            keyboard.Controller().press(keyboard.Key.backspace)

        keyboard.Controller().release(keyboard.Key.backspace)

        # Enter snippet
        keyboard.Controller().type(snippet)

    except Exception as ex:
        exception_to_log = f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} : {ex}'
        logging(exception_to_log)


def check_for_snippet(typedword):
    if typedword in Snippets.keys():
        return True


def on_press(key):
    try:
        typing_word.append(key.char)
    except AttributeError:
        if key == keyboard.Key.backspace:
            if(len(typing_word) > 0):
                typing_word.pop()
        
        if key == keyboard.Key.enter:
            typing_word.clear()


def on_release(key):
    if key == keyboard.Key.space:
        # Check for any matching snippets
        typed_word = ''.join([str(letter) for letter in typing_word])

        if check_for_snippet(typed_word):
            replace_word(typed_word, Snippets[typed_word])
            typing_word.clear()
    
        else:
            typing_word.clear()

    if key == keyboard.Key.backspace:
        if(len(typing_word) > 0):
            typing_word.pop()

    if key == keyboard.Key.enter:
        typing_word.clear()
    
# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
