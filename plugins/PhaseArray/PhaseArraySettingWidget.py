from  .designs import Ui_PhaseArraySettingWidget
from business.SettingDialog import SettingContentWidget

class PhaseArraySettingWidget(SettingContentWidget):

    def __init__(self,PhasePlugin,parent=None):
        super().__init__(parent)
        ui = Ui_PhaseArraySettingWidget()
        ui.setupUi(self)