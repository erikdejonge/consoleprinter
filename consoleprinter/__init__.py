#!/usr/bin/env python3
# coding=utf-8
"""
console
Active8 (05-03-15)
license: GNU-GPL2
"""
from __future__ import division, print_function, absolute_import, unicode_literals
from future import standard_library

import io
import os
import re
import sys
import code
import copy
import time
import json
import atexit
import base64
import random
import socket
import readline
import traceback
import collections
import unicodedata

# noinspection PyUnresolvedReferences
try:
    from urllib.parse import urlparse
except ImportError:
    # noinspection PyUnresolvedReferences
    from urlparse import urlparse

SINGULARS = [
    (r"(?i)(database)s$", r'\1'),
    (r"(?i)(quiz)zes$", r'\1'),
    (r"(?i)(matr)ices$", r'\1ix'),
    (r"(?i)(vert|ind)ices$", r'\1ex'),
    (r"(?i)^(ox)en", r'\1'),
    (r"(?i)(alias|status)(es)?$", r'\1'),
    (r"(?i)(octop|vir)(us|i)$", r'\1us'),
    (r"(?i)^(a)x[ie]s$", r'\1xis'),
    (r"(?i)(cris|test)(is|es)$", r'\1is'),
    (r"(?i)(shoe)s$", r'\1'),
    (r"(?i)(o)es$", r'\1'),
    (r"(?i)(bus)(es)?$", r'\1'),
    (r"(?i)(m|l)ice$", r'\1ouse'),
    (r"(?i)(x|ch|ss|sh)es$", r'\1'),
    (r"(?i)(m)ovies$", r'\1ovie'),
    (r"(?i)(s)eries$", r'\1eries'),
    (r"(?i)([^aeiouy]|qu)ies$", r'\1y'),
    (r"(?i)([lr])ves$", r'\1f'),
    (r"(?i)(tive)s$", r'\1'),
    (r"(?i)(hive)s$", r'\1'),
    (r"(?i)([^f])ves$", r'\1fe'),
    (r"(?i)(t)he(sis|ses)$", r"\1hesis"),
    (r"(?i)(s)ynop(sis|ses)$", r"\1ynopsis"),
    (r"(?i)(p)rogno(sis|ses)$", r"\1rognosis"),
    (r"(?i)(p)arenthe(sis|ses)$", r"\1arenthesis"),
    (r"(?i)(d)iagno(sis|ses)$", r"\1iagnosis"),
    (r"(?i)(b)a(sis|ses)$", r"\1asis"),
    (r"(?i)(a)naly(sis|ses)$", r"\1nalysis"),
    (r"(?i)([ti])a$", r'\1um'),
    (r"(?i)(n)ews$", r'\1ews'),
    (r"(?i)(ss)$", r'\1'),
    (r"(?i)s$", ''),
]

PLURALS = [
    (r"(?i)(quiz)$", r'\1zes'),
    (r"(?i)^(oxen)$", r'\1'),
    (r"(?i)^(ox)$", r'\1en'),
    (r"(?i)(m|l)ice$", r'\1ice'),
    (r"(?i)(m|l)ouse$", r'\1ice'),
    (r"(?i)(matr|vert|ind)(?:ix|ex)$", r'\1ices'),
    (r"(?i)(x|ch|ss|sh)$", r'\1es'),
    (r"(?i)([^aeiouy]|qu)y$", r'\1ies'),
    (r"(?i)(hive)$", r'\1s'),
    (r"(?i)([lr])f$", r'\1ves'),
    (r"(?i)([^f])fe$", r'\1ves'),
    (r"(?i)sis$", 'ses'),
    (r"(?i)([ti])a$", r'\1a'),
    (r"(?i)([ti])um$", r'\1a'),
    (r"(?i)(buffal|tomat)o$", r'\1oes'),
    (r"(?i)(bu)s$", r'\1ses'),
    (r"(?i)(alias|status)$", r'\1es'),
    (r"(?i)(octop|vir)i$", r'\1i'),
    (r"(?i)(octop|vir)us$", r'\1i'),
    (r"(?i)^(ax|test)is$", r'\1es'),
    (r"(?i)s$", 's'),
    (r"$", 's'),
]

g_sizesystem_verbose = [
    (1024 ** 5, (' Petabyte', ' Petabytes')),
    (1024 ** 4, (' Terabyte', ' Terabytes')),
    (1024 ** 3, (' Gigabyte', ' Gigabytes')),
    (1024 ** 2, (' Megabyte', ' Megabytes')),
    (1024 ** 1, (' Kilobyte', ' Kilobytes')),
    (1024 ** 0, (' Byte', ' Bytes')),
]

g_sizesystem_alternative_lower = [
    (1024 ** 5, ' pb'),
    (1024 ** 4, ' tb'),
    (1024 ** 3, ' gb'),
    (1024 ** 2, ' mb'),
    (1024 ** 1, ' kb'),
    (1024 ** 0, (' b.', ' bytes')),
]

g_sizesystem_alternative = [
    (1024 ** 5, ' PB'),
    (1024 ** 4, ' TB'),
    (1024 ** 3, ' GB'),
    (1024 ** 2, ' MB'),
    (1024 ** 1, ' KB'),
    (1024 ** 0, (' byte', ' bytes')),
]

g_sizesystem_traditional = [
    (1024 ** 5, 'P'),
    (1024 ** 4, 'T'),
    (1024 ** 3, 'G'),
    (1024 ** 2, 'M'),
    (1024 ** 1, 'K'),
    (1024 ** 0, 'B'),
]

g_sizesystem_iec = [
    (1024 ** 5, 'Pi'),
    (1024 ** 4, 'Ti'),
    (1024 ** 3, 'Gi'),
    (1024 ** 2, 'Mi'),
    (1024 ** 1, 'Ki'),
    (1024 ** 0, ''),
]

g_sizesystem_si = [
    (1000 ** 5, 'P'),
    (1000 ** 4, 'T'),
    (1000 ** 3, 'G'),
    (1000 ** 2, 'M'),
    (1000 ** 1, 'K'),
    (1000 ** 0, 'B'),
]

UNCOUNTABLES = {'equipment', 'fish', 'information', 'jeans', 'money', 'rice', 'series', 'sheep', 'species'}

SALPHA = "~ |_.-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
SAFECHARS = [ord(ch) for ch in SALPHA]

g_column_resize_threshold = None
g_start_time = time.time()


class Bar(object):
    """
    Bar
    """
    def __enter__(self):
        """
        __enter__
        """
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        @type exc_type: str
        @type exc_val: str
        @type exc_tb: str
        @return: None
        """
        self.done()
        return False  # we're not suppressing exceptions

    def __init__(self, label='', width=32, hide=None, empty_char=' ', filled_char='#', expected_size=None, every=1):
        """
        @type label: str
        @type width: int
        @type hide: str, None
        @type empty_char: float
        @type filled_char: float
        @type expected_size: int, None
        @type every: int
        @return: None
        """
        self.label = label
        self.width = width
        self.hide = hide

        # Only show bar in terminals by default (better for piping, logging etc.)
        stream = sys.stderr

        if hide is None:
            try:
                self.hide = not stream.isatty()
            except AttributeError:  # output does not support isatty()
                self.hide = True

        self.empty_char = empty_char
        self.filled_char = filled_char
        self.expected_size = expected_size
        self.every = every
        self.start = time.time()
        self.ittimes = []
        self.eta = 0
        self.etadelta = time.time()
        self.etadisp = self.format_time(self.eta)
        self.last_progress = 0
        self.elapsed = 0

        if self.expected_size:
            self.show(0)

    def show(self, progress, count=None):
        """
        @type progress: int
        @type count: str, None
        @return: None
        """
        stream = sys.stderr
        bar_template = '%s|%s%s| \033[34m%s/%s - %s\033[0m\r'

        # How long to wait before recalculating the ETA
        eta_interval = 1

        # How many intervals (excluding the current one) to calculate the simple moving
        # average
        eta_sma_window = 14

        if count is not None:
            self.expected_size = count

        if self.expected_size is None:
            raise Exception("expected_size not initialized")

        self.last_progress = "%.2f" % progress
        self.label = "\033[33m" + self.label + "\033[0m"

        if (time.time() - self.etadelta) > eta_interval:
            self.etadelta = time.time()
            self.ittimes = self.ittimes[-eta_sma_window:] + [-(self.start - time.time()) / (progress + 1)]
            self.eta = sum(self.ittimes) / float(len(self.ittimes)) * (self.expected_size - progress)
            self.etadisp = self.format_time(int(self.eta))

        x = int(self.width * progress // self.expected_size)

        if not self.hide:
            if ((progress % self.every) == 0 or      # True every "every" updates
                    (progress == self.expected_size)):   # And when we're done

                if len(remove_color(self.label.strip())) == 0:
                    bar_template = '%s|%s%s| \033[34m%s/%s\033[0m\r'
                    stream.write(bar_template % (
                        self.etadisp, self.filled_char * x,
                        self.empty_char * (self.width - x), sizeof_fmt(progress),
                        sizeof_fmt(self.expected_size)))
                else:
                    stream.write(bar_template % (
                        self.label, self.filled_char * x,
                        self.empty_char * (self.width - x), sizeof_fmt(progress + 1),
                        sizeof_fmt(self.expected_size), self.etadisp))

                stream.flush()

    def done(self):
        """
        done
        """
        self.elapsed = time.time() - self.start
        elapsed_disp = self.format_time(self.elapsed)
        stream = sys.stderr
        bar_template = '%s|%s%s| \033[32m%s/%s - %s\033[0m\r'
        self.last_progress = "%.1f" % float(self.last_progress)
        self.expected_size = "%.1f" % float(self.expected_size)

        if not self.hide:
            # Print completed bar with elapsed time
            stream.write('\r')
            stream.write('                                                                                        \r')

            if len(remove_color(self.label.strip())) == 0:
                bar_template = '%s|%s%s| \033[34m%s/%s\033[0m\r'
                stream.write(bar_template % (
                    elapsed_disp, self.filled_char * self.width,
                    self.empty_char * 0, self.last_progress,
                    self.expected_size))
            else:
                stream.write(bar_template % (
                    self.label, self.filled_char * self.width,
                    self.empty_char * 0, self.last_progress,
                    self.expected_size, elapsed_disp))

            stream.write('\n')
            stream.flush()

    @staticmethod
    def format_time(seconds):
        """
        @type seconds: int
        @return: None
        """
        return time.strftime('%H:%M:%S', time.gmtime(seconds))


class FastList(object):
    """
    FastList
    """
    def __init__(self):
        """
        __init__
        """
        self.dictlist = {}

    def add(self, o):
        """
        @type o: object
        """
        self.dictlist[o] = 1

    def delete(self, o):
        """
        @type o: str
        """
        if o in self.dictlist:
            del self.dictlist[o]

    def has(self, o):
        """
        @type o: object
        """
        return o in self.dictlist

    def ilist(self):
        """
        list
        """
        return iter(list(self.dictlist.keys()))

    def list(self):
        """
        list
        """
        return list(self.dictlist.keys())

    def size(self):
        """
        size
        """
        return len(list(self.dictlist.keys()))


class Colors(object):
    """
    Colors
    """
    black = "black"
    blue = "blue"
    cyan = "cyan"
    darkcyan = "darkcyan"
    darkgreen = "darkgreen"
    darkmagenta = "darkmagenta"
    darkyellow = "darkyellow"
    default = "default"
    green = "green"
    grey = "grey"
    magenta = "magenta"
    orange = "orange"
    purple = "purple"
    red = "red"
    white = "white"
    yellow = "yellow"


# noinspection PyClassicStyleClass
class HistoryConsole(code.InteractiveConsole):
    """
    HistoryConsole
    """
    def __init__(self, locals2=None, filename="<console>", histfile=os.path.expanduser("~/.console-history")):
        """
        @type locals2: list, None
        @type filename: str
        @type histfile: str
        @return: None
        """
        code.InteractiveConsole.__init__(self, locals2, filename)
        self.init_history(histfile)

    def init_history(self, histfile):
        """
        @type histfile: str
        @return: None
        """
        readline.parse_and_bind("tab: complete")

        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass

            atexit.register(self.save_history, histfile)

    @staticmethod
    def save_history(histfile):
        """
        @type histfile: str
        @return: None
        """
        readline.write_history_file(histfile)


class Info(object):
    """
    Bar
    """
    def __init__(self, *args):
        """
        @type args: tuple
        @return: None
        """
        command = ""

        for i in args:
            command += str(i) + " "

        self.command = command.strip()
        self.items = []

    def __enter__(self):
        """
        __enter__
        """
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        @type exc_type: str
        @type exc_val: str
        @type exc_tb: str
        @return: None
        """
        linenr = get_line_number()

        # print("\033[37m== " + str(self.command), linenr, "==\033[0m")
        longest = 0

        for line in self.items:
            for item in line:
                if len(str(item)) > longest:
                    longest = len(str(item))
                break

        for line in self.items:
            t = True

            for item in line:
                if t:
                    sys.stdout.write("\033[0m" + item + " \033[0m")
                    spaces = " " * (longest - len(remove_escapecodes(item)))
                    sys.stdout.write("\033[0m" + spaces + ": \033[0m")
                    t = False
                else:
                    item = colorize_for_print(str(item))
                    sys.stdout.write("\033[32m" + item + " \033[0m")
                    t = True

            sys.stdout.write("\n")
            sys.stdout.flush()

        return False

    def add(self, *args):
        """
        @type args: list
        @return: None
        """
        self.items.append(args)


