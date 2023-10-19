from ctrl.ctrl import Ctrl
from ctrl.ctrl import CtrlError, CtrlModuleError
from ctrl.gen  import HcGen


class HcCtrl(Ctrl):
    """
    Coin hopper control class.
    """
    def __init__(self, logger, ctrl_info=None):
        super().__init__(logger, ctrl_info)

    def verify_model(self):
        if not isinstance(self.model, HcGen) and not issubclass(self.model.__class__, HcGen):
            msg = "unknown support library specification in {0}".format(self.model)
            raise CtrlModuleError(msg)

    def dispense(self, quantity):
        """Dispenses a quantity of coins"""
        self.logger.debug("asking the coin-hooper to dispense {0} coins".format(quantity))
        self.model.dispense(quantity)
