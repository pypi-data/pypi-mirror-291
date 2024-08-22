import easygui as eg


功能演示=eg.egdemo

def 提示框(提示文字='这是个提示框弹窗', 窗口标题=' ', 按钮文字='确定', 图片=None):
    """只有一个确定按钮 msgbox , 返回按钮文字,不选返回空None (图片仅支持gif和png,点击返回图片路径)"""
    return eg.msgbox(msg=提示文字, title=窗口标题, ok_button=按钮文字, image=图片, root=None)

def 双按钮提示框(提示文字='这是两个按钮的提示框弹窗', 窗口标题=' ', 按钮文字=('确定','取消'), 图片=None):
    """两个按钮 , 返回真或假, 都不选返回空None"""
    return eg.ccbox(msg=提示文字, title=窗口标题, choices=按钮文字, image=图片)

def 多按钮提示框_返序(提示文字='这是多个按钮的提示框弹窗, 返回序号0或1,2...', 窗口标题=' ', 按钮文字=('确定','取消','按钮3'), 图片=None):
    """多个按钮, 返回序号0或1,2..."""
    return eg.indexbox(msg=提示文字, title=窗口标题, choices=按钮文字, image=图片)

def 多按钮提示框(提示文字='这是多个按钮的提示框弹窗, 返回按钮文字', 窗口标题=' ', 按钮文字=('按钮1','按钮2','按钮3'), 图片=None):
    """多个按钮 , 返回按钮文字"""
    return eg.buttonbox(msg=提示文字, title=窗口标题, choices=按钮文字, image=图片)

def 列表选择框(提示文字='列表选择窗口,返回选中的文字', 窗口标题=' ', 列表文字=('文字1','文字2','文字3'), 默认选中=0):
    """在列表文字中选择, 返回选择的列表文字内容"""
    return eg.choicebox(msg=提示文字, title=窗口标题, choices=列表文字, preselect=默认选中)

def 列表选择框_可多选(提示文字='列表选择窗口,返回选中的列表文字构成的列表', 窗口标题=' ', 列表文字=('文字1','文字2','文字3'), 默认选中=0):
    """在列表文字中选择, 返回选择的列表文字构成的列表"""
    return eg.multchoicebox(msg=提示文字, title=窗口标题, choices=列表文字, preselect=默认选中)

def 输入框(提示文字='输入框,返回输入的文字,默认去空格', 窗口标题=' ', 默认输入='', 是否去空格=True, 图片=None):
    """输入框,返回输入的文字,默认去空格 取消返回空None"""
    return eg.enterbox(msg=提示文字, title=窗口标题, default=默认输入, strip=是否去空格, image=图片, root=None)

def 密码输入框(提示文字='密码输入框,返回输入的文字', 窗口标题=' ', 默认输入='', 图片=None):
    """密码输入框(显示*号),返回输入的文字 取消返回空None"""
    return eg.passwordbox(msg=提示文字, title=窗口标题, default=默认输入,  image=图片, root=None)

def 范围整数输入框(提示文字='限制大小范围整数输入框,返回输入的数值', 窗口标题=' ', 默认输入=None, 最小值=0,最大值=99, 图片=None):
    """限制大小范围整数输入框,返回输入的整数, 输入的不是整数或不在范围内会提示"""
    return eg.integerbox(msg=提示文字, title=窗口标题, default=默认输入, lowerbound=最小值, upperbound=最大值, image=图片, root=None)

def 多项目输入框(提示文字='多项目输入框, 返回列表', 窗口标题=' ', 项目名称=['项目名1','项目名2'],默认值=None):
    """多项目输入框, 返回输入内容构成的列表,(默认值如果输入,需要和项目名称个数对应)"""
    return eg.multenterbox(提示文字, title=窗口标题, fields=项目名称, values=默认值)

def 多项目带密码输入框(提示文字='多项目带密码输入框(最后一个是密码输入框), 返回列表', 窗口标题=' ', 项目名称=['项目名1','项目名2'],默认值=None):
    return eg.multpasswordbox(提示文字, title=窗口标题, fields=项目名称, values=默认值)

def 长文本显示输入框(提示文字='长文本显示输入框,可以显示长文本,也可以接受带换行的大段文字输入', 窗口标题=' ', 默认显示文本='',单行限80字=True):
    return eg.textbox(msg=提示文字, title=窗口标题, text=默认显示文本, codebox=单行限80字)

def 选择文件需要保存的路径(提示文字='', 窗口标题='另存为',默认=None,文件类型=None):
    '''提供一个对话框，让用于选择文件需要保存的路径（带完整路径），如果用户选择 “Cancel” 则返回 None。

    默认default 参数应该包含一个文件名（例如当前需要保存的文件名），当然也可以设置为空的，或者包含一个文件格式掩码的通配符。\n
    关于 文件类型filetypes 参数的设置方法：\n
    可以是包含文件掩码的字符串列表，例如：文件类型 = ["*.txt"]\n
    可以是字符串列表，列表的最后一项字符串是文件类型的描述，例如：文件类型 = ["*.css", ["*.htm", "*.html", "HTML文件"]]
    '''
    return eg.filesavebox(msg=提示文字, title=窗口标题, default=默认, filetypes=文件类型)

