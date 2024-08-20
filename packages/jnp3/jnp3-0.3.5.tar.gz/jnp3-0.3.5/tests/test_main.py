# coding: utf8
import unittest
from unittest import TestCase

from jnp3.misc import deprecated, url2cn, group_by
from jnp3.path import path_not_exist, get_log_dir
from jnp3.dict import get_with_chained_keys, append_dic


@deprecated("Use `ord`")
def char_utf8_to_unicode(char):
    """将 utf8 字符转换为 unicode

    对于 n 个字节的 utf8 编码，第一个字节的前 n 位为 1，第 n+1 位为 0，
    之后每个字节的前两位为 10，其它都是 unicode 编码

    :param char: the character
    :return: the unicode in decimal
    """
    return ord(char)


class MainTestCase(TestCase):

    @deprecated("Use `chr`")
    def unicode_to_utf8_char(self, unicode):
        """将十进制 unicode 转换为 utf8 编码的字符

        :param unicode:
        :return:
        """
        return chr(unicode)

    def test_deprecated(self):
        self.assertWarns(DeprecationWarning, char_utf8_to_unicode, "a")
        self.assertWarns(DeprecationWarning, self.unicode_to_utf8_char, 97)

    def test_url2cn(self):
        url = "https://translate.google.com/?source=gtx&sl=auto&tl=en&text=%E6%9C%BA%E8%BA%AB%E8%B4%B4%E7%9D%80%E5%9C%B0%E9%9D%A2&op=translate"
        self.assertEqual(url2cn(url), "https://translate.google.com/?source=gtx&sl=auto&tl=en&text=机身贴着地面&op=translate")

    def test_group_by(self):
        group = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.assertListEqual(list(group_by(group, 2)), [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12)])
        self.assertListEqual(list(group_by(group, 3)), [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)])
        self.assertListEqual(list(group_by(group, 4)), [(1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12)])
        self.assertListEqual(list(group_by(group, 6)), [(1, 2, 3, 4, 5, 6), (7, 8, 9, 10, 11, 12)])
        self.assertRaises(ValueError, group_by, group, 7)

    def test_path(self):
        self.assertTrue(path_not_exist(""))
        # self.assertTrue(path_not_exist(None))

    def test_dict(self):
        dic = {
            "1": {
                "2": {
                    "3": "c"
                },
                "4": "d",
            },
            "5": "e"
        }
        self.assertEqual(get_with_chained_keys(dic, ["1", "2", "3"]), "c")
        self.assertEqual(get_with_chained_keys(dic, ["1", "4"]), "d")
        self.assertEqual(get_with_chained_keys(dic, ["5"]), "e")
        self.assertIsNone(get_with_chained_keys(dic, []))
        self.assertEqual(get_with_chained_keys(dic, ["1", "3"], "NULL"), "NULL")

        sub_dic = {
            "6": "f",
            "1": {
                "7": "g",
                "2": "b"
            }
        }
        exp_dic = {
            "1": {
                "2": "b",
                "4": "d",
                "7": "g",
            },
            "5": "e",
            "6": "f"
        }
        append_dic(dic, sub_dic)
        self.assertDictEqual(dic, exp_dic)

    def test_log_dir(self):
        self.assertIsNotNone(get_log_dir())


if __name__ == '__main__':
    unittest.main()
