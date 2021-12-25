from .problem import DhcProblem


class DhcSettings:

    def __init__(
            self,
            minStepSize: float = 1e-10,
            nMaxSteps: int = None,
            dhcProblem: DhcProblem = None,
    ):
        self.minStepSize = minStepSize
        self.nMaxSteps = nMaxSteps
        if nMaxSteps is None:
            self.nMaxSteps = 20000
            if dhcProblem is not None:
                self.nMaxSteps = 5000 * dhcProblem.nParameters
