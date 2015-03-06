# coding=utf-8
"""
console
Active8 (05-03-15)
license: GNU-GPL2
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from builtins import super
from builtins import int
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from builtins import object

import time
import io
import traceback
import os
import sys
import socket
import logging
import base64
import json
import ujson


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
        @type k: str, unicode
        @return:
        @raise:
        """
        return k in self.g_memory

    def get(self, k):
        """
        @type k: str, unicode
        @return:
        @raise:
        """
        if not isinstance(k, str):
            raise AssertionError("keys must be string")

        if k not in self.g_memory:
            raise AssertionError(k + " not found")

        return self.g_memory[k]

    def set(self, k, v):
        """
        @type k: str, unicode
        @type v: object
        @return:
        @raise:
        """
        if not isinstance(k, str):
            raise AssertionError("keys must be string")

        console("SystemGlobals:set", k, once=True, color='grey', line_num_only=3)
        self.g_memory[k] = v


SystemGlobals()


def exist(data):
    """
    @type data: str, unicode, int, float, None, dict, list
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


def running_in_debugger(include_tests=False):
    """
    @type include_tests: bool
    @return:
    @raise:
    """
    sysglob = SystemGlobals()

    if (include_tests is False and sysglob.g_running_in_debugger is None) or (include_tests is True and sysglob.g_running_in_debugger_unit_tests is None):
        in_debugger = False
        stack = stack_trace(ret_list=True, reverse_stack=False)

        for i in stack:
            i = str(i)

            if "simple_server.py" in i:
                in_debugger = True
                print("crypto_data_lib.py:473", "debugger, simple_server.py")

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


def human_now(timedelta_seconds=3600):
    """
    @type timedelta_seconds: str, unicode
    """
    return timestamp_to_string_gmt(time.time() + timedelta_seconds)


def log_date_time_string():
    """
    log_date_time_string
    @return: @rtype:
    """
    ts = "[" + timestamp_to_string_gmt(time.time()) + "]"
    return ts


def stack_as_string():
    if sys.version_info.major==3:
        stack = io.StringIO()
    else:
        stack = io.BytesIO()
    traceback.print_stack(file=stack)
    stack.seek(0)
    stack = stack.read()
    return stack


def stack_trace(line_num_only=0, ret_list=False, fullline=False, reverse_stack=True):
    """
    @type line_num_only: int
    @type ret_list: bool
    @type fullline: bool
    @type reverse_stack: bool
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
                            # noinspection PyBroadException
                            try:
                                ln = int(k)

                                if fullline:
                                    codeline = i.strip()
                                    codeline = codeline.split(", in ")
                                    return codeline[0] + " (" + codeline[1] + ")"
                                else:
                                    i = i.replace("File ", "")

                                fs = i.replace('"', "").split(",")[0].split(os.sep)
                                return str("/".join(fs[len(fs) - 1:])) + ":" + str(ln)
                            except:
                                pass

                cnt += 1

    if line_num_only > 0:
        return str("?")

    if ret_list:
        return stackl

    return "\n".join(stackl)


def strcmp(s1, s2):
    """
    @type s1: str, unicode or unicode
    @type s2: str, unicode or unicode
    @return: @rtype: bool
    """
    # noinspection PyArgumentEqualDefault
    s1 = s1.encode("utf-8")

    # noinspection PyArgumentEqualDefault
    s2 = s2.encode("utf-8")

    if not s1 or not s2:
        return False

    s1 = s1.strip()
    s2 = s2.strip()
    equal = s1 == s2
    return equal


def set_console_start_time():
    """
    set_console_start_time
    """
    global g_start_time
    g_start_time = time.time()


def format_source_code_line_console(path):
    """
    @type path: str, unicode, unicode
    @return: @raise
    """
    paths = path.split(",")

    if len(paths) == 2:
        # dpath = os.path.basename(os.path.dirname(paths[0]))
        fpath = os.path.basename(paths[0]).strip().replace('"', "")
        location = paths[1].replace(' line ', ":").strip("/")
        return fpath + location.replace(" (", ":").replace(")", "").strip()
    else:
        return path


def source_code_link(stack_offset=0, fullline=True):
    """
    @type stack_offset: int
    @type fullline: bool
    """
    return stack_trace(line_num_only=2 + stack_offset, fullline=fullline)


set_console_start_time()

g_column_resize_threshold = None


