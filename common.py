from nltk.corpus import words

colemak = "qwfpgjluy;arstdhneiozxcvbkm"
qwerty  = "qwertyuiopasdfghjkl;zxcvbnm"
chars = set(colemak)
colemak_to_qwerty = {k: v for k, v in zip(colemak, qwerty)}
qwerty_to_colemak = {v: k for k, v in zip(colemak, qwerty)}

def convert(word):
    return ''.join(colemak_to_qwerty.get(char.lower(), ' ') for char in word)

QWERTY = "qwerty"
COLEMAK = "colemak"

PICKLE_PATH = "cache.p"

NGRAMS = 4
MAX_LOG_LENGTH = 2 ** 22
SIGNAL_THRESHOLD = 0.25

COLEMAK_WORDS = [word.lower() for word in words.words()]
QWERTY_WORDS = [convert(word) for word in words.words()]

def roll(word, n):
    padding = ' ' * (n - 1)
    padded = padding + word + padding
    for i in range(len(padded) - n + 1):
        yield ''.join(c if c in chars else ' ' for c in padded[i:i + n])

keycodes = {
  "a"             : 0x00,
  "s"             : 0x01,
  "d"             : 0x02,
  "f"             : 0x03,
  "h"             : 0x04,
  "g"             : 0x05,
  "z"             : 0x06,
  "x"             : 0x07,
  "c"             : 0x08,
  "v"             : 0x09,
  "b"             : 0x0B,
  "q"             : 0x0C,
  "w"             : 0x0D,
  "e"             : 0x0E,
  "r"             : 0x0F,
  "y"             : 0x10,
  "t"             : 0x11,
  "1"             : 0x12,
  "2"             : 0x13,
  "3"             : 0x14,
  "4"             : 0x15,
  "6"             : 0x16,
  "5"             : 0x17,
  "="             : 0x18,
  "9"             : 0x19,
  "7"             : 0x1A,
  "-"             : 0x1B,
  "8"             : 0x1C,
  "0"             : 0x1D,
  "]"             : 0x1E,
  "o"             : 0x1F,
  "u"             : 0x20,
  "["             : 0x21,
  "i"             : 0x22,
  "p"             : 0x23,
  "l"             : 0x25,
  "j"             : 0x26,
  "'"             : 0x27,
  "k"             : 0x28,
  ";"             : 0x29,
  "/"             : 0x2A,
  ","             : 0x2B,
  "\\"            : 0x2C,
  "n"             : 0x2D,
  "m"             : 0x2E,
  "."             : 0x2F,
  "`"             : 0x32,
  "*"             : 0x43,
  "+"             : 0x45,
  "Return"        : 0x24,
  "Tab"           : 0x30,
  "Space"         : 0x31,
  " "             : 0x31,
  "Delete"        : 0x33,
  "Escape"        : 0x35,
  "\x1b"          : 0x35,
  "Command"       : 0x37,
  "Shift"         : 0x38,
  "CapsLock"      : 0x39,
  "Option"        : 0x3A,
  "Control"       : 0x3B,
  "RightCommand"  : 0x36,
  "RightShift"    : 0x3C,
  "RightOption"   : 0x3D,
  "RightControl"  : 0x3E,
  "Function"      : 0x3F,
  "F17"           : 0x40,
  "VolumeUp"      : 0x48,
  "VolumeDown"    : 0x49,
  "Mute"          : 0x4A,
  "F18"           : 0x4F,
  "F19"           : 0x50,
  "F20"           : 0x5A,
  "F5"            : 0x60,
  "F6"            : 0x61,
  "F7"            : 0x62,
  "F3"            : 0x63,
  "F8"            : 0x64,
  "F9"            : 0x65,
  "F11"           : 0x67,
  "F13"           : 0x69,
  "F16"           : 0x6A,
  "F14"           : 0x6B,
  "F10"           : 0x6D,
  "F12"           : 0x6F,
  "F15"           : 0x71,
  "Help"          : 0x72,
  "Home"          : 0x73,
  "PageUp"        : 0x74,
  "ForwardDelete" : 0x75,
  "F4"            : 0x76,
  "End"           : 0x77,
  "F2"            : 0x78,
  "PageDown"      : 0x79,
  "F1"            : 0x7A,
  "LeftArrow"     : 0x7B,
  "RightArrow"    : 0x7C,
  "DownArrow"     : 0x7D,
  "UpArrow"       : 0x7E
}