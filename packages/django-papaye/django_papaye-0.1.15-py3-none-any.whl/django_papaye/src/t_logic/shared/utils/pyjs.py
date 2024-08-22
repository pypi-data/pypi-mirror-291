# __pragma__('skip')
require = dict
Date = None
WebSocket = None


class window:
    bootstrap = None
    host = None
    PROTOCOL = None

    @staticmethod
    def addEventListener(type, listener, options=None):
        return None

    @staticmethod
    def scrollTo(x, y):
        return None

    class location:
        href = None
        pathname = None

    class history:
        @staticmethod
        def pushState(state, unused, url):
            return None


class document:
    body = None
    cookie = str
    innerText = str
    innerHTML = str
    classList = None
    parentElement = None
    lastElementChild = None
    style = None

    @staticmethod
    def getElementById(obj):
        return document

    @staticmethod
    def querySelector(obj):
        return document

    @staticmethod
    def querySelectorAll(objs):
        return [document]

    @staticmethod
    def addEventListener(type, listener, options=None):
        return None

    @staticmethod
    def removeEventListener(type, listener, options=None):
        return None

    @staticmethod
    def insertAdjacentHTML(position, text):
        return None

    @staticmethod
    def createElement(element_type):
        return None

    @staticmethod
    def click():
        return None

    @staticmethod
    def remove():
        return None


class event:
    currentTarget = None

    @staticmethod
    def preventDefault():
        return None

    @staticmethod
    def stopPropagation():
        return None


class Math:
    @staticmethod
    def abs(obj):
        return None

    @staticmethod
    def ceil(obj):
        return None


class console:
    @staticmethod
    def log(*args):
        return None

    @staticmethod
    def info(obj):
        return None


class JSON:
    @staticmethod
    def stringify(value, replacer=None, space=None):
        return None

    @staticmethod
    def parse(text, reviver=None):
        return None


class DOMEl(document):
    pass


def alert(message):
    return None


def setTimeout(handler, timeout):
    return None


def setInterval(code, delay):
    return None


def typeof(obj):
    return None

# __pragma__('noskip')