class SizeSystems(object):
    """
    SizeSystems
    """
    def __init__(self):
        """
        __init__
        """
        self.traditional = g_sizesystem_traditional
        self.alternative = g_sizesystem_alternative
        self.alternative_lower = g_sizesystem_alternative_lower
        self.verbose = g_sizesystem_verbose
        self.iec = g_sizesystem_iec
        self.si = g_sizesystem_si


class SystemGlobals(object):
    """
    SystemGlobals
    """
    _instance = None
    g_console_printed = set()
    g_width_console_columns = []
    g_safe_alphabet = None
    g_running_in_debugger_unit_tests = None
    g_running_in_debugger = None
    g_slugified_unicode_lut = {}
    g_debug = False
    g_memory = {}

    def __new__(cls, *args, **kwargs):
        """
        @type cls: class
        @type args: tuple
        @type kwargs: dict
        @return:
        @raise:
        """
        if not cls._instance:
            cls._instance = super(SystemGlobals, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        """
        __init__
        """
        pass

    def has(self, k):
        """
        @type k: str
        @return:
        @raise:
        """
        return k in self.g_memory

    def get(self, k):
        """
        @type k: str
        @return:
        @raise:
        """
        if not isinstance(k, str):
            raise AssertionError("keys must be mystring")

        if k not in self.g_memory:
            raise AssertionError(k + " not found")

        return self.g_memory[k]

    def set(self, k, v):
        """
        @type k: str
        @type v: object
        @return:
        @raise:
        """
        if not isinstance(k, str):
            raise AssertionError("keys must be mystring")

        console("SystemGlobals:set", k, once=True, color='grey', line_num_only=3)
        self.g_memory[k] = v


def _irregular(singular, plural):
    """
    @type singular: str
    @type plural: str
    @return: None
    """
    def caseinsensitive(mystring):
        """
        @type mystring: str
        @return: None
        """
        return ''.join('[' + char + char.upper() + ']' for char in mystring)

    if singular[0].upper() == plural[0].upper():
        PLURALS.insert(0, (r"(?i)(%s)%s$" % (singular[0], singular[1:]), r'\1' + plural[1:]))
        PLURALS.insert(0, (r"(?i)(%s)%s$" % (plural[0], plural[1:]), r'\1' + plural[1:]))
        SINGULARS.insert(0, (r"(?i)(%s)%s$" % (plural[0], plural[1:]), r'\1' + singular[1:]))
    else:
        PLURALS.insert(0, (r"%s%s$" % (singular[0].upper(), caseinsensitive(singular[1:])), plural[0].upper() + plural[1:]))
        PLURALS.insert(0, (r"%s%s$" % (singular[0].lower(), caseinsensitive(singular[1:])), plural[0].lower() + plural[1:]))
        PLURALS.insert(0, (r"%s%s$" % (plural[0].upper(), caseinsensitive(plural[1:])), plural[0].upper() + plural[1:]))
        PLURALS.insert(0, (r"%s%s$" % (plural[0].lower(), caseinsensitive(plural[1:])), plural[0].lower() + plural[1:]))
        SINGULARS.insert(0, (r"%s%s$" % (plural[0].upper(), caseinsensitive(plural[1:])), singular[0].upper() + singular[1:]))
        SINGULARS.insert(0, (r"%s%s$" % (plural[0].lower(), caseinsensitive(plural[1:])), singular[0].lower() + singular[1:]))


def abort(command, description, stack=False):
    """
    @type command: str, None
    @type description: str
    @type stack: bool
    @return: None
    """
    if command is None:
        command = "?"

    linno = get_line_number()
    command = "\033[31m" + "abort:" + str(linno) + ":" + str(command).strip() + "\033[0m"

    console_cmd_desc(str(command).strip(), str(description), "red", enteraftercmd=False)

    if stack is True:
        console(str(chr(9889)), print_stack=True)

    raise SystemExit(1)


def bar(it, label='', width=32, hide=None, empty_char=' ', filled_char=None, expected_size=None, every=1):
    """
    Progress iterator. Wrap your iterables with it.
    @type it: iterator
    @type label: str
    @type width: int
    @type hide: str, None
    @type empty_char: float
    @type filled_char: float
    @type expected_size: int, None
    @type every: int
    @return: None
    """
    if filled_char is None:
        filled_char_tmp = b'\xe2\x96\x88'.decode()
        filled_char = "\033[0;37m" + filled_char_tmp + "\033[0m"

    count = len(it) if expected_size is None else expected_size
    with Bar(label=label, width=width, hide=hide, expected_size=count, every=every, empty_char=empty_char, filled_char=filled_char) as mybar:
        for i, item in enumerate(it):
            if isinstance(item, tuple) and len(item) == 2:
                mybar.label = item[0]
                item = item[1]
            yield item
            mybar.show(i)


def camel_case(mystring, uppercase_first_letter=True, remove_spaces=True):
    """
    @type mystring: str
    @type uppercase_first_letter: bool
    @type remove_spaces: bool
    @return: None
    """
    if remove_spaces is True:
        ns = ""

        for s in mystring.split():
            ns += re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), s)

        mystring = ns

    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), mystring)
    else:
        return mystring[0].lower() + camelize(mystring)[1:]


def camelize(mystring, uppercase_first_letter=True):
    """
    @type mystring: str
    @type uppercase_first_letter: bool
    @return: None
    """
    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), mystring)
    else:
        return mystring[0].lower() + camelize(mystring)[1:]


def check_for_positional_argument(kwargs, name, default=False):
    """
    @type kwargs: dict
    @type name: str
    @type default: bool, int, str
    @return: bool, int
    """
    if name in kwargs:
        if str(kwargs[name]) == "True":
            return True
        elif str(kwargs[name]) == "False":
            return False
        else:
            return kwargs[name]

    return default


def check_for_positional_arguments(kwargs, namelist):
    """
    @type kwargs: dict
    @type namelist: list
    @return: None
    """
    for name in namelist:
        if name in kwargs:
            return check_for_positional_argument(kwargs, name)

    return False


def class_with_address(cls):
    """
    @type cls: str
    @return: None
    """
    return str(cls.__class__).replace(">", "").replace("class ", "").replace("'", "") + " object at 0x%x>" % id(cls)


def class_without_address(cls):
    """
    @type cls: str
    @return: None
    """
    return str(cls.__class__).replace(">", "").replace("class ", "").replace("'", "") + " object>"


def clear_screen(ctrlkey=False):
    """
    @type ctrlkey: bool
    @return: None
    """
    try:
        if sys.stderr.isatty() and ctrlkey is True:
            sys.stderr.write('\x1Bc')
            sys.stderr.flush()
        else:
            os.system("clear")
    except BaseException:
        pass


def colorize_path(p):
    """
    @type p: str
    @return: None
    """
    orgp = p

    if os.getcwd() not in p:
        p = os.path.join(os.getcwd(), p)

    if os.path.isdir(p):
        p = "\033[34m" + orgp + "\033[0m"
    else:
        p = "\033[93m" + orgp + "\033[0m"

    return p

me = os.popen("whoami").read()