def size_columns(columncounter, g_width_console_columns, subs, donotuseredis):
    """
    @type columncounter: int
    @type g_width_console_columns: list
    @type subs: str, unicode
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
        print("crypto_data_lib.py:546", "crypto_data.py:515", ex)
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


def console(*args, **kwargs):
    """
    @param args:
    @type args:
    @param kwargs
    @type kwargs:
    """
    sysglob = SystemGlobals()
    debug = False

    if debug:
        s = ""

        for i in args:
            s += str(i) + " "

        print("crypto_data_lib.py:590", "crypto_data.py:559", s)
        return
    global g_start_time
    runtime = "%0.2f" % float(time.time() - g_start_time)
    toggle = True
    arguments = list(args)
    line_num_only = 2
    print_stack = False
    warningmsg = False
    newline = True
    once = False
    stackpointer = 0
    plainprint = False

    if "msg" in kwargs:
        arguments = [kwargs["msg"]]

    if "print_stack" in kwargs:
        print_stack = kwargs["print_stack"]

    if "stack" in kwargs:
        line_num_only += kwargs["stack"]

    if "line_num_only" in kwargs:
        line_num_only = kwargs["line_num_only"]

    if "stackpointer" in kwargs:
        stackpointer = kwargs["stackpointer"]

    if "warning" in kwargs:
        warningmsg = kwargs["warning"]

    if "plainprint" in kwargs:
        plainprint = True

    if "dolstrip" in kwargs:
        dolstrip = kwargs["dolstrip"]
    else:
        dolstrip = True

    if "newline" in kwargs:
        newline = kwargs["newline"]

    colors = {'red': '\033[31m',
              'green': '\033[32m',
              'yellow': '\033[37m',
              'darkyellow': '\033[33m',
              'blue': '\033[34m',
              'magenta': '\033[35m',
              'cyan': '\033[36m',
              'white': '\033[97m',
              'black': '\033[90m',
              'grey': '\033[30m',
              'orange': '\033[91m',
              'default': '\033[0m'}

    if "color" in kwargs:
        color = kwargs["color"]
    else:
        color = "default"

    if plainprint is True:
        print(colors[color] + "".join(arguments) + "\033[0m")
        return

    if "donotuseredis" in kwargs:
        donotuseredis = kwargs["donotuseredis"]
    else:
        donotuseredis = True

    if color not in colors:
        console(color, "not available", source_code_link(1), color='red')
        color = "default"

    if "ret_str" not in kwargs:
        dbs = colors['yellow'] + str(runtime) + colors['yellow']
    else:
        dbs = ""

    source_code_link_msg = None
    columncounter = 0

    if not source_code_link_msg:
        if stackpointer == 0:
            source_code_link_msg = stack_trace(line_num_only=line_num_only).strip()
        else:
            source_code_link_msg = ""

            for i in range(0, stackpointer + 1):
                scm = str(stack_trace(line_num_only=line_num_only + i)).strip()
                if scm != "?":
                    source_code_link_msg += "\n\t"
                    source_code_link_msg += scm

            source_code_link_msg += "\n\t"

    if not print_stack:
        if line_num_only >= 0:
            if "ret_str" not in kwargs:
                if warningmsg:
                    fcolor = "red"
                else:
                    fcolor = "yellow"

                subs = " | " + colors[fcolor] + source_code_link_msg + colors[fcolor]
                columncounter, subs = size_columns(columncounter, sysglob.g_width_console_columns, subs, donotuseredis)
                dbs += subs

    for s in arguments:
        if toggle:
            if warningmsg:
                dbs += colors['red']
            else:
                dbs += colors[color]
        else:
            dbs += colors['default']

        toggle = not toggle

        if s is None:
            s = "None"

        if s == "":
            s = ""
        else:
            dbs += " |"

        if isinstance(s, dict):
            s = s.copy()

            # noinspection PyBroadException
            try:
                s = ujson.dumps(s, indent=1)
            except Exception:
                try:
                    for k in s:
                        s[k] = str(s[k])
                    import json
                    s = json.dumps(s, indent=1)
                except Exception as e:
                    s = str(s)
                    s += " | error dumping dict" + str(e) + " | "

            subs = str(s)
        else:
            subs = str(s).replace("\n", "")

        if dolstrip:
            subs = " " + subs.strip()
        else:
            subs = " " + subs.rstrip()

        columncounter, subs = size_columns(columncounter, sysglob.g_width_console_columns, subs, donotuseredis)
        dbs += subs

    dbs += "\033[0m"

    if "ret_str" in kwargs:
        if kwargs["ret_str"] is True:
            return dbs.strip()

    if print_stack:
        newline = False
        trace = stack_trace(ret_list=True)
        toggle = True
        stackline = ""
        stackcnt = 0
        dbs += colors["yellow"]
        dbs += "\n"
        lastitem = ""

        for item in trace:
            if 3 < stackcnt < 18:
                if not toggle:
                    if lastitem != "":
                        dbs += " " * len(runtime)

                if toggle:
                    stackline = item.strip().split(", in")[0]
                else:
                    if running_in_debugger(include_tests=True):
                        if lastitem != "":
                            dbs += " | " + stackline + " -> " + lastitem + "\n"

                        lastitem = item.strip()
                    else:
                        if lastitem != "":
                            dbs += " | " + format_source_code_line_console(stackline) + " -> " + lastitem + "\n"

                        lastitem = item.strip()

                toggle = not toggle

            stackcnt += 1

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

    sys.stderr.write(dbs)
    sys.stderr.flush()
    time.sleep(0.01)
    logger = logging.getLogger("crypto_data")

    if len(logger.handlers) > 0:
        for color in colors:
            dbs = dbs.replace(colors[color], "")

        logger.info(dbs.strip().replace("\n", ""))


def console_saved_exception(excstr, verbose=True):
    """
    @type excstr: str, unicode
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


