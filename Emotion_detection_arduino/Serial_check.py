from pyfirmata2 import ArduinoMega, util, STRING_DATA
board = ArduinoMega('/dev/ttyUSB0')
def msg( text ):
    if text:
        board.send_sysex( STRING_DATA, util.str_to_two_byte_iter( text ) )