def colorize_for_print(v):
    """
    @type v: str
    @return: None
    """
    spacesbefore = len(v) - len(v.lstrip())
    sl = []
    v = v.rstrip()
    spacecnt = 0

    if header_trigger(v):
        retval = "\033[97m" + v.lower() + "\033[0m"
    else:
        first = True
        scanning = False
        scanbuff = ""

        for v in v.split(" "):
            addenter = v.rstrip(" ").endswith("\n")
            v = remove_color(v.rstrip())

            if len(v) > 0:
                # noinspection PyPep8,PyPep8
                if scanning is True:
                    scanbuff += " " + v

                    if v.endswith("}"):
                        scanning = False
                        sl.append(scanbuff)

                elif "charset" in v:
                    sl.append("\033[35m" + v + "\033[0m")
                elif v.startswith("http") and not v.startswith("http_") or v.startswith("www."):
                    addhttp = False

                    if v.startswith("www."):
                        addhttp = True
                        v = "http://" + v

                    url = urlparse(v)
                    strex = lambda val: val is not "" and val is not None
                    validurl = strex(url.scheme) and strex(url.netloc)

                    if validurl:
                        if addhttp:
                            v = v.lstrip("http://")

                        sl.append("\033[91m" + v + "\033[0m")
                    else:
                        reason = ", "

                        if not strex(url.scheme):
                            reason += "no schema "

                        if not strex(url.netloc):
                            reason += "no location"

                        sl.append("\033[31m" + v + reason + "\033[0m")

                elif v.startswith("{"):
                    scanning = True
                    scanbuff = v
                elif "=" in v and not "====" in v and not "|=" in v:
                    for v in v.split(","):
                        vs = v.split("=")
                        v2 = "\033[35m" + vs[0] + "\033[0m\033[36m=\033[34m"
                        for i in vs[1:]:
                            v2 += str(i) + ","

                        sl.append(v2.strip(","))

                elif "/" in v and v.count("/") == 1 and not v.startswith("/") and not v.count(".") > 2:
                    sl.append("\033[95m" + v + "\033[0m")
                elif v.strip() == "Pod":
                    sl.append("\033[91m" + v + "\033[0m")
                elif v.strip().startswith("-") and not v.endswith("+") and not "---" in v:
                    if len(v) > 4:
                        v = v.replace("--", "\n\t--")

                    sl.append("\033[34m" + v + "\033[0m")
                elif v.strip() in list_add_capitalize(["up", "true", "active", "running", "ready", "running", "true"]):
                    sl.append("\033[32m" + snake_case(v) + "\033[0m")
                elif v.strip().lower() in ["activating"]:
                    sl.append("\033[91m" + v + "\033[0m")
                elif " am" in v or "pm" in v:
                    sl.append("\033[33m" + v + "\033[0m")
                elif v.count(":") == 5 and len(v.strip()) == 17:
                    sl.append("\033[37m" + v + "\033[0m")
                elif v.strip().lower() in ["exited", "loaded"]:
                    sl.append("\033[33m" + v + "\033[0m")
                elif v.strip() in list_add_capitalize(["down", "dead", "inactive", "killing", "false", "failed", "NotReady"]):
                    sl.append("\033[31m" + snake_case(v) + "\033[0m")
                elif ("core" in v or "node" in v) and ".nl" in v:
                    sl.append("\033[91m" + v + "\033[0m")
                elif v == "<none>":
                    sl.append("\033[37m" + v + "\033[0m")
                elif "." in v and v.count(".") % 3 == 0:
                    vip = v.replace(".", "").replace(":", "").replace("(", "").replace(")", "").replace("/", "").rstrip()

                    if vip.isdigit():
                        sl.append("\033[33m" + v + "\033[0m")
                    else:
                        sl.append(v)

                elif v.count(":") == 1 and v.strip().replace(":", "").isdigit():
                    sl.append("\033[33m" + v + "\033[0m")
                elif v.isnumeric() or v.strip().replace(".", "").replace("'", "").replace('|', "").replace('"', "").isdigit():
                    if "." in v:
                        v = str(float(v))
                        sl.append("\033[36m" + v + "\033[0m")
                    else:
                        if "|" in v:
                            sl.append("|\033[34m" + v.split("|")[1] + "\033[0m")
                        else:
                            sl.append("\033[34m" + v + "\033[0m")

                elif "/" in v and os.path.exists(v):
                    sl.append("\033[32m" + v.rstrip() + "\033[0m")
                elif me in v.strip():
                    sl.append("\033[37m" + v + "\033[0m")
                elif len(v) == 64:
                    sl.append("\033[90m" + v[:8] + "\033[0m")
                elif "----" in v or "====" in v or v.strip().startswith("|"):
                    sl.append("\033[90m" + v + "\033[0m")
                else:
                    if first:
                        sl.append("\033[93m" + v + "\033[0m")
                    else:
                        sl.append("\033[93m" + v + "\033[0m")
            else:
                sl.append("\033[93m" + v + "\033[0m")

            if v == "":
                spacecnt += 1

            if spacecnt == 2:
                first = False
                spacecnt = 0

            if addenter:
                sl.append("\n")

        retval = " ".join([x for x in sl])

    retval = retval.replace("\t", " " * 4)
    retval = spacesbefore * " " + retval.rstrip()
    return retval


def colorize_for_print2(v):
    """
    @type v: str
    @return: None
    """
    spacesbefore = len(v) - len(v.lstrip())
    sl = []
    v = v.rstrip()
    maxspace = 0
    spacecnt = 0

    if header_trigger(v):
        retval = "\033[97m" + v.lower() + "\033[0m"
    else:
        first = True
        scanning = False
        scanbuff = ""
        spacecnt2 = 0

        for v2 in v.split(" "):
            if v2.strip() == '':
                spacecnt2 += 1
            else:
                if maxspace < spacecnt2:
                    maxspace = spacecnt2

                spacecnt2 = 0

        for v in v.split(" "):
            addenter = v.rstrip(" ").endswith("\n")
            v = remove_color(v.rstrip())

            if len(v) > 0:
                # noinspection PyPep8,PyPep8
                if scanning is True:
                    scanbuff += " " + v

                    if v.endswith("}"):
                        scanning = False
                        sl.append(scanbuff)

                elif "charset" in v:
                    sl.append("\033[35m" + v + "\033[0m")
                elif v.startswith("http") and not v.startswith("http_") or v.startswith("www."):
                    addhttp = False

                    if v.startswith("www."):
                        addhttp = True
                        v = "http://" + v

                    url = urlparse(v)
                    strex = lambda val: val is not "" and val is not None
                    validurl = strex(url.scheme) and strex(url.netloc)

                    if validurl:
                        if addhttp:
                            v = v.lstrip("http://")

                        sl.append("\033[91m" + v + "\033[0m")
                    else:
                        reason = ", "

                        if not strex(url.scheme):
                            reason += "no schema "

                        if not strex(url.netloc):
                            reason += "no location"

                        sl.append("\033[31m" + v + reason + "\033[0m")

                elif v.startswith("{"):
                    scanning = True
                    scanbuff = v
                elif "=" in v and not "====" in v and not "|=" in v:
                    for v in v.split(","):
                        vs = v.split("=")
                        v2 = "\033[35m" + vs[0] + "\033[0m\033[36m=\033[34m"
                        for i in vs[1:]:
                            v2 += str(i) + ","

                        sl.append(v2.strip(","))

                elif "/" in v and v.count("/") == 1 and not v.startswith("/") and not v.count(".") > 2:
                    sl.append("\033[95m" + v + "\033[0m")
                elif v.strip() == "Pod":
                    sl.append("\033[91m" + v + "\033[0m")
                elif v.strip().startswith("-") and not v.endswith("+") and not "---" in v:
                    if len(v) > 4:
                        v = v.replace("--", "\n\t--")

                    sl.append("\033[34m" + v + "\033[0m")
                elif v.strip() in list_add_capitalize(["up", "true", "active", "running", "ready", "running", "true"]):
                    sl.append("\033[32m" + snake_case(v) + "\033[0m")
                elif v.strip().lower() in ["activating"]:
                    sl.append("\033[91m" + v + "\033[0m")
                elif " am" in v or "pm" in v:
                    sl.append("\033[33m" + v + "\033[0m")
                elif v.count(":") == 5 and len(v.strip()) == 17:
                    sl.append("\033[37m" + v + "\033[0m")
                elif v.strip().lower() in ["exited", "loaded"]:
                    sl.append("\033[33m" + v + "\033[0m")
                elif v.strip() in list_add_capitalize(["down", "dead", "inactive", "killing", "false", "failed", "NotReady"]):
                    sl.append("\033[31m" + snake_case(v) + "\033[0m")
                elif ("core" in v or "node" in v) and ".nl" in v:
                    sl.append("\033[91m" + v + "\033[0m")
                elif v == "<none>":
                    sl.append("\033[37m" + v + "\033[0m")
                elif "." in v and v.count(".") % 3 == 0:
                    vip = v.replace(".", "").replace(":", "").replace("(", "").replace(")", "").replace("/", "").rstrip()

                    if vip.isdigit():
                        sl.append("\033[33m" + v + "\033[0m")
                    else:
                        sl.append(v)

                elif v.count(":") == 1 and v.strip().replace(":", "").isdigit():
                    sl.append("\033[33m" + v + "\033[0m")
                elif v.isnumeric() or v.strip().replace(".", "").replace("'", "").replace('|', "").replace('"', "").isdigit():
                    if "." in v:
                        v = str(float(v))
                        sl.append("\033[36m" + v + "\033[0m")
                    else:
                        if "|" in v:
                            sl.append("|\033[34m" + v.split("|")[1] + "\033[0m")
                        else:
                            sl.append("\033[34m" + v + "\033[0m")

                elif "/" in v and os.path.exists(v):
                    sl.append("\033[32m" + v.rstrip() + "\033[0m")
                elif me in v.strip():
                    sl.append("\033[37m" + v + "\033[0m")
                elif len(v) == 64:
                    sl.append("\033[90m" + v[:8] + "\033[0m")
                elif "----" in v or "====" in v or v.strip().startswith("|"):
                    sl.append("\033[90m" + v + "\033[0m")
                else:
                    if first:
                        sl.append("\033[93m" + v + "\033[0m")
                    else:
                        sl.append("\033[93m" + v + "\033[0m")
            else:
                if v.strip():
                    sl.append("\033[93m" + v + "\033[0m")

            if v == "":
                spacecnt += 1

            if spacecnt == 2:
                first = False
                spacecnt = 0

            if addenter:
                sl.append("\n")

        retval = " ".join([x for x in sl])

    retval = retval.replace("\t", " " * 4)
    retval = spacesbefore * " " + retval.rstrip()

    # print(retval, maxspace, len(retval))
    return retval.rstrip()


def require_python3():
    """
    require_python3
    """
    if (sys.version_info < (3, 0)):
        print("python2 not supported")
        exit(1)


