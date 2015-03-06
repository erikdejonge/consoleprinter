# coding=utf-8
"""
console
Active8 (05-03-15)
license: GNU-GPL2
"""
<<<<<<< HEAD
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from unittester import *
from consoleprinter import *


class ConsoleTest(unittest.TestCase):

    def test_slugify(self):
        """
        test_slugify
        """
        self.assertEqual(slugify("Hello€€€WorldFoo BarMy file.xls"), "hello4oks4oks4oksworldfooiabarmyiafile.xls")
        self.assertEqual(slugify("Hello€€€WorldFoo Bar"), "hello4oks4oks4oksworldfooiabar")
        self.assertEqual(slugify("Hello 7234 Foobar-World2"), "helloia7234iafoobar-world2")
        self.assertEqual(slugify("Hello WorldFoo Bar"), "helloiaworldfooiabar")
        self.assertEqual(slugify("yUo Xnm*a"), "yuoiaxnmkga")
        self.assertEqual(slugify("FiNNaI%y~foo"), "finnaijqy~foo")
        self.assertEqual(slugify("yGg5C4eBG"), "ygg5c4ebg")
        self.assertEqual(slugify("Y1fWg@79t"), "y1fwgqa79t")
        self.assertEqual(slugify("0f)5m@t0nS"), "0fkq5mqat0ns")
        self.assertEqual(slugify("8Q#a5devJ6r"), "8qiwa5devj6r")
        self.assertEqual(slugify("cHXE*Ya ueme"), "chxekgyaiaueme")
        self.assertEqual(slugify("JKBnvMkKK^2"), "jkbnvmkkkxg2")
        self.assertEqual(slugify("$RdoI1ghgqQf"), "jardoi1ghgqqf")
        self.assertEqual(slugify("^4OF7YXm0lCi8_t+"), "xg4of7yxm0lci8_tkw")
        self.assertEqual(slugify("Y3NtOAFlHNlvoW3QwCd"), "y3ntoaflhnlvow3qwcd")
        self.assertEqual(slugify("xWn EQ#(bbj9+^&9xuOj"), "xwniaeqiwkabbj9kwxgjg9xuoj")
        self.assertEqual(slugify("cO^I0Dt@X&1*sfIvUxCA"), "coxgi0dtqaxjg1kgsfivuxca")
        self.assertEqual(slugify("d89p8o3*iI2+6bWd1CX@1"), "d89p8o3kgii2kw6bwd1cxqa1")
        self.assertEqual(slugify("Ks68l6MN9On3GcAMfnB6t"), "ks68l6mn9on3gcamfnb6t")
        self.assertEqual(slugify("X8+y&yKigfmpKE_F0Eoxwf"), "x8kwyjgykigfmpke_f0eoxwf")
        self.assertEqual(slugify("oaJWpypbhFr+zLRL4*weU$"), "oajwpypbhfrkwzlrl4kgweuja")
        self.assertEqual(slugify("i(C + FUKV$7m(W@KnzbA"), "ikaciakwiafukvja7mkawqaknzba")
        self.assertEqual(slugify("k0ruekX#F81q^ Qso1wasbMhePv)4"), "k0ruekxiwf81qxgiaqso1wasbmhepvkq4")
        self.assertEqual(slugify("Za_SDw7y!#Q0N$XU2PXkZKQBHEM*INn"), "za_sdw7yiqiwq0njaxu2pxkzkqbhemkginn")
        self.assertEqual(slugify("@FI0Rl%C%+VBBqpv4us&eV(wVp5L9ac"), "qafi0rljqcjqkwvbbqpv4usjgevkawvp5l9ac")
        self.assertEqual(slugify("^7oS1ngoY5XTzOp@K_&fV27dUa)rXu1"), "xg7os1ngoy5xtzopqak_jgfv27duakqrxu1")
        self.assertEqual(slugify("GD31vDpPVS9eC4t@XyRS9#^$fSK8Ikv"), "gd31vdppvs9ec4tqaxyrs9iwxgjafsk8ikv")
        self.assertEqual(slugify("Saa1N%irJhxRtJ)@TeyvCPe(3MY0_GxrPq"), "saa1njqirjhxrtjkqqateyvcpeka3my0_gxrpq")
        self.assertEqual(slugify("8+HMg%*#+BI5G2Q W6zIdUZetfExAf7%4I4nw"), "8kwhmgjqkgiwkwbi5g2qiaw6ziduzetfexaf7jq4i4nw")
        self.assertEqual(slugify("dMCAMmK+6pQSVzB4%8@nbg*(yaIYrCMXOTr0eh"), "dmcammkkw6pqsvzb4jq8qanbgkgkayaiyrcmxotr0eh")
        self.assertEqual(slugify("E5O$zBLa%gw+B1deX 5a)n0@mHp$x2Zr7+YV2SQf_"), "e5ojazblajqgwkwb1dexia5akqn0qamhpjax2zr7kwyv2sqf_")
        self.assertEqual(slugify("o #9 0taChMxv8uh&TLDX4KbczB80M(wGrgPlsWYMkEsq 0Q3Id"), "oiaiw9ia0tachmxv8uhjgtldx4kbczb80mkawgrgplswymkesqia0q3id")
        self.assertEqual(slugify("GDRp6o#O(2RfG%hpB%6wL1u5+21DIJsg&6E%t6 is5Rgtpy^p1^h_s"), "gdrp6oiwoka2rfgjqhpbjq6wl1u5kw21dijsgjg6ejqt6iais5rgtpyxgp1xgh_s")
        self.assertEqual(slugify("Nl_#SQxRJ(G)NN328P8D!DuVVHn@f6OlQT9Lnup1ZkHo5ZyaJxK2&5R^R0Li74"), "nl_iwsqxrjkagkqnn328p8diqduvvhnqaf6olqt9lnup1zkho5zyajxk2jg5rxgr0li74")

    def test_stack_trace(self):
        """
        test_stack_trace
        """
        stack = stack_trace(1)
        self.assertTrue("tests.py:" in stack)

    def test_fpath_in_stack(self):
        """
        test_fpath_in_stack
        """
        self.assertTrue(fpath_in_stack("tests.py"))
        self.assertFalse(fpath_in_stack("website"))

    def test_timestamp_to_string(self):
        """
        test_timestamp_to_string
        """
        option1 = "Jul 24 2013 23:14:30"
        option2 = "Jul 25 2013 06:14:30"
        option3 = "Jul 24 2013 20:14:30"
        val = timestamp_to_string_gmt(1374732870.483823)
        checked = val in [option1, option2, option3]
        self.assertTrue(checked)

    def test_exist(self):
        """
        test_exist
        """
        self.assertFalse(exist(""))
        self.assertFalse(exist(None))
        self.assertFalse(exist(False))
        self.assertFalse(exist("false"))
        self.assertFalse(exist("false"))
        self.assertTrue(exist("hello"))
        self.assertTrue(exist([1, 2]))
        self.assertTrue(exist({1, 2}))
        self.assertTrue(exist((1, 2)))
        self.assertTrue(exist(True))
        self.assertTrue(exist(1))
        self.assertTrue(exist(1.0))
        self.assertFalse(exist(False))
        self.assertFalse(exist(0))
        self.assertFalse(exist(0.0))
        self.assertFalse(exist([]))
        self.assertFalse(exist(set()))
        self.assertFalse(exist(tuple()))

        o = None
        self.assertFalse(exist(o))

        o = SystemGlobals()
        self.assertTrue(exist(o))

    def test_strcmp(self):
        """
        test_strcmp
        """
        self.assertFalse(strcmp("hello", "world"))
        self.assertTrue(strcmp("hello", "hello "))

    def test_console(self):
        """
        test_console
        """
        console("hello world")
        colors = ['black', 'blue', 'cyan', 'default', 'green', 'grey', 'magenta', 'orange', 'red', 'white', 'yellow', 'darkyellow']


        for color in colors:
            console(color, color=color)

        


        for color in colors:
            console(color, color=color, plainprint=True)

    def test_warning(self):
        """
        test_warning
        """
        console_warning("Warning")

    def test_reversed_keywordparam(self):
        """
        """