def resetterminal():
    """
    resetterminal():
    """
    sys.stderr.write('\033[0m')
    return


def handle_ex(exc=None, again=True, give_string=False, extra_info=None, source_code_links=True):
    """
    @type exc: Exception, None
    @type again: bool
    @type give_string: bool
    @type extra_info: str, unicode, list
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
        raise

    return "\033[93m" + error_msg


def console_exception(ex):
    """
    @type ex: object, Exception
    """
    exstr = handle_ex(ex, False, True)
    console_saved_exception(exstr)


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


def consoledict(mydict, members=None):
    """
    @type mydict: dict
    @type members: list, None
    @return: None
    """
    dbs = "\033[92m" + log_date_time_string() + " "
    dbs += stack_trace(line_num_only=2)
    dbs += "\033[93m\n"

    if isinstance(mydict, dict):
        if members is not None:
            for i in members:
                dbs += " " + str(i) + " : " + str(mydict[i]) + "\n"
        else:
            for i in mydict:
                dbs += " " + str(i) + " : " + str(mydict[i]) + "\n"
    else:
        dbs += "not dict: " + str(mydict) + "\n"

    sys.stderr.write(dbs)
    return ""


def slugify(value):
    """
    @type value: str, unicode
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

    for c in value:
        if c in safechars:
            slug += c
        else:
            c64 = base64.encodestring(c).strip().rstrip("=")
            slug += c64

    retval = slug.lower()
    sysglob.g_slugified_unicode_lut[hvalue] = retval
    return retval


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


def console_warning(*args, **kwargs):
    """
    @param args
    @type args:
    @param kwargs
    @type kwargs:
    """
    if "print_stack" in kwargs:
        print_stack = kwargs["print_stack"]
    else:
        print_stack = False

    if "line_num_only" in kwargs:
        line_num_only = kwargs["line_num_only"]
    else:
        line_num_only = 3

    if "once" in kwargs:
        once = kwargs["once"]
    else:
        once = False

    if running_in_debugger(True):
        args = list(args)
        args.insert(0, "==")
        args.append(source_code_link(line_num_only - 2))
        args.append("==")

    console(*args, print_stack=print_stack, warning=True, line_num_only=line_num_only, once=once)


def fpath_in_stack(fpath):
    """
    @type fpath: str, unicode
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


def pretty_print_json(jsondata, tofilename=None):
    """
    @type jsondata: str, unicode
    @type tofilename: str, unicode, None
    """
    jsonproxy = ujson.decode(jsondata)

    if tofilename is None:
        return json.dumps(jsonproxy, sort_keys=True, indent=4, separators=', ')
    else:
        json.dump(jsonproxy, open(tofilename, "w"), sort_keys=True, indent=4, separators=(',', ': '))
        return tofilename


def clear_screen():
    """
    clear_screen
    """
    if sys.stderr.isatty():
        sys.stderr.write('\x1Bc')
        sys.stderr.flush()


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
        @type o: str, unicode
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


def get_hostname():
    """
    get_hostname
    """
    return str(socket.gethostname())


def get_alphabet():
    """
    get_alphabetget_safe_alphabet
    """
    return tuple(['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', ' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                  'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])


def get_safe_alphabet():
    """
    get_alphabet
    """
    return tuple(['~', '_', '.', '-', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c',
                  'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])


def get_alphabet_lower():
    """
    get_alphabet_lower
    """
    return tuple(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])


def get_alphabet_lower_numbers():
    """
    get_alphabet_lower_numbers
    """
    return tuple(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])


def get_vowels_lower():
    """
    get_vowels_lower
    """
    return tuple(['a', 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'])


def main():
    """
    main
    """
    console("test")


if __name__ == "__main__":
    main()