def console(*args, **kwargs):
    """
    @param args:
    @type args:
    @param kwargs
    @type kwargs:
    """
    if len(args) == 0:
        if "msg" in kwargs:
            args = tuple([kwargs["msg"]])
        else:
            print()
            return

    sysglob = SystemGlobals()
    debug = False

    if debug:
        s = ""

        for i in args:
            s += str(i) + " "

        print(s)
        return
    global g_start_time
    runtime = "%0.2f" % (1000 * float(time.time() - g_start_time))
    arglist = list(args)
    once = False
    colors = get_colors()

    if "msg" in kwargs:
        arglist = [kwargs["msg"]]

    prefix = check_for_positional_argument(kwargs, "prefix", default=None)
    stackpointer = check_for_positional_argument(kwargs, "stackpointer", default=0)
    line_num_only = check_for_positional_argument(kwargs, "line_num_only", default=3)
    print_stack = check_for_positional_argument(kwargs, "print_stack")
    plainprint = check_for_positional_arguments(kwargs, ["plaintext", "plain_text", "plainprint", "plain_print"])
    return_string = check_for_positional_arguments(kwargs, ["ret_str", "retval", "ret_val"])
    newline = check_for_positional_argument(kwargs, "newline", default=True)
    fileref = check_for_positional_argument(kwargs, "fileref", default=False)
    indent = ""

    if prefix is not None:
        line_num_only = -1

    if "indent" in kwargs:
        if plainprint is False:
            raise AssertionError("console: indent only works for plainprint")

        indent = str(kwargs["indent"])

    if "stack" in kwargs:
        line_num_only += kwargs["stack"]

    toggle = True

    if "color" in kwargs:
        color = kwargs["color"]
    else:
        toggle = False
        color = "grey"

    if color not in colors:
        toggle = False
        color = "default"

    if plainprint is True:
        txt = ""

        for arg in arglist:
            txt, subs = get_value_as_text(colors, 22, return_string, arg, txt, True)

            if toggle:
                txt += colors[color] + subs + "\033[0m"
            else:
                subcolor = "default"

                if color == "red":
                    subcolor = "darkyellow"
                elif color == "grey":
                    subcolor = "black"
                elif color == "black":
                    subcolor = "grey"

                txt += colors[subcolor] + subs + "\033[0m"

            toggle = not toggle
            txt += " "

        txt = remove_extra_indentation(txt)

        if "@@@" not in txt:
            txt = txt.replace("  ", " ")

        if return_string is True:
            return indent + txt
        else:
            sys.stdout.write(indent + colors[color] + txt + "\033[0m")

        if newline is True:
            sys.stdout.write("\n")
        else:
            sys.stdout.write(" ")

        return

    if "donotuseredis" in kwargs:
        donotuseredis = kwargs["donotuseredis"]
    else:
        donotuseredis = True

    if color not in colors:
        console(color, "color not available", source_code_link(1), color='red')
        color = "default"

    if prefix is None:
        prefix = str(runtime)

    if return_string is False:
        dbs = colors['yellow'] + str(prefix) + colors['yellow']
    else:
        dbs = str(prefix)

    source_code_link_msg = None
    columncounter = 0

    if not source_code_link_msg:
        if stackpointer == 0:
            strce = stack_trace(line_num_only=line_num_only).strip()

            if "__init__.py" in strce:
                strce = stack_trace(line_num_only=line_num_only, extralevel=True).strip().replace(os.getcwd(), "")

            source_code_link_msg = strce
        else:
            source_code_link_msg = ""

            for i in range(0, stackpointer + 1):
                scm = str(stack_trace(line_num_only=line_num_only + i)).strip()
                if scm != "?":
                    source_code_link_msg += "\n\t"
                    source_code_link_msg += scm

            source_code_link_msg += "\n\t"

    if not print_stack and fileref is True:
        if line_num_only >= 0:
            if return_string is False:
                subs = " | " + colors[color] + source_code_link_msg + colors[color]
                columncounter, subs = size_columns(columncounter, sysglob.g_width_console_columns, subs, donotuseredis)
                dbs += subs
            else:
                subs = " | " + source_code_link_msg
                dbs += subs

    for s in arglist:
        if toggle:
            dbs += colors[color]
        else:
            dbs += colors['default']

        if s is None:
            s = "None"
        try:
            if str(s) == "":
                s = ""
            else:
                stripecolor = "grey"
                if color == "red":
                    stripecolor = color

                dbs += colors[stripecolor] + " | " + colors['default']
        except BaseException as ex:
            print(colors["red"], ex, colors["default"])

        if toggle:
            dbs += colors[color]
        else:
            dbs += colors['default']

        toggle = not toggle
        indent = 19
        dbs, subs = get_value_as_text(colors, indent, return_string, s, dbs)
        columncounter, subs = size_columns(columncounter, sysglob.g_width_console_columns, subs, donotuseredis)
        dbs += subs

    dbs += "\033[0m"

    if return_string is True:
        return dbs.strip()

    linecnt = 0

    if print_stack:
        newline = False
        trace = stack_trace(ret_list=True)
        toggle = True
        stackline = ""
        dbs += colors["yellow"]
        dbs += "\n"
        lastitem = ""

        for item in trace:
            stacks = ""

            if not toggle:
                if lastitem != "":
                    stacks += " " * len(runtime)

            if toggle:
                stackline = item.strip().split(", in")[0]
            else:
                if running_in_debugger(include_tests=True):
                    if lastitem != "":
                        stacks += " | " + stackline + colors["grey"] + " -> " + lastitem + colors["default"] + "\n"

                    lastitem = item.strip()
                else:
                    if lastitem != "":
                        stacks += colors["grey"] + " | " + format_source_code_line_console(stackline) + colors["black"] + " -> " + lastitem + colors["default"] + "\n"

                    lastitem = item.strip()

            toggle = not toggle
            linecnt += 1

            if linecnt > line_num_only + 4:
                dbs += stacks

    dbs += colors['default']

    if newline:
        dbs += "\n"
    else:
        dbs = dbs.strip()

    if "once" in kwargs:
        once = kwargs["once"]

    if once:
        dbs_no_time = dbs[dbs.find("|"):]

        if dbs_no_time in sysglob.g_console_printed:
            return
        else:
            sysglob.g_console_printed.add(dbs_no_time)

            if len(sysglob.g_console_printed) > 100:
                sysglob.g_console_printed.clear()

    if not sys.stdout.isatty():
        dbs = remove_color(dbs)

    sys.stderr.write(dbs)
    sys.stderr.flush()


def console_cmd_desc(command, description, color, enteraftercmd=False):
    """
    @type command: str
    @type description: str
    @type color: str
    @type enteraftercmd: bool
    @return: None
    """
    linenr = get_line_number(5)
    cmdstr = command + ":"

    if color == "red":
        color = "darkyellow"
        subcolor = "red"
    else:
        subcolor = color
        color = "blue"
    try:
        cmdstr = str(cmdstr).replace(str(os.getcwd()), ".")
        description = str(description).replace(os.getcwd(), ".")
    except FileNotFoundError:
        cmdstr += "<file not found>"
        description += "<file not found>"

    console(cmdstr, color=color, plaintext=not get_debugmode(), line_num_only=4, newline=enteraftercmd)

    if "\n" not in description:
        console(description, color=subcolor, plaintext=not get_debugmode(), line_num_only=4, newline=color != "red")
    else:
        first = True

        for s in description.split("\n"):
            if first is True:
                console(s, color=subcolor, plaintext=not get_debugmode(), line_num_only=4)
            else:
                spaces = len(remove_escapecodes(cmdstr))
                sys.stdout.write(" " * (spaces + 1))
                console(s.strip(), color=subcolor, plaintext=not get_debugmode(), line_num_only=4)

            first = False

    if color == "red":
        console(linenr, plaintext=True, color="black", newline=True)


def console_error(stacktracemsg, exceptiontoraise, errorplaintxt=None, line_num_only=6):
    """
    @type stacktracemsg: str
    @type exceptiontoraise: BaseException
    @type errorplaintxt: str, None
    @type line_num_only: int
    @return: None
    """
    if errorplaintxt:
        console(errorplaintxt, color="red", plainprint=True)

    console_warning(stacktracemsg, print_stack=True, color="darkyellow", line_num_only=line_num_only)

    raise exceptiontoraise


def console_error_exit(*args, **kwargs):
    """
    @type args: tuple
    @type kwargs: dict
    @return: None
    """
    kwargs["exit"] = True
    kwargs["print_stack"] = True
    return SystemExit(console_warning(*args, **kwargs))


def console_exception(ex):
    """
    @type ex: object, Exception
    """
    exstr = handle_ex(ex, False, True)
    console_saved_exception(exstr)


def console_saved_exception(excstr, verbose=True):
    """
    @type excstr: str
    @type verbose: bool
    """
    major_info = []
    cnt = 0

    for ei in excstr.split("\n"):
        if exist(ei):
            cargs = ei.split(" -> ")

            if cnt < 3:
                major_info.append(cargs[0])

                if len(cargs) > 1:
                    major_info.append(cargs[1])

                cnt += 1

            if verbose:
                console(*cargs, warning=True, dolstrip=False, line_num_only=4)

    return major_info


def console_warning(*args, **kwargs):
    """
    @param args
    @type args:
    @param kwargs
    @type kwargs:
    """
    retval = check_for_positional_arguments(kwargs, ["ret_str", "retval", "ret_val"])

    if "color" in kwargs:
        color = kwargs["color"]
    else:
        color = "red"

    if "print_stack" in kwargs:
        print_stack = kwargs["print_stack"]
    else:
        print_stack = True

    if "line_num_only" in kwargs:
        line_num_only = kwargs["line_num_only"]
    else:
        line_num_only = 4

    if "once" in kwargs:
        once = kwargs["once"]
    else:
        once = False

    if running_in_debugger(True):
        args = list(args)
        args.insert(0, "==")
        args.append(source_code_link(line_num_only - 2))
        args.append("==")

    bexit = check_for_positional_argument(kwargs, "exit", default=False)
    retval = console(*args, print_stack=print_stack, color=color, line_num_only=line_num_only, once=once, retval=retval)

    if bexit is True:
        retval = console(*args, print_stack=print_stack, color=color, line_num_only=line_num_only, once=once, retval=True, plaintext=True)

        raise SystemExit(retval)

    return retval


def consoledict(mydict, members=None, printval=True, indent=0, retval=False, plainprint=False):
    """
    @type mydict: dict
    @type members: str, None
    @type retval: bool
    @type indent: int
    @type printval: bool
    @type plainprint: bool
    @return: None
    """
    dbs = ""

    if printval is True:
        dbs = "\033[32m" + log_date_time_string() + " | "
        dbs += stack_trace(line_num_only=3).strip()
        dbs += " - consoledict:\033[0m\n"

    if plainprint is True:
        dbs = log_date_time_string() + " | "
        dbs += stack_trace(line_num_only=3).strip()
        dbs += " - consoledict:\n"

    if indent > 0:
        dbs = ""

    if isinstance(mydict, dict):
        if members is None:
            members = list(mydict.keys())

        members.sort()

        for i in members:
            dbs += "    " * indent

            if isinstance(mydict[i], dict):
                newindent = indent + 1

                if plainprint is False:
                    dbs += "\033[35m" + str(i) + ":\n" + "\033[0m"
                else:
                    dbs += str(i) + ":\n"

                dbs += consoledict(mydict[i], printval=printval, indent=newindent, retval=True, plainprint=plainprint)
            else:
                if plainprint is False:
                    dbs += "\033[35m" + str(i) + ": " + "\033[0m"
                    dbs += colorize_for_print(str(mydict[i])) + "\n"
                else:
                    dbs += str(i) + ": " + str(mydict[i]) + "\n"
    else:
        dbs += "not dict: " + str(mydict) + "\n"

    if printval is True and retval is False:
        sys.stderr.write(dbs)

    if indent == 0:
        dbs = dbs.strip()

    return dbs


def consoletasks(*args, **kwargs):
    """
    @type args: tuple
    @type kwargs: dict
    @return:
    @raise:
    """
    line_num_only = 3
    if "line_num_only" in kwargs:
        line_num_only = kwargs["line_num_only"]

    kwargs["line_num_only"] = line_num_only
    kwargs["newline"] = False

    console(*args, **kwargs)