=======

#from unittester import *
from consoleprinter import *
>>>>>>> 2150a385d987632f50d46f660f0b72f8af610089

# class ConsoleTest(unittest.TestCase):
#     def test_slugify(self):
#         """
#         test_slugify
#         """
#         self.assertEqual(slugify("Hello€€€WorldFoo BarMy file.xls"), "hello4oks4oks4oksworldfooiabarmyiafile.xls")
#         self.assertEqual(slugify("Hello€€€WorldFoo Bar"), "hello4oks4oks4oksworldfooiabar")
#         self.assertEqual(slugify("Hello 7234 Foobar-World2"), "helloia7234iafoobar-world2")
#         self.assertEqual(slugify("Hello WorldFoo Bar"), "helloiaworldfooiabar")
#         self.assertEqual(slugify("yUo Xnm*a"), "yuoiaxnmkga")
#         self.assertEqual(slugify("FiNNaI%y~foo"), "finnaijqy~foo")
#         self.assertEqual(slugify("yGg5C4eBG"), "ygg5c4ebg")
#         self.assertEqual(slugify("Y1fWg@79t"), "y1fwgqa79t")
#         self.assertEqual(slugify("0f)5m@t0nS"), "0fkq5mqat0ns")
#         self.assertEqual(slugify("8Q#a5devJ6r"), "8qiwa5devj6r")
#         self.assertEqual(slugify("cHXE*Ya ueme"), "chxekgyaiaueme")
#         self.assertEqual(slugify("JKBnvMkKK^2"), "jkbnvmkkkxg2")
#         self.assertEqual(slugify("$RdoI1ghgqQf"), "jardoi1ghgqqf")
#         self.assertEqual(slugify("^4OF7YXm0lCi8_t+"), "xg4of7yxm0lci8_tkw")
#         self.assertEqual(slugify("Y3NtOAFlHNlvoW3QwCd"), "y3ntoaflhnlvow3qwcd")
#         self.assertEqual(slugify("xWn EQ#(bbj9+^&9xuOj"), "xwniaeqiwkabbj9kwxgjg9xuoj")
#         self.assertEqual(slugify("cO^I0Dt@X&1*sfIvUxCA"), "coxgi0dtqaxjg1kgsfivuxca")
#         self.assertEqual(slugify("d89p8o3*iI2+6bWd1CX@1"), "d89p8o3kgii2kw6bwd1cxqa1")
#         self.assertEqual(slugify("Ks68l6MN9On3GcAMfnB6t"), "ks68l6mn9on3gcamfnb6t")
#         self.assertEqual(slugify("X8+y&yKigfmpKE_F0Eoxwf"), "x8kwyjgykigfmpke_f0eoxwf")
#         self.assertEqual(slugify("oaJWpypbhFr+zLRL4*weU$"), "oajwpypbhfrkwzlrl4kgweuja")
#         self.assertEqual(slugify("i(C + FUKV$7m(W@KnzbA"), "ikaciakwiafukvja7mkawqaknzba")
#         self.assertEqual(slugify("k0ruekX#F81q^ Qso1wasbMhePv)4"), "k0ruekxiwf81qxgiaqso1wasbmhepvkq4")
#         self.assertEqual(slugify("Za_SDw7y!#Q0N$XU2PXkZKQBHEM*INn"), "za_sdw7yiqiwq0njaxu2pxkzkqbhemkginn")
#         self.assertEqual(slugify("@FI0Rl%C%+VBBqpv4us&eV(wVp5L9ac"), "qafi0rljqcjqkwvbbqpv4usjgevkawvp5l9ac")
#         self.assertEqual(slugify("^7oS1ngoY5XTzOp@K_&fV27dUa)rXu1"), "xg7os1ngoy5xtzopqak_jgfv27duakqrxu1")
#         self.assertEqual(slugify("GD31vDpPVS9eC4t@XyRS9#^$fSK8Ikv"), "gd31vdppvs9ec4tqaxyrs9iwxgjafsk8ikv")
#         self.assertEqual(slugify("Saa1N%irJhxRtJ)@TeyvCPe(3MY0_GxrPq"), "saa1njqirjhxrtjkqqateyvcpeka3my0_gxrpq")
#         self.assertEqual(slugify("8+HMg%*#+BI5G2Q W6zIdUZetfExAf7%4I4nw"), "8kwhmgjqkgiwkwbi5g2qiaw6ziduzetfexaf7jq4i4nw")
#         self.assertEqual(slugify("dMCAMmK+6pQSVzB4%8@nbg*(yaIYrCMXOTr0eh"), "dmcammkkw6pqsvzb4jq8qanbgkgkayaiyrcmxotr0eh")
#         self.assertEqual(slugify("E5O$zBLa%gw+B1deX 5a)n0@mHp$x2Zr7+YV2SQf_"), "e5ojazblajqgwkwb1dexia5akqn0qamhpjax2zr7kwyv2sqf_")
#         self.assertEqual(slugify("o #9 0taChMxv8uh&TLDX4KbczB80M(wGrgPlsWYMkEsq 0Q3Id"), "oiaiw9ia0tachmxv8uhjgtldx4kbczb80mkawgrgplswymkesqia0q3id")
#         self.assertEqual(slugify("GDRp6o#O(2RfG%hpB%6wL1u5+21DIJsg&6E%t6 is5Rgtpy^p1^h_s"), "gdrp6oiwoka2rfgjqhpbjq6wl1u5kw21dijsgjg6ejqt6iais5rgtpyxgp1xgh_s")
#         self.assertEqual(slugify("Nl_#SQxRJ(G)NN328P8D!DuVVHn@f6OlQT9Lnup1ZkHo5ZyaJxK2&5R^R0Li74"), "nl_iwsqxrjkagkqnn328p8diqduvvhnqaf6olqt9lnup1zkho5zyajxk2jg5rxgr0li74")
#     def test_stack_trace(self):
#         """
#         test_stack_trace
#         """
#         stack = stack_trace(1)
#         self.assertTrue("tests.py:" in stack)
#     def test_fpath_in_stack(self):
#         """
#         test_fpath_in_stack
#         """
#         self.assertTrue(fpath_in_stack("tests.py"))
#         self.assertFalse(fpath_in_stack("website"))
#     def test_timestamp_to_string(self):
#         """
#         test_timestamp_to_string
#         """
#         option1 = "Jul 24 2013 23:14:30"
#         option2 = "Jul 25 2013 06:14:30"
#         option3 = "Jul 24 2013 20:14:30"
#         val = timestamp_to_string_gmt(1374732870.483823)
#         checked = val in [option1, option2, option3]
#         self.assertTrue(checked)
#     def test_exist(self):
#         """
#         test_exist
#         """
#         self.assertFalse(exist(""))
#         self.assertFalse(exist(None))
#         self.assertFalse(exist(False))
#         self.assertFalse(exist("false"))
#         self.assertFalse(exist("false"))
#         self.assertTrue(exist("hello"))
#         self.assertTrue(exist([1, 2]))
#         self.assertTrue(exist({1, 2}))
#         self.assertTrue(exist((1, 2)))
#         self.assertTrue(exist(True))
#         self.assertTrue(exist(1))
#         self.assertTrue(exist(1.0))
#         self.assertFalse(exist(False))
#         self.assertFalse(exist(0))
#         self.assertFalse(exist(0.0))
#         self.assertFalse(exist([]))
#         self.assertFalse(exist(set()))
#         self.assertFalse(exist(tuple()))
#         o = None
#         self.assertFalse(exist(o))
#         o = SystemGlobals()
#         self.assertTrue(exist(o))
#     def test_strcmp(self):
#         """
#         test_strcmp
#         """
#         self.assertFalse(strcmp("hello", "world"))
#         self.assertTrue(strcmp("hello", "hello "))
#     def test_console(self):
#         """
#         test_console
#         """
#         console("hello world")
#         colors = ['black', 'blue', 'cyan', 'default', 'green', 'grey', 'magenta', 'orange', 'red', 'white', 'yellow', 'darkyellow']
#         print("linenumbers")
#         for color in colors:
#             console(color, color=color)
#         print()
#         print("plain")
#         for color in colors:
#             console(color, color=color, plainprint=True)
#     def test_warning(self):
#         """
#         test_warning
#         """
#         console_warning("Warning")
#     def test_reversed_keywordparam(self):
#         """
#         #     test_reversed_keywordparam
#         """
#         console("next line should be foobar")
#         console(color="red", msg="foobar")


def main():
    """
    main
    """
    colors = ['black', 'blue', 'cyan', 'default', 'green', 'grey', 'magenta', 'orange', 'red', 'white', 'yellow', 'darkyellow']

    for color in colors:
        console(color, color=color)


if __name__ == "__main__":
    main()
