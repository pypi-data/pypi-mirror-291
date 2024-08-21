from PyQt5.QtCore import QSettings
import platform

"""
    This is where Stec QObject are kept, this are not QWidgets
"""
class VSettings(QSettings):
    """
    Used to save setup data
    """
    def __init__(self, project : str = "stec-general"):
        """
        :param project:   default is "stec-opc" Should be the Project you or instance of the Project
        """
        super().__init__( project, QSettings.IniFormat)


class RetensionSettings(QSettings):

    def __init__(self, project: str = "stdcomQt.ResidentSubscriber"):
        """
        :param project:   default is "stec-opc" Should be the Project you or instance of the Project
        """
        if platform.system().upper() == 'WINDOWS':
            super().__init__('C:/S-Tec/StecConfig/' + project, QSettings.IniFormat)
        else:
            super().__init__(project, QSettings.IniFormat)

    def SaveResidentData(self, name : str, data):
        self.setValue(name, data)

    def GetResidentData(self, name : str , data : [] = None ) :
        if data is None:
            data = []

        data = self.value(name, data)
        if data is None or len(data) == 0:
            return None
        return data