def coolname():
    """
    coolname
    """
    names = """
    Aldous
    Ara
    Azarias
    Balthazar
    Barnaby
    Bastien
    Berlin
    Birch
    Bridge
    Cabe
    Cabot
    Calixto
    Callaghan
    Calloway
    Carlson
    Christo
    Chuck
    Clovis
    Columbus
    Connelly
    Costello
    Cyprian
    Dermot
    Detroit
    Drexel
    Driver
    Fergus
    Finbar
    Finch
    Fitzpatrick
    Gardner
    Garth
    Griffith
    Grover
    Hanan
    Harrington
    Hawthorne
    Heron
    Horatio
    Huckleberry
    Humphrey
    Hunt
    Jupiter
    Keene
    Keir
    Kelso
    Kermit
    Kipling
    Kristof
    Lambert
    Lancelot
    Lanier
    Laurent
    Leib
    Llewellyn
    Loch
    Mackson
    Mcgregor
    Mcguire
    Mercury
    Morocco
    Moss
    Nicasio
    Oak
    Octavion
    Ogden
    Oracio
    Osborn
    Osias
    Osric
    Pacer
    Park
    Phelan
    Pilot
    Primo
    Quint
    Racer
    Rafferty
    Ralston
    Raoul
    Redmond
    Reynolds
    Romulus
    Saber
    Sadler
    Satchel
    Sender
    Severus
    Spence
    best
    Thurman
    Topher
    Wagner
    Waldo
    Wally
    Webster
    Witt
    Yale
    Zed
    Zoran
    """
    lastnames = """
    Abernathy
    Abner
    Aldaine
    Amor
    Amherst
    Armstrong
    Angeles
    Annesley
    Archer
    Ash
    Bancroft
    Bandini
    Banner
    Barringer
    Blackwood
    Blood
    Bloom
    Boulder
    Cadwell
    Cage
    Carmichael
    Chase
    Cobain
    Cohen
    Colburn
    Colt
    Crabtree
    Crassus
    Creed
    Crew
    Cullen
    Dalton
    Danger
    Davenport
    Dillinger
    Duke
    East
    Fall
    Fawn
    Freeze
    Gamble
    Granger
    Gryffon
    Gunn
    Halifax
    Havoc
    Hilton
    Holly
    Hope
    Hunter
    Ice
    Iris
    Iver
    Ivy
    Jarvis
    Joy
    Kelly
    Kennicot
    King
    Knight
    Lily
    Love
    Mayhem
    Merry
    Noble
    North
    Paris
    Pendleton
    Pevensie
    Phoenix
    Poe
    Potter
    Power
    Quake
    Radcliffe
    Raven
    River
    Rose
    Savage
    Slade
    Slayer
    Star
    Stratton
    Stryker
    Styles
    Tatum
    Tremaine
    Troublefield
    Underwood
    Verbeck
    Violet
    Vow
    Waldgrave
    Walker
    Winter
    Wolf
    York
    Young
    Zedler
    Zimmerman
    """
    names = [x.strip() for x in names.split("\n") if x]
    lastnames = [x.strip() for x in lastnames.split("\n") if x]
    randomnumbername = random.randint(0, len(names) - 1)
    randomnumberlastname = random.randint(0, len(names) - 1)
    print(names[randomnumbername], lastnames[randomnumberlastname])


def dasherize(word):
    """
    @type word: str
    @return: None
    """
    return word.replace('_', '-')


def deprecated_remove_extra_indentation(doc, stop_looking_when_encountered=None, padding=0, frontspacer=" "):
    """
    @type doc: str
    @type stop_looking_when_encountered: str, None
    @type padding: int
    @type frontspacer: str
    @return: None
    """
    startspaces = len(doc.lstrip("\n")) - len(doc.lstrip("\n").lstrip(" "))

    if doc is None:
        console_warning("doc is None")
        return doc

    newdoc = ""
    whitespacecount = 0
    keeplookingforindention = True

    for line in doc.split("\n"):
        line = line.rstrip()

        if stop_looking_when_encountered is not None:
            if line.lower().startswith(stop_looking_when_encountered):
                keeplookingforindention = False

        if keeplookingforindention is True:
            if whitespacecount == 0:
                whitespacecount = len(line) - len(line.lstrip())

        line = str(" " * padding) + line[whitespacecount:]
        newdoc += line + "\n"

    newdoc = newdoc.strip()
    newdoc = str(frontspacer * ((startspaces - whitespacecount) + padding)) + newdoc.lstrip()
    return newdoc


def doinput_display_answers(answers, default):
    """
    @type answers: list
    @type default: str
    @return: None
    """
    display_answers = []

    for ans in answers:
        ans = str(ans)

        if ans is default:
            ans = ans.upper()

        display_answers.append(ans)

    display_answers.sort(key=lambda x: str(x).lower().strip())
    return display_answers


def doinput(description="", default=None, theanswers=None, force=False, returnnum=False):
    """
    @type description: str
    @type default: str, None
    @type theanswers: list, None
    @type force: bool
    @type returnnum: bool
    @return: None
    """
    answers = copy.deepcopy(theanswers)

    if force is True:
        if default is None:
            raise AssertionError("no default set")

        return default

    answer = ""
    ianswer = -1
    quitanswers = ["quit", "q", "Quit", "Q", "QUIT"]

    if default is not None:
        description += "\033[96m (default: \033[33m" + str(default) + "\033[96m" + ", quit: q)?"

    if answers is not None:
        display_answers = doinput_display_answers(answers, default)

        # answers.extend(quitanswers)
        console(description, color="darkcyan", plaintext=not get_debugmode(), line_num_only=4, newline=True)
        if len(description) == 0:
            console("options:", color="grey", plaintext=not get_debugmode(), line_num_only=4, newline=True)

        for cnt, pa in enumerate(display_answers):
            console(pa, indent=" " + str(cnt + 1) + ". ", color="grey", plaintext=not get_debugmode(), line_num_only=4, newline=True)

        while True:
            answer = get_input_answer(default)

            if answer in quitanswers:
                raise SystemExit()

            if answer not in answers:
                try:
                    ianswer = int(answer)
                    ianswer = ianswer - 1
                    answer = display_answers[ianswer]
                except ValueError:
                    pass

                except IndexError:
                    pass

            if answer not in answers:
                console("$: invalid -> ", answer, color="red", plaintext=not get_debugmode(), line_num_only=4)
                for cnt, pa in enumerate(display_answers):
                    console(pa, indent=" " + str(cnt + 1) + ". ", color="grey", plaintext=not get_debugmode(), line_num_only=4, newline=True)
            else:
                break
    else:
        console(description, color="darkcyan", plaintext=not get_debugmode(), line_num_only=4, newline=True)
        answer = get_input_answer(default)
        try:
            answer = int(answer)
            ianswer = answer - 1
        except ValueError:
            pass

    if answer in quitanswers:
        # print("SystemExit(doinput quit)", quitanswers, answer)
        raise SystemExit()

    console("ok: " + str(answer), color="green", plaintext=not get_debugmode(), line_num_only=4, newline=True)

    if returnnum:
        return ianswer, display_answers

    return answer, display_answers


def dot_print(cnt=0, total=0, modint=10):
    """
    @type cnt: int
    @type total: int
    @type modint: int
    @return: None
    """
    sys.stdout.write(".")

    if cnt > 0 and cnt % modint == 0:
        sys.stdout.write("\n" + str(cnt) + "/" + str(total) + "\n")

    sys.stdout.flush()


def dot_print_end():
    """
    dot_print_end
    """
    sys.stdout.write("\n")
    sys.stdout.flush()


def exist(data):
    """
    @type data: str, int, float, None, dict, list
    """
    if data is None:
        return False

    if isinstance(data, bool) or isinstance(data, int) or isinstance(data, float):
        return data
    elif isinstance(data, list) or isinstance(data, set) or isinstance(data, tuple):
        if data:
            return True
        else:
            return False

    data = str(data).strip()

    if not data:
        return False
    elif str(data) == "":
        return False
    elif len(str(data)) == 0:
        return False
    elif str(data) == "False":
        return False
    elif str(data) == "false":
        return False
    elif str(data) == "undefined":
        return False
    elif str(data) == "null":
        return False
    elif str(data) == "none":
        return False
    elif str(data) == "None":
        return False

    return True


def forceascii(unicrap):
    """
    @type unicrap: str
    @return: None
    """
    xlate = {0xc0: 'A', 0xc1: 'A', 0xc2: 'A', 0xc3: 'A', 0xc4: 'A', 0xc5: 'A',
             0xc6: 'Ae', 0xc7: 'C',
             0xc8: 'E', 0xc9: 'E', 0xca: 'E', 0xcb: 'E',
             0xcc: 'ival', 0xcd: 'ival', 0xce: 'ival', 0xcf: 'ival',
             0xd0: 'Th', 0xd1: 'N',
             0xd2: 'O', 0xd3: 'O', 0xd4: 'O', 0xd5: 'O', 0xd6: 'O', 0xd8: 'O',
             0xd9: 'U', 0xda: 'U', 0xdb: 'U', 0xdc: 'U',
             0xdd: 'Y', 0xde: 'th', 0xdf: 'ss',
             0xe0: 'a', 0xe1: 'a', 0xe2: 'a', 0xe3: 'a', 0xe4: 'a', 0xe5: 'a',
             0xe6: 'ae', 0xe7: 'c',
             0xe8: 'e', 0xe9: 'e', 0xea: 'e', 0xeb: 'e',
             0xec: 'ival', 0xed: 'ival', 0xee: 'ival', 0xef: 'ival',
             0xf0: 'th', 0xf1: 'n',
             0xf2: 'o', 0xf3: 'o', 0xf4: 'o', 0xf5: 'o', 0xf6: 'o', 0xf8: 'o',
             0xf9: 'u', 0xfa: 'u', 0xfb: 'u', 0xfc: 'u',
             0xfd: 'y', 0xfe: 'th', 0xff: 'y',
             0xa1: '!', 0xa2: '{cent}', 0xa3: '{pound}', 0xa4: '{currency}',
             0xa5: '{yen}', 0xa6: '|', 0xa7: '{section}', 0xa8: '{umlaut}',
             0xa9: '{C}', 0xaa: '{^a}', 0xab: '<<', 0xac: '{not}',
             0xad: '-', 0xae: '{R}', 0xaf: '_', 0xb0: '{degrees}',
             0xb1: '{+/-}', 0xb2: '{^2}', 0xb3: '{^3}', 0xb4: "'",
             0xb5: '{micro}', 0xb6: '{paragraph}', 0xb7: '*', 0xb8: '{cedilla}',
             0xb9: '{^1}', 0xba: '{^o}', 0xbb: '>>',
             0xbc: '{1/4}', 0xbd: '{1/2}', 0xbe: '{3/4}', 0xbf: '?',
             0xd7: '*', 0xf7: '/'}

    result = ''

    for ival in unicrap:
        if ord(ival) in xlate:
            result += xlate[ord(ival)]
        elif ord(ival) >= 0x80:
            pass
        else:
            result += str(ival)

    return result


