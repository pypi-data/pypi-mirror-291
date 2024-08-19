# -*- coding:utf-8 -*-

"""
 - **Author: BL_30G** (https://space.bilibili.com/1654383134)
 - **Version: 0.7.6**
 - **Installation requirements: No dependencies packages** (csv_to_lst_or_dic() function depends on pandas library)
 - **Python Version：3.7 and above**
"""

from .advanced_list_MAIN import __advanced_list__


class advanced_list(__advanced_list__):
    """
    This class inherits all the features of list !

    Parameters:\n
    args: The value you want to assign a value to a list\n

    KeyWords:\n
    auto_replenishment (bool)\n
    use_type (bool)\n
    (If the use_type is not True, the type parameter is invalid.)\n
    type [type1, type2..., typeN]\n
    ignore_error (bool)\n
    no_prompt (bool)\n
    lock_all (bool)\n
    writable (bool)
    """

    def copy(self) -> 'advanced_list':
        """
        Return a shallow copy of the advanced_list.
        :return:
        """
        self._copy_self = super().copy()
        self._copy_self = __advanced_list__(self._copy_self,
                                            auto_replenishment=self.auto_replenishment,
                                            use_type=self.use_type, type=self.type_lst,
                                            ignore_error=self.ignore_error,
                                            no_prompt=self.no_prompt,
                                            writable=self.writable,
                                            lock_all=self.lock_all)
        self._tmp_lock_lst = self.view_lock_list()
        if not self.lock_all:
            for self._i in range(len(self._tmp_lock_lst)):
                self._copy_self.lock(self._tmp_lock_lst.__getitem__(self._i))
        return advanced_list(self._copy_self)


def get_type_lst(lst):
    """
    Get the types of elements in this list
    :param lst:
    :return:
    """
    if not isinstance(lst, list):
        return [type(lst)]

    result_lst: list = []

    if len(lst) == 0:
        return [Any]

    for _i in range(len(lst)):
        if type(lst[_i]) is type:
            result_lst.append(lst[_i])
        else:
            result_lst.append(type(lst[_i]))
    return list(set(result_lst))


