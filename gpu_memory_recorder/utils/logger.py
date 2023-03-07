import numpy

class color:
    W = '\033[0m'   # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
    P = '\033[35m'  # purple


class Logger(object):
    def __init__(self, source=None, note=None, log_level=2):
        self.log_level = log_level
        self.source = source
        self.note = note

    @staticmethod
    def red(text):
        return color.R + str(text) + color.W

    @staticmethod
    def green(text):
        return color.G + str(text) + color.W

    @staticmethod
    def orange(text):
        return color.O + str(text) + color.W

    @staticmethod
    def blue(text):
        return color.B + str(text) + color.W

    @staticmethod
    def purple(text):
        return color.P + str(text) + color.W

    @staticmethod
    def white(text):
        return color.W + str(text) + color.W

    def log(self, *args, **kw):
        if ('log_level' in kw):
            log_level = kw['log_level']
        else:
            log_level = 1

        if ('source' in kw):
            source = kw['source']
        else:
            source = None

        if ('note' in kw):
            note = kw['note']
        else:
            note = None

        if (log_level < self.log_level):
            if (source is not None):
                the_source = source
            elif (self.source is not None):
                the_source = self.source

            if (self.note is not None and note is not None):
                print('(' + self.green(the_source) + ' [' + self.blue(self.note) + '|' + self.blue(note) + ']):')
            elif (note is not None):
                print('(' + self.green(the_source) + ' [' + self.blue(note) + ']):')
            elif (self.note is not None):
                print('(' + self.green(the_source) + ' [' + self.blue(self.note) + ']):')
            else:
                print('(' + self.green(the_source) + '):')

            for message in args:
                if isinstance(message, (int, float, numpy.float32, numpy.ndarray)):
                    print(self.green(message))
                else:
                    print(message)
            print

    def stars(self, length=100):
        print('*' * length)

    def line(self, length=100):
        print('-' * length)