def format_source_code_line_console(path):
    """
    @type path: str, unicode
    @return: @raise
    """
    paths = path.split(",")

    if len(paths) == 2:
        # dpath = os.path.basename(os.path.dirname(paths[0]))
        fpath = os.path.basename(paths[0]).strip().replace('"', "")

        if "__init__" in fpath:
            fpath = os.path.basename(os.path.dirname(paths[0]).strip().replace('"', "")) + "/" + fpath

        location = paths[1].replace(' line ', ":").strip("/")
        return fpath + location.replace(" (", ":").replace(")", "").strip()
    else:
        return path


def fpath_in_stack(fpath):
    """
    @type fpath: str
    """
    stack = stack_as_string()
    stack = stack.split("\n")
    stack.reverse()

    for i in stack:
        if i.strip().startswith("File"):
            if fpath.lower() in i.lower():
                if "greenlet.py" in fpath:
                    console("fpath_in_stack", fpath, source_code_link(2))

                # else:
                #    console("fpath_in_stack", fpath, source_code_link(1))
                return True

    return False


def func_info(func_object):
    """
    @type func_object: function
    """
    if func_object is None:
        raise TypeError("func_info needs function")

    fname = func_object.__code__.co_filename
    linenr = func_object.__code__.co_firstlineno
    funcname = func_object.__code__.co_name
    return fname, funcname, linenr