class type_list(list):

    @staticmethod
    def __get_type_lst(lst) -> list:
        """
        Get the types of elements in this list
        :param lst:
        :return:
        """
        if not isinstance(lst, list):
            return [type(lst)]

        result_lst: list = []

        if len(lst) == 0:
            return [Any]

        for _i in range(len(lst)):
            if type(lst[_i]) is type:
                result_lst.append(lst[_i])
            else:
                result_lst.append(type(lst[_i]))
        return list(set(result_lst))

    def _check(self) -> None:
        self._i2: int = 0
        try:
            for self._i in range(0, len(self)):
                if type(self[self._i2]) not in self.type_lst:
                    self.remove(self[self._i2])
                    self._i2 -= 1
                self._i2 += 1
        except IndexError:
            pass

    def __init__(self, *args, **kwargs):
        """

         - THIS CLASS IS SCRAPPED!!!!!!!!!!

        This class inherits all the features of list !\n
        :param args: The value you want to assign a value to a list
        :param kwargs: REMEMBER Just only four parameters named 'type', 'retain(bool)', 'ignore_error(bool)' and 'no_prompt(bool)'
        :keyword type [type1, type2..., typeN]
        :keyword ignore_error (bool)
        :keyword no_prompt (bool)
        :keyword retain (bool)
        """
        self._i = None
        self._type_dic = {}
        self.type_lst = []
        self.ignore_error: bool = bool(kwargs.get("ignore_error"))
        self.no_prompt: bool = bool(kwargs.get("no_prompt"))
        self.retain: bool = False
        if kwargs.get("retain"):
            self.retain = True
        _t = kwargs.get("type")
        self._None_t = False
        self._B_T_arg = False

        if args != () and len(args) == 1 and isinstance(list(args)[0], list):
            super().__init__(list(args)[0])
            self._B_T_arg = True
            self._T_arg = list(args)[0]
        else:
            super().__init__(args)

        if _t is None:
            self._None_t = True
        if isinstance(_t, list):
            if len(_t) > 0:
                for _i in range(len(_t)):
                    if not (type(_t[_i]) is type):
                        self._type_dic[_i] = type(_t[_i])
                    else:
                        self._type_dic[_i] = _t[_i]
            else:
                self._type_dic[0] = Any
        else:
            if self._B_T_arg:
                self.type_lst = self.__get_type_lst(self._T_arg)
            else:
                self.type_lst = self.__get_type_lst(list(args))
        if not self._None_t:
            for _i in range(len(self._type_dic)):
                self.type_lst.append(self._type_dic[_i])

        if not self.retain:
            self._check()

    def type(self, _t):
        if _t is None:
            _t = self
        self.type_lst = self.__get_type_lst(_t)

        if not self.retain:
            self._check()

    def __class_getitem__(cls, item):
        """
        Only use for define function\n
        for example:\n
        def func() -> type_list[type1, type2, ..., typeN]: pass
        """
        pass

    def __setitem__(self, index, value):
        if type(value) not in self.type_lst and self.type_lst != [Any]:
            if not self.ignore_error:
                raise TypeError(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(value)}, type of value: {type(value)}, method: __setitem__")
            elif self.ignore_error and not self.no_prompt:
                print(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(value)}, type of value: {type(value)}, method: __setitem__")
            elif self.ignore_error and self.no_prompt:
                pass
        else:
            super().__setitem__(index, value)

    def append(self, item):
        if type(item) not in self.type_lst and self.type_lst != [Any]:
            if not self.ignore_error:
                raise TypeError(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(item)}, type of value: {type(item)}, method: append")
            elif self.ignore_error and not self.no_prompt:
                print(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(item)}, type of value: {type(item)}, method: append")
            elif self.ignore_error and self.no_prompt:
                pass
        else:
            super().append(item)

    def extend(self, iterable):
        if type(iterable) not in self.type_lst and self.type_lst != [Any]:
            if not self.ignore_error:
                raise TypeError(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(iterable)}, type of value: {type(iterable)}, method: extend")
            elif self.ignore_error and not self.no_prompt:
                print(
                    f"The types of elements in this list is: {self.type_lst}, The value you want to change: {repr(iterable)}, type of value: {type(iterable)}, method: extend")
            elif self.ignore_error and self.no_prompt:
                pass
        else:
            super().extend(iterable)


def tidy_up_list(lst, bool_mode=False, eval_mode=False, float_mode=False, int_mode=False, none_mode=False):
    """
    A function to tidy up list(●ˇ∀ˇ●)

    :param float_mode:
    :param int_mode:
    :param none_mode:
    :param bool_mode: If you want to turn such as 'True' into True which it is in this list, you can turn on 'bool_mode' (～￣▽￣)～
    :param eval_mode: If you want to turn such as '[]' into [] which it is in this list, you can turn on 'eval_mode' (￣◡￣)
    :param lst:put list which you need to sorting and clean（￣︶￣）
    :return: the perfect list  ( ´◡` )
    """


def deeply_tidy_up_list(lst):
    """
    This Function can search list elements and tidy up it too(‾◡‾)

    :param lst:put list which you need to sorting and clean（￣︶￣）
    :return: the perfect list  ( ´◡` )
    """


def bubble_sort(lst, if_round=False, in_reverse_order=False):
    """
    A simple bubble sort function ~(￣▽￣)~*\n

    :param lst: The list you need to sort
    :param if_round: Rounding floating-point numbers
    :param in_reverse_order: Reverse the list
    :return: The sorted list
    """


def list_calculation(*args, calculation="+", multi_calculation="", nesting=False):
    """
    The function for perform calculation on multiple lists
    :param args: The lists to calculation
    :param calculation: An calculation symbol used between all lists (Only one)(default:"+")(such as "+", "-", "*", "/", "//", "%")
    :param multi_calculation: Different calculation symbols between many lists (Use ',' for intervals)
    :param nesting: If the lists you want to calculation are in a list, You should turn on 'nesting' to clean the nesting list
    :return: The result of lists
    """