def 选择电脑上的文件夹(提示文字='', 窗口标题='请选择一个文件夹(目录)',默认=None):
    return eg.diropenbox(msg=提示文字, title=窗口标题, default=默认)

def 返回用户选择的文件名(提示文字='', 窗口标题='请选择一个文件',默认='*',文件类型=None, 多选=False):
    '''返回用户选择的文件名（带完整路径），如果用户选择 “Cancel” 则返回 None。

    关于 默认default 参数的设置方法：\n
    默认default 参数指定一个默认路径，通常包含一个或多个通配符。默认的参数是 '*'，即匹配所有文件。\n
    例如：
    默认="c:/fishc/*.py" 即显示 C:\fishc 文件夹下所有的 Python 文件。\n
    默认="c:/fishc/test*.py" 即显示 C:\fishc 文件夹下所有的名字以 test 开头的 Python 文件。

    关于 文件类型filetypes 参数的设置方法：\n
    可以是包含文件掩码的字符串列表，例如：文件类型 = ["*.txt"]\n
    可以是字符串列表，列表的最后一项字符串是文件类型的描述，例如：文件类型 = ["*.css", ["*.htm", "*.html", "HTML文件"]]
    '''
    return eg.fileopenbox(msg=提示文字, title=窗口标题, default=默认, filetypes=文件类型, multiple=多选)

def 捕获异常(提示文字=None, 窗口标题=None):
    '''
    当异常出现的时候，exceptionbox() 会将堆栈追踪显示在一个 codebox() 中，并且允许你做进一步的处理。
    例如:\n
    try:\n
        打印(1+'a') # 这里会产生异常\n
    except:\n
            exceptionbox()\n
    '''
    eg.exceptionbox(msg=提示文字, title=窗口标题)

import errno
import os
import pickle
import datetime

class EgStore(object):
    """
    支持持久存储的类。

    您可以使用``EgStore``来支持存储和检索EasyGui应用程序的用户设置。

    **首先：定义一个类,例如“数据存储器”，继承自EgStore类
    class 数据存储器(EgStore):
        def __init__(self, 文件名):  # 需要指定文件名
            # 指定要记住的属性名称
            self.bl作者 = ""
            self.bl书籍 = ""
            # 必须执行下面两个语句
            self.filename = 文件名
            self.恢复()
    *第二步：创建持久设置对象** ::
        bl存储器实例 = 数据存储器("settings.txt")

    *运行中存储数据：
        bl作者 = "郭老师"
        bl书籍 = "《青少年中文编程入门》"
        # 将上面两个变量的值保存到“settings”对象中
        bl存储器实例.bl作者 = bl作者
        bl存储器实例.bl书籍 = bl书籍
        bl存储器实例.保存()

    **下次打开恢复数据:
        if os.path.exists("settings.txt"):
            settings.恢复()
            打印(bl存储器实例.bl作者,bl存储器实例.bl书籍)
            <<< 郭老师 《青少年中文编程入门》
    """

    def __init__(self, 文件名):
        """使用给定的文件名初始化存储。
        """

        self.filename = 文件名

    def 恢复(self):
        try:
            self._restore()
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise


    def _restore(self):
        with open(self.filename, 'rb') as f:
            store = pickle.load(f)

        for key, value in store.__dict__.items():
            self.__dict__[key] = value

        self.last_time_restored = datetime.datetime.now()


    def 保存(self):
        """Save this store to a pickle file.
        All directories in :attr:`filename` must already exist.
        """

        with open(self.filename, 'wb') as f:
            self.last_time_stored = datetime.datetime.now()
            pickle.dump(self, f)


    def 删除(self):
        """Delete this store's file if it exists."""

        if os.path.isfile(self.filename):
            os.remove(self.filename)

    def __getstate__(self):
        """ All attributes will be pickled """
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        """ Ensure filename won't be unpickled """
        if 'filename' in state:
            del state['filename']
        self.__dict__.update(state)

    def __str__(self):
        """"Format this store as "key : value" pairs, one per line."""
        stored_values = self.__dict__
        lines = []
        width = max(len(key) for key in stored_values)
        for key in sorted(stored_values.keys()):
            value = stored_values[key]
            if isinstance(value, datetime.datetime):
                value = value.isoformat()
            lines.append('{0} : {1!r}'.format(key.ljust(width), value))
        return '\n'.join(lines)

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.filename)

if __name__ == '__main__':
    长文本显示输入框()
    pass