def get_alphabet():
    """
    get_alphabetget_safe_alphabet
    """
    return tuple(['!', ' ', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', ' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                  'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])


def get_alphabet_lower():
    """
    get_alphabet_lower
    """
    return tuple([' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])


def get_alphabet_lower_numbers():
    """
    get_alphabet_lower_numbers
    """
    return tuple([' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])


def remove_youtube_tag(fpath):
    """
    @type fpath: str
    @return: None
    """
    fpathsplit = os.path.splitext(fpath)
    fpathsplitext = fpathsplit[0].strip()
    fpathsplitextlast = fpathsplit[1]
    splitrev = fpathsplitext.split("-")
    splitrev.reverse()
    taglen = 0
    tag = ""
    nfpath = fpath

    for fpj in splitrev:
        tag = fpj
        taglen = len(fpj)
        break

    if taglen >= 11 and "." in tag:
        for fpk in tag.split("."):
            tag = fpk
            taglen = fpk
            break

    if taglen == 10:
        nfpath = forceascii(fpathsplitext).replace("-" + tag, "").strip("_").strip("-").strip() + fpathsplitextlast
    elif taglen == 11:
        if "-" + tag in fpath:
            nfpath = forceascii(fpathsplitext).replace("-" + tag, "").strip("_").strip("-").strip() + fpathsplitextlast

    elif fpathsplitext.endswith("_") or fpathsplitext.endswith("-") or fpathsplitext.endswith(" ") or fpathsplitext.startswith("_") or fpathsplitext.startswith("-") or fpathsplitext.startswith(" "):
        nfpath = forceascii(fpathsplitext).strip("_").strip("-").strip() + fpathsplitextlast

    return nfpath


def get_colors():
    """
    get_colors
    """
    colors = {'red': '\033[31m',
              'darkmagenta': '\033[95m',
              'green': '\033[32m',
              'darkgreen': '\033[32m',
              'yellow': '\033[33m',
              'darkyellow': '\033[33m',
              'blue': '\033[34m',
              'magenta': '\033[35m',
              'cyan': '\033[36m',
              'darkcyan': '\033[96m',
              'white': '\033[97m',
              'black': '\033[90m',
              'purple': '\033[34m',
              'grey': '\033[90m',
              'orange': '\033[91m',
              'default': '\033[0m'}

    return colors


def get_debugmode():
    """
    get_debugmode
    """
    sg = SystemGlobals()
    return sg.g_debug


def get_hostname():
    """
    get_hostname
    """
    return str(socket.gethostname())


def get_input_answer(default):
    """
    @type default: str
    @return: None
    """
    try:
        answer = input("$: ").lower()
    except KeyboardInterrupt:
        answer = "quit"

    answer = get_safe_string(answer.strip())

    if answer is "" and default is not None:
        answer = default
    try:
        answeri = int(answer)

        if str(answeri) == answer:
            answer = answeri
    except ValueError:
        pass

    if isinstance(answer, str):
        try:
            answer = float(answer)
        except ValueError:
            pass

    return answer


def get_line_number(line_num_only=4):
    """
    @type line_num_only: int
    @return: None
    """
    try:
        strce = stack_trace(line_num_only=line_num_only).strip()

        if "__init__.py" in strce:
            strce = stack_trace(line_num_only=line_num_only, extralevel=True).strip().replace(os.getcwd(), "")

        linenr = ":".join([x.split("(")[0].strip().strip(",").strip('"') for x in strce.split("line")]).replace("/__init__.py", "")
        return linenr
    except BaseException as exc:
        print("\033[37m", exc, "\033[0m")


def get_print_yaml(yamlmystring):
    """
    @type yamlmystring: str
    @return: None
    """

    # print({1:yamlmystring})
    s = ""
    currnumdashes = 0
    currnumspaces = 0

    for i in yamlmystring.split("\n"):
        i = i.replace("http:", "http|")
        i = i.replace("https:", "https|")
        numdashes = i.count("-") - i.lstrip("-").count("-")

        if numdashes > currnumdashes:
            s += "\n"

        currnumdashes = numdashes
        numspaces = i.count(" ") - i.lstrip(" ").count(" ")

        if numspaces is 0 and currnumspaces > 0:
            if not s.endswith("\n\n"):
                s += "\n"

        currnumspaces = numspaces
        ls = [x for x in i.split(":") if x]
        cnt = 0

        if len(ls) > 1:
            for ii in ls:
                ii = ii.replace("http|", "http:")
                ii = ii.replace("https|", "https:")

                if cnt == 0:
                    s += "\033[37m" + ii + ":" + "\033[0m"
                else:
                    s += colorize_for_print(ii)

                cnt += 1
        else:
            if i.strip().startswith("---"):
                s += "\033[37m" + i + "\033[0m"
            else:
                s += "\033[37m" + i + "\033[0m"

        s += "\n"

    s = s.replace("items:\x1b[0m\n\n\x1b[95m-", "\nitems:\x1b[0m\n\x1b[95m-")
    return s.strip()


def get_safe_alphabet():
    """
    get_alphabet
    """
    return tuple(['~', ' ', '|', '_', '.', '-', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c',
                  'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])


def get_safe_string(s, extrachars=None):
    """
    @type s: str
    @type extrachars: str, None`
    @return: None
    """
    if extrachars is not None:
        mysafechars = [ord(mch) for mch in SALPHA + extrachars]
    else:
        mysafechars = SAFECHARS

    s = remove_escapecodes(s)
    targetdict = {}

    for mch in SALPHA:
        targetdict[ord(mch)] = ord(mch)

    for mch in s:
        if ord(mch) not in mysafechars:
            targetdict[ord(mch)] = None

    s = s.translate(targetdict)
    return s


def get_value_as_text(colors, indent, return_string, value, dbs, plaintext=False):
    """
    @type colors: dict
    @type indent: int
    @type return_string: bool
    @type value: str
    @type dbs: str
    @type plaintext: bool
    @return: None
    """
    if plaintext is True:
        colors2 = {}

        for k in colors:
            colors2[k] = ""

        colors = colors2

    if isinstance(value, dict):
        value = value.copy()

        # noinspection PyBroadException
        try:
            value = json.dumps(value)
        except Exception:
            try:
                for k in value:
                    value[k] = str(value[k])
                import json
                value = json.dumps(value, indent=1)
            except Exception as e:
                value = str(value)
                value += " | error dumping dict" + str(e) + " | "

        subs = str(value)
    elif isinstance(value, str) or isinstance(value, (int, float, complex)) or isinstance(value, (tuple, list, set)):
        subs = str(value)

        if not sys.stdout.isatty():
            try:
                subs = get_safe_string(subs, "@:-_?/")
            except:
                pass

    elif isinstance(value, BaseException):
        if plaintext is True:
            subs = str(value)
        else:
            subs = handle_ex(value, False, True)
    else:
        if return_string:
            clsaddr = str(class_without_address(value))
        else:
            clsaddr = str(class_with_address(value))
        try:
            if str(clsaddr) == str(value):
                dbs += colors["purple"] + str(value) + colors["default"] + "\n"
            else:
                dbs += colors["grey"] + clsaddr + ": " + colors["purple"] + str(value) + colors["default"] + "\n"
        except TypeError:
            dbs += colors["grey"] + " |" + colors["default"] + "\n"

        leftoffset = remove_color(dbs).find("|") - 1
        subs = " " * (leftoffset - 4)
        colwidthdelta = 0

        if plaintext:
            colwidthdelta = 19
            subs = ""

        sm = get_safe_string(value.__class__.__name__)

        if len(sm) > indent:
            sm = sm[:indent] + ".."

        subheader = colors['orange'] + subs + " | " + sm
        subheader += (37 - len(get_safe_string(str(subheader)))) * " "
        subheader += "type"
        subheader += (68 - len(get_safe_string(str(subheader)))) * " "
        subheader += "value" + colors['default'] + "\n"
        members = set()

        for m in dir(value):
            members.add(m)

        members = sorted(members)
        mycolors = collections.deque(["darkcyan", "yellow"])

        if plaintext is False:
            subs += " " * leftoffset

        numprintable = 0

        for m in members:
            if not m.startswith("__"):
                numprintable += 1

        if numprintable > 0:
            subs += subheader + (leftoffset * " ")
            subs += colors["grey"] + " | " + 90 * "-" + colors['default'] + "\n"

        for m in members:
            if not m.startswith("__"):
                if m.startswith("_"):
                    if not m.lstrip("_").startswith(get_safe_string(value.__class__.__name__)):
                        continue

                if plaintext is False:
                    subs += " " * leftoffset

                subs += colors["grey"] + " | " + colors['default']
                privatevar = False

                if ("_" + value.__class__.__name__) in m:
                    privatevar = True

                sm = str(m).replace("_" + value.__class__.__name__, "")
                mycolor = mycolors.pop()

                if len(sm) > 31:
                    sm = sm[:31] + ".. "

                tempcolor = mycolor

                if privatevar is True:
                    mycolor = "red"

                subs += colors[mycolor] + sm
                mycolor = tempcolor
                mycolors.appendleft(mycolor)

                if privatevar is True:
                    subs += colors['default']
                    subs += colors[mycolor]

                subs += " " * (34 - len(sm))

                if hasattr(value.__class__, m):
                    t = type(getattr(value.__class__, m))
                else:
                    t = type(getattr(value, m))

                sm = repr(t).replace("<class '", "").replace("'>", "")

                # sm += "jfhsjkdfjsdfhdjkshfjksdhfjsdhkfhsdjkhfskdhfdsksdfjkh"
                extraspacereduction = 0

                if len(sm) > 31:
                    sm = sm[:31] + ".."
                    extraspacereduction = len("..")

                subs += sm
                memberval = getattr(value, m)

                if isinstance(memberval, str) or isinstance(memberval, (int, float, complex)) or isinstance(memberval, (tuple, list, set)):
                    subs += (72 - colwidthdelta - extraspacereduction - len(get_safe_string("".join(subs.split("\n")[-1:])))) * " "

                    if plaintext is True:
                        subs += str(memberval)
                    else:
                        subs += colorize_for_print(str(memberval))

                subs += "\n" + colors['default']

    return dbs, subs


def get_vowels_lower():
    """
    get_vowels_lower
    """
    return tuple([' ', 'a', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'])


def handle_ex(exc=None, again=True, give_string=False, extra_info=None, source_code_links=True):
    """
    @type exc: Exception, None
    @type again: bool
    @type give_string: bool
    @type extra_info: str, list
    @type source_code_links: bool
    """
    import sys
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_msg = ""

    if exc:
        if not give_string:
            console("handle_ex", str(exc))

    if not give_string:
        error_msg += "\033[91m\nTaceback:\n"

    items = traceback.extract_tb(exc_traceback)

    # items.reverse()
    leni = 0

    if not give_string:
        error_msg += "\033[91m  " + str(exc_type) + "\n"
        error_msg += "\033[91m  " + str(exc_value) + "\n"

        if extra_info:
            if isinstance(extra_info, list):
                spaces = ""

                for msg in extra_info:
                    spaces += "  "
                    error_msg += "\033[91m" + spaces + str(msg) + "\n"
            else:
                error_msg += "\033[91m" + str(extra_info) + "\n"

        error_msg += "\033[91m\n"
    else:
        error_msg += str(exc_type) + "\n"
        error_msg += str(exc_value) + "\n"
    try:
        linenumsize = 0

        for line in items:
            fnamesplit = str(line[0]).split("/")
            fname = "/".join(fnamesplit[len(fnamesplit) - 2:])
            ls = len(fname + ":" + str(line[1]))

            if ls > linenumsize:
                linenumsize = ls

        items.reverse()

        for line in items:
            leni += 1

            if source_code_links:
                fname_number = '  File "' + line[0] + '", line ' + str(line[1]) + ', in ' + line[2].strip()
            else:
                fnamesplit = str(line[0]).split("/")
                fname = "/".join(fnamesplit[len(fnamesplit) - 2:])
                fname_number = fname + ":" + str(line[1])
                fname_number += (" " * (linenumsize - len(fname_number)))

            val = ""

            if line[3]:
                val = line[3].strip()

            if give_string:
                error_msg += val + " -> " + fname_number + "\n"
            else:
                error_msg += "" + fname_number + ": " + val + "\n"

    except Exception as e:
        console(e)

    if give_string:
        return error_msg.replace("\033[95m", "")
    else:
        try:
            sys.stderr.write(str(error_msg) + '\n\033[0m')
        except IOError:
            console(error_msg)

    if again:
        raise exc

    return "\033[33m" + error_msg


def header_trigger(s):
    """
    @type s: str
    @return: None
    """
    for t in ["CONTROLLER", "POD", "NAME", "FIRSTSEEN"]:
        if s.strip().startswith(t):
            return True

    return False


def human_now(timedelta_seconds=3600):
    """
    @type timedelta_seconds: str
    """
    return timestamp_to_string_gmt(time.time() + timedelta_seconds)


def humanize(word):
    """
    @type word: str
    @return: None
    """
    word = re.sub(r"_id$", "", word)
    word = word.replace('_', ' ')
    word = re.sub(r"(?i)([a-z\d]*)", lambda m: m.group(1).lower(), word)
    word = re.sub(r"^\w", lambda m: m.group(0).upper(), word)

    return word


def humansize(inbytes, system=g_sizesystem_alternative_lower, color=True):
    """
    @type inbytes: list
    @type system: float
    @type color: bool
    @return: None
    """
    factor = 1
    suffix = "b."

    for factor, suffix in system:
        if inbytes >= factor:
            break

    amount = int(inbytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix

        if amount == 1:
            suffix = singular
        else:
            suffix = multiple

    if color is True:
        inbytes = float(inbytes)

        if inbytes >= 1024 * 1024 * 1024:
            color = 35
        elif inbytes >= 1024 * 1024 * 1024:
            color = 92
        elif inbytes >= 1024 * 1024:
            color = 34
        elif inbytes >= 1024 * 10:
            color = 33
        elif inbytes < 1024 * 10:
            color = 36
        else:
            color = 91

        result = "\033[" + str(color) + "m" + str(amount) + suffix + "\033[0m"
    else:
        result = str(amount) + suffix

    return result


def info(command, description):
    """
    @type command: str, None
    @type description: str, None
    @return: None
    """
    if command is None:
        command = "?"

    if description is None:
        console(command, color="red", plaintext=not get_debugmode(), line_num_only=4)
    else:
        console_cmd_desc(command, description, "default")


def list_add_capitalize(l):
    """
    @type l: list
    @return: list
    """
    nl = []

    for i in l:
        nl.append(i)

        if hasattr(i, "capitalize"):
            nl.append(i.capitalize())

    return list(set(nl))


def log_date_time_string():
    """
    log_date_time_string
    @return: @rtype:
    """
    ts = "[" + timestamp_to_string_gmt(time.time()) + "]"
    return ts


def mill(it, label='', hide=None, expected_size=None, every=1):
    """
    @type it: iterator
    @type label: str
    @type hide: str, None
    @type expected_size: int, None
    @type every: int
    @return: None
    """
    stream = sys.stderr
    mill_chars = ['|', '/', '-', '\\']
    mill_template = '%s %s %i/%i\r'

    def _mill_char(_i):
        """
        @type _i: int
        @return: None
        """
        if _i >= count:
            return ' '
        else:
            return mill_chars[(_i // every) % len(mill_chars)]

    def _show(_i):
        """
        @type _i: int
        @return: None
        """
        if not hide:
            if ((_i % every) == 0 or         # True every "every" updates
                    (_i == count)):            # And when we're done
                stream.write(mill_template % (
                    label, _mill_char(_i), _i, count))

                stream.flush()
    count = len(it) if expected_size is None else expected_size

    if count:
        _show(0)

    for i, item in enumerate(it):
        yield item
        _show(i + 1)

    if not hide:
        stream.write('\n')
        stream.flush()


def ordinal(number):
    """
    @type number: str
    @return: None
    """
    number = abs(int(number))

    if number % 100 in (11, 12, 13):
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd", }.get(number % 10, "th")


def ordinalize(number):
    """
    @type number: str
    @return: None
    """
    return "%s%s" % (number, ordinal(number))


def parameterize(mystring, separator='-'):
    """
    @type mystring: str
    @type separator: str
    @return: None
    """
    mystring = transliterate(mystring)
    mystring = re.sub(r"(?i)[^a-z0-9\-_]+", separator, mystring)

    if separator:
        re_sep = re.escape(separator)
        mystring = re.sub(r'%s{2,}' % re_sep, separator, mystring)
        mystring = re.sub(r"(?i)^%(sep)s|%(sep)s$" % {'sep': re_sep}, '', mystring)

    return mystring.lower()


def pluralize(word):
    """
    @type word: str
    @return: None
    """
    if not word or word.lower() in UNCOUNTABLES:
        return word
    else:
        for rule, replacement in PLURALS:
            if re.search(rule, word):
                return re.sub(rule, replacement, word)

        return word


def pretty_print_json(jsondata, tofilename=None):
    """
    @type jsondata: str
    @type tofilename: str, None
    """
    jsonproxy = json.decode(jsondata)

    if tofilename is None:
        return json.dumps(jsonproxy, sort_keys=True, indent=4, separators=', ')
    else:
        json.dump(jsonproxy, open(tofilename, "w"), sort_keys=True, indent=4, separators=(',', ': '))
        return tofilename


def print_stdout(chara, cnt=0, moddiv=1):
    """
    @type chara: str
    @type cnt: int
    @type moddiv: int
    @return: None
    """
    cnt += 1

    if cnt % moddiv == 0:
        sys.stdout.write(chara)
        sys.stdout.flush()

    return cnt


def query_yes_no(args, force=False, default=True, command=None):
    """
    @type args: str,list
    @type force: bool
    @type default: bool
    @type command: str, None
    @return: None
    """
    question = ""
    t = True

    if isinstance(args, list):
        for arg in args:
            if t:
                question += "\033[96m"
                t = False
            else:
                question += "\033[33m"

            question += str(arg)
            question += "? \033[0m"
    else:
        question += "\033[96m"
        question += str(args)
        question += "? \033[0m"

    question = question.replace("??", "?")

    if force is True:
        return default

    valid = {"yes": "yes", "y": "yes", "ye": "yes",
             "no": "no", "n": "no",
             "quit": "quit", "qui": "quit", "qu": "quit", "q": "quit"}

    if default is None:
        prompt = "[y/N/q]"
    elif default:
        prompt = "[Y/n/q]"
    elif not default:
        prompt = "[y/N/q]"
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        if command is not None:
            question = str(command) + ": "

        console(question, plaintext=True, newline=True)
        console(prompt, color="white", plaintext=True, newline=False)
        choice = input("$: ").lower()

        if default is not None and choice == '':
            if default is True:
                return True
            else:
                return False

        elif choice in valid.keys():
            choice = valid[choice]

            if choice == "quit":
                raise SystemExit(question + "-> quit")

            console("-> " + choice, color="white", plaintext=True)

            if choice == "yes":
                return True
            else:
                return False
        else:
            console("please respond with 'yes', 'no' or 'quit'.\n", color="darkyellow", plaintext=True)


def remove_color(mystring):
    """
    @type mystring: str
    @return: None
    """
    return remove_escapecodes(mystring)


def remove_escapecodes(escapedstring):
    """
    @type escapedstring: str
    @return: None
    """
    ansi_escape = re.compile(r'\x1b[^a-z]*[a-z]')
    return ansi_escape.sub('', escapedstring)


def remove_extra_indentation(doc, stop_looking_when_encountered=None, padding=0, frontspacer=" "):
    """
    @type doc: str
    @type stop_looking_when_encountered: str, None
    @type padding: int
    @type frontspacer: str
    @return: None
    """
    startspaces = len(doc.lstrip("\n")) - len(doc.lstrip("\n").lstrip(" "))

    if doc is None:
        console_warning("doc is None")
        return doc

    newdoc = ""
    whitespacecount = -1
    keeplookingforindention = True

    for line in doc.split("\n"):
        line = line.rstrip()

        if stop_looking_when_encountered is not None:
            if line.lower().startswith(stop_looking_when_encountered):
                keeplookingforindention = False

        if keeplookingforindention is True and '"""' not in line and len(line.strip()) > 0:
            whitespacecount2 = len(line) - len(line.lstrip())
            if (whitespacecount2 < whitespacecount) or (whitespacecount < 0):
                whitespacecount = whitespacecount2

    for line in doc.split("\n"):
        line = str(" " * padding) + line[whitespacecount:]
        newdoc += line + "\n"

    newdoc = newdoc.strip()
    newdoc = str(frontspacer * ((startspaces - whitespacecount) + padding)) + newdoc.lstrip()
    return newdoc


def reset_console():
    """
    reset console
    """
    stty_sane()


def reset_terminal():
    """
    reset_terminal
    """
    stty_sane()


def resetterminal():
    """
    resetterminal():
    """
    sys.stderr.write('\033[0m')
    return


def running_in_debugger(include_tests=False):
    """
    @type include_tests: bool
    @return:
    @raise:
    """
    if not sys.stdout.isatty():
        return True

    sysglob = SystemGlobals()

    if (include_tests is False and sysglob.g_running_in_debugger is None) or (include_tests is True and sysglob.g_running_in_debugger_unit_tests is None):
        in_debugger = False
        stack = stack_trace(ret_list=True, reverse_stack=False)

        for i in stack:
            i = str(i)

            if "simple_server.py" in i:
                in_debugger = True
                print("debugger, simple_server.py")

            if include_tests:
                if "unittest.TextTestRunner" in i:
                    in_debugger = True
                elif "TeamcityTestRunner().run" in i:
                    in_debugger = True
                elif "test.py" in i:
                    in_debugger = True

            if "debugger.run" in i:
                in_debugger = True

            if in_debugger:
                break

        if include_tests:
            sysglob.g_running_in_debugger_unit_tests = in_debugger

        sysglob.g_running_in_debugger = in_debugger
    else:
        if include_tests:
            in_debugger = sysglob.g_running_in_debugger_unit_tests
        else:
            in_debugger = sysglob.g_running_in_debugger

    return in_debugger


def set_console_start_time():
    """
    set_console_start_time
    """
    global g_start_time
    g_start_time = time.time()


def singularize(word):
    """
    @type word: str
    @return: None
    """
    for inflection in UNCOUNTABLES:
        if re.search(r'(?i)\b(%s)\Z' % inflection, word):
            return word

    for rule, replacement in SINGULARS:
        if re.search(rule, word):
            return re.sub(rule, replacement, word)

    return word


def size_columns(columncounter, g_width_console_columns, subs, donotuseredis):
    """
    @type columncounter: int
    @type g_width_console_columns: list
    @type subs: str
    @type donotuseredis: bool
    @return: (int, str)
    """
    if donotuseredis:
        return columncounter, subs
    global g_column_resize_threshold

    # noinspection PyBroadException
    try:
        if g_column_resize_threshold is not None:
            return g_column_resize_threshold
    except:
        return columncounter, subs
    try:
        lsub = len(str(subs))
    except Exception as ex:
        print(ex)
        lsub = len(subs)

    if len(g_width_console_columns) <= columncounter:
        g_width_console_columns.append(lsub)
    else:
        if g_width_console_columns[columncounter] < lsub:
            g_width_console_columns[columncounter] = lsub

        column_resize_threshold = g_column_resize_threshold

        if g_column_resize_threshold is None:
            column_resize_threshold = 15

        if (g_width_console_columns[columncounter] - lsub) > column_resize_threshold:
            g_width_console_columns[columncounter] = lsub
            g_column_resize_threshold = 15
        else:
            g_column_resize_threshold = column_resize_threshold - 1

    if (g_width_console_columns[columncounter] - lsub) > 0:
        if columncounter < 3:
            subs += " " * (g_width_console_columns[columncounter] - lsub)

    columncounter += 1
    return columncounter, subs


def sizeof_fmt(num, suffix=''):
    """
    @type num: int, float
    @type suffix: str
    @return: None
    """
    if num is None:
        return num

    numorg = num
    num = float(num) / 1024

    if num < 0.1:
        return numorg
    for unit in ['Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)

        num /= 1024.0

    return "%.1f%s%s" % (num, 'Yi', suffix)


def snake_case(word, remove_spaces=True):
    """
    @type word: str
    @type remove_spaces: bool
    @return: None
    """
    if remove_spaces is True:
        word = word.replace(" ", "_")

    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


def source_code_link(stack_offset=0, fullline=True):
    """
    @type stack_offset: int
    @type fullline: bool
    """
    return stack_trace(line_num_only=2 + stack_offset, fullline=fullline)


def source_code_link_func(func_object):
    """
    @type func_object: function, None
    """
    if func_object is None:
        return "no-link"

    fname, funcname, linenr = func_info(func_object)
    link = 'File "' + fname + '", line ' + str(linenr) + " (" + str(funcname) + ")"

    if running_in_debugger():
        return link
    else:
        return format_source_code_line_console(link)


def spaces_leftside(mystring):
    """
    @type mystring: str
    @return: int
    """
    mystring = get_safe_string(mystring)
    fl = len(mystring)
    mystring = mystring.lstrip()
    return fl - len(mystring)


def stack_as_string():
    """
    stack_as_string
    """
    if sys.version_info.major == 3:
        stack = io.StringIO()
    else:
        stack = io.BytesIO()

    traceback.print_stack(file=stack)
    stack.seek(0)
    stack = stack.read()
    return stack


def stack_trace(line_num_only=0, ret_list=False, fullline=False, reverse_stack=True, extralevel=False):
    """
    @type line_num_only: int
    @type ret_list: bool
    @type fullline: bool
    @type reverse_stack: bool
    @type extralevel: bool
    @return: None
    """
    stack = stack_as_string()

    if ret_list and (line_num_only > 0):
        raise Exception("ret_list or line_num_only both true")

    stackl = []
    stack = stack.split("\n")

    if reverse_stack:
        stack.reverse()

    cnt = 0

    for i in stack:
        i = str(i)
        stackl.append(i)

        if line_num_only > 0:
            if "line" in i and "File" in i:
                if cnt > line_num_only - 1:
                    for j in i.split("line"):
                        for k in j.split(","):
                            try:
                                ln = int(k)

                                if fullline or extralevel:
                                    codeline = i.strip()
                                    codeline = codeline.split(", in ")

                                    if extralevel:
                                        codepath = os.path.basename(os.path.dirname(codeline[0]))
                                        codepath += "/"
                                        codepath += os.path.basename(codeline[0])
                                        return codepath + " (" + codeline[1] + ")"
                                    else:
                                        return codeline[0] + " (" + codeline[1] + ")"
                                else:
                                    i = i.replace("File ", "")

                                fs = i.replace('"', "").split(",")[0].split(os.sep)
                                return str("/".join(fs[len(fs) - 1:])) + ":" + str(ln)
                            except ValueError:
                                pass

                            except BaseException as be:
                                print(be)

                cnt += 1

    if line_num_only > 0:
        return str("?")

    if ret_list:
        return stackl

    return "\n".join(stackl)


def start_interactive_console():
    """
    start_interactive_console
    """
    HistoryConsole()


def stdoutwriteline(*args):
    """
    @type args: tuple
    @return: None
    """
    s = ""

    for i in args:
        s += str(i) + " "

    s = s.strip()
    sys.stdout.write(str(s) + "\n")
    sys.stdout.flush()

    return s


def stripall(astr):
    """
    @type astr: str
    @return: None
    """
    return remove_extra_indentation(astr)


def stty_sane():
    """
    stty_sane
    """
    os.system('stty sane')


def tableize(word):
    """
    @type word: str
    @return: None
    """
    return pluralize(underscore(word))


def timestamp_to_string_gmt(ts, short=False):
    """
    @type ts: float
    @type short: bool
    """
    monthname = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year, month, day, hh, mm, ss, x, y, z = time.gmtime(ts)

    if short:
        year -= 2000
        s = "%d-%d-%d %02d:%02d:%02d" % (day, month, year, hh, mm, ss)
    else:
        s = "%3s %02d %04d %02d:%02d:%02d" % (monthname[month], day, year, hh, mm, ss)

    return s


def titleize(word):
    """
    @type word: str
    @return: None
    """
    return re.sub(r"\b('?[a-z])", lambda match: match.group(1).capitalize(), humanize(underscore(word)))


def transliterate(mystring):
    """
    @type mystring: str
    @return: None
    """
    normalized = unicodedata.normalize('NFKD', mystring)
    return normalized.encode('ascii', 'ignore').decode('ascii')


def underscore(word):
    """
    @type word: str
    @return: None
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


def warning(command, description):
    """
    @type command: str, None
    @type description: str
    @return: None
    """
    if command is None:
        command = "?"

    linno = get_line_number()
    description += " \033[90m(" + str(linno) + ") \033[0m"
    console_cmd_desc(command, description, "red", enteraftercmd=False)


def main():
    """
    main
    """
    console("Consoleprinter is a library for use in commandline application")


SystemGlobals()

_irregular('child', 'children')
_irregular('cow', 'kine')
_irregular('man', 'men')
_irregular('move', 'moves')
_irregular('person', 'people')
_irregular('sex', 'sexes')
_irregular('zombie', 'zombies')

set_console_start_time()

standard_library.install_aliases()
"""
Human-readable file size.
Using the traditional system, where a factor of 1024 is used::
>>> size(10)
'10B'
>>> size(100)
'100B'
>>> size(1000)
'1000B'
>>> size(2000)
'1K'
>>> size(10000)
'9K'
>>> size(20000)
'19K'
>>> size(100000)
'97K'
>>> size(200000)
'195K'
>>> size(1000000)
'976K'
>>> size(2000000)
'1M'
Using the SI system, with a factor 1000::
>>> size(10, system=si)
'10B'
>>> size(100, system=si)
'100B'
>>> size(1000, system=si)
'1K'
>>> size(2000, system=si)
'2K'
>>> size(10000, system=si)
'10K'
>>> size(20000, system=si)
'20K'
>>> size(100000, system=si)
'100K'
>>> size(200000, system=si)
'200K'
>>> size(1000000, system=si)
'1M'
>>> size(2000000, system=si)
'2M'
"""


def slugify(value):
    """
    @type value: str
    """
    sysglob = SystemGlobals()
    hvalue = str(value)

    if hvalue in sysglob.g_slugified_unicode_lut:
        return sysglob.g_slugified_unicode_lut[hvalue]

    value = value.lower().replace("\\", "").replace("/", "")
    value = value.strip()
    slug = ""

    if sysglob.g_safe_alphabet:
        safechars = sysglob.g_safe_alphabet
    else:
        safechars = set(get_safe_alphabet())
    try:
        value = str(value)
    except UnicodeError:
        value = str(value)

    safechars = list(safechars)
    safechars.remove(" ")
    safechars = tuple(safechars)

    for c in value:
        if c in safechars:
            slug += c
        else:
            if isinstance(c, str):
                # noinspection PyArgumentEqualDefault #                                                                                                                                    after keyword 0
                c = c.encode()

            c64 = base64.encodebytes(c)
            slug += c64.decode("utf-8").strip().rstrip("=")

    retval = slug.lower()
    sysglob.g_slugified_unicode_lut[hvalue] = retval
    return retval


def strcmp(s1, s2):
    """
    @type s1: str or unicode
    @type s2: str or unicode
    @return: @rtype: bool
    """
    # noinspection PyArgumentEqualDefault #                                                                                                                                     after keyword 0
    s1 = s1.encode()

    # noinspection PyArgumentEqualDefault
    s2 = s2.encode()

    if not s1 or not s2:
        return False

    s1 = s1.strip()
    s2 = s2.strip()
    equal = s1 == s2
    return equal


if __name__ == "__main__":
    main()
