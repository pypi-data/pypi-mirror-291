# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
import os

from qtpy.QtDesigner import QDesignerCustomWidgetInterface
from qtpy.QtGui import QIcon

import bec_widgets
from bec_widgets.widgets.position_indicator.position_indicator import PositionIndicator

DOM_XML = """
<ui language='c++'>
    <widget class='PositionIndicator' name='position_indicator'>
    </widget>
</ui>
"""

MODULE_PATH = os.path.dirname(bec_widgets.__file__)


class PositionIndicatorPlugin(QDesignerCustomWidgetInterface):  # pragma: no cover
    def __init__(self):
        super().__init__()
        self._form_editor = None

    def createWidget(self, parent):
        t = PositionIndicator(parent)
        return t

    def domXml(self):
        return DOM_XML

    def group(self):
        return "BEC Utils"

    def icon(self):
        icon_path = os.path.join(MODULE_PATH, "assets", "designer_icons", "position_indicator.png")
        return QIcon(icon_path)

    def includeFile(self):
        return "position_indicator"

    def initialize(self, form_editor):
        self._form_editor = form_editor

    def isContainer(self):
        return False

    def isInitialized(self):
        return self._form_editor is not None

    def name(self):
        return "PositionIndicator"

    def toolTip(self):
        return "PositionIndicator"

    def whatsThis(self):
        return self.toolTip()