def var_in_list(lst, __class, return_lst=False, only_return_lst=False):
    """
    Returns the number of variables in the list that match the type given by the user
    :param lst: The list
    :param __class: The class of variable you want to find
    :param return_lst: Returns a list of variables that match the type
    :param only_return_lst: Only returns a list of variables that match the type
    :return:
    """


def in_list_calculation(lst, calculation="+", multi_calculation=""):
    """
    A function to calculation all the int or float in the list
    :param lst: The list
    :param calculation: An calculation symbol used between all lists (Only one)(default:"+")(such as "+", "-", "*", "/", "//", "%")
    :param multi_calculation: Different calculation symbols between many lists (Use ',' for intervals)
    :return:
    """


def csv_to_lst_or_dic(csv, dict_mode=False):
    """
    Can turn csv you read into list or dict
    :param csv:
    :param dict_mode: turn csv you read into dict
    :return:
    """


def len_sorted_lst(lst, reverse=False, filtration=True):
    """
    This function according to the len of list to sort the lists(From small to large)
    :param lst:
    :param reverse: If is true the order will reverse
    :param filtration: If is true it will clear the type of variable isn't list(these variable will append at the lists right)
    :return:
    """


def populate_lsts(*args, _type=0, nesting=False):
    """
    This function will populate the list with less than the longest list length according to the length of the list until the longest list length is met
    :param _type: the thing you want to populate
    :param nesting: If the lists you want to populate are in a list, You should turn on 'nesting' to clean the nesting list
    :return:
    """


def list_internal_situation(lst):
    """
     This function will print all variable in the list
    :param lst:
    :return:
    """


def get_variable(value) -> list:
    """
    A function to get the name of variable
    :param value: the value of variable
    :return: the name of variable
    """


def index_len(__obj) -> int:
    """
    Return the number of items in a container(= len(__obj)-1)
    :param __obj
    :return
    """


# str functions area
def replace_str(string, __c, __nc='', num=0, __start=0, __end=None):
    # This Function is Finished!
    """
    Change the character in the string to a new character, but unlike "str.replace()", num specifies the number of original strs that that need to change (not the maximum times of changes)
    :param string: The string
    :param __c: Original character
    :param __nc: New character
    :param num: How many character(default is Zero(replace all Eligible character))
    :param __start:
    :param __end:
    :return:
    """


def reverse_str(string):
    """
    A very, very easy function to reverse str（混水分
    :param string: The string you want to reverse
    :return: the reversed str
    """


def statistics_str(string):
    """
    Return the statistics of the string,
    include the sort of the character according to ASCII Table and the appeared numbers of the character in this string
    :param string: The string you need statistics
    :return: The statistics of the string
    """


def find_list(lst, __fc, start=False, mid=False, end=False):
    """
    Based on the string given by the user, find the string that contains this string in the list.
    :param lst: The list you want to find
    :param __fc: The character in list in string
    :param start: Only find on list start
    :param mid: Only find on list middle
    :param end: Only find on list end
    :return: List of find result
    """


# bool area
def can_variable(string):
    """
    The function can judge the string can or cannot be variable
    :param string:
    :return:
    """
    import gc

    string = str(string)
    judgment_lst = ["False", "None", "True", "and", "as", "assert", "break", "case", "class", "continue", "def", "del",
                    "elif",
                    "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda",
                    "match", "nonlocal", "not", "or",
                    "pass", "raise", "return", "try", "while", "with", "yield"]
    C_variable: bool = True

    if string in judgment_lst:
        C_variable = False
    elif not string.isalpha():
        C_variable = False
    elif 48 <= ord(string[0:]) <= 57:
        C_variable = False

    del judgment_lst
    gc.collect()
    return C_variable


from .list_func_part import *
from .str_func_part import *
