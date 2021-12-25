import numpy as np
import logging
from typing import Callable

logger = logging.getLogger('Mary9ProblemLogger')


class DhcProblem:

    def __init__(
            self,
            objectiveFunction: Callable,
            lowerBounds: np.ndarray = None,
            upperBounds: np.ndarray = None,
            nParameters: int = None,
    ):
        self.objective_function = objectiveFunction
        if lowerBounds is not None:
            self.lowerBounds = np.array(lowerBounds)
        if upperBounds is not None:
            self.upperBounds = np.array(upperBounds)
        if nParameters is not None:
            self.nParameters = int(nParameters)
        DhcProblemValidator.check_consistency(self)


class DhcProblemValidator:
    @staticmethod
    def check_consistency(dhcProblem):
        DhcProblemValidator.checkObjectiveFunction(dhcProblem)
        DhcProblemValidator.checkProblemSize(dhcProblem)
        DhcProblemValidator.checkConsistencyOfBounds(dhcProblem)

    @staticmethod
    def checkObjectiveFunction(dhcProblem):
        if not isinstance(dhcProblem.objective_function, Callable):
            raise TypeError("pyDHC needs an objective function to work with.")

    @staticmethod
    def checkProblemSize(dhcProblem):

        lowerBoundSet = dhcProblem.lowerBounds is None
        upperBoundSet = dhcProblem.upperBounds is None
        noBoundsSet = lowerBoundSet and upperBoundSet

        if noBoundsSet and dhcProblem.nParameters is None:
            raise AssertionError(
                "Mary9 can not create a misc without either lower bounds,"
                "or upper bounds, or a a misc size, i.e., n_parameters."
            )
        DhcProblemValidator.assertProblemSizeConsistency(
            dhcProblem, lowerBoundSet, upperBoundSet
        )

    @staticmethod
    def assertProblemSizeConsistency(
            problem: DhcProblem,
            lower_bound_set: bool,
            upper_bound_set: bool
    ):
        if lower_bound_set and upper_bound_set:
            if len(problem.lowerBounds) != len(problem.upperBounds):
                raise AssertionError("Upper and lower bounds needs to have "
                                     "the same length.")
        elif lower_bound_set:
            problem.upperBounds = np.full(len(problem.lowerBounds), np.inf)
        elif upper_bound_set:
            problem.lowerBounds = np.full(len(problem.upperBounds), -np.inf)
        else:
            problem.lowerBounds = np.full(problem.nParameters, -np.inf)
            problem.upperBounds = np.full(problem.nParameters, np.inf)
        if problem.nParameters is None:
            problem.nParameters = len(problem.lowerBounds)
        else:
            if len(problem.lowerBounds) != problem.nParameters:
                raise AssertionError("Length of bounds needs to match the "
                                     "number of free parameters.")

    @staticmethod
    def checkConsistencyOfBounds(problem: DhcProblem):
        problem.upperBounds = np.array([
            checkAndAdaptBoundPerParameter(
                problem.lowerBounds[iPar],
                problem.upperBounds[iPar],
                iPar
            ) for iPar in range(problem.nParameters)
        ])


def checkAndAdaptBoundPerParameter(lowerBounds, upperBounds, iPar):
    if lowerBounds[iPar] > upperBounds[iPar]:
        logger.warning(
            f'Lower bound for parameter index {iPar} greater than upper bound. '
            f'Adjusting upper bound to match lower bound.'
        )
        upperBounds[iPar] = lowerBounds[iPar]
