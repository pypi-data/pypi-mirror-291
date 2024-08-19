"""、

Fluent设计的tkinter组件库（模板）

-------------
作者：XiangQinxi
-------------
"""

from .badge import FluBadge
from .button import FluButton
from .entry import FluEntry
from .frame import FluFrame
from .label import FluLabel
from .menu import FluMenu
from .menubar import FluMenuBar
from .popupmenu import FluPopupMenu
from .text import FluText
from .thememanager import FluThemeManager
from .togglebutton import FluToggleButton
from .toplevel import FluToplevel
from .window import FluWindow
#from .winico import FluWinico


FluChip = FluBadge
FluPushButton = FluButton
FluTextInput = FluEntry
FluTextBox = FluText
FluPanel = FluFrame
FluMainWindow = FluWindow
FluSubWindow = FluToplevel

# 