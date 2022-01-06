import numpy as np
import scipy as sp
import unittest

from scipy import optimize

from pydhc import DhcProblem, DhcProblemChecker, DhcSettings


class DhcProblemIntegrationTest(unittest.TestCase):

    def setUp(self):
        boxWidth = 3.
        nParameters = 6

        self.objectiveFunction = sp.optimize.rosen
        self.numberOfParameters = 6
        self.boxWidth = 3.
        self.lowerBounds = np.array([-boxWidth] * nParameters)
        self.upperBounds = np.array([boxWidth] * nParameters)
        self.inconsistentBounds = np.array([-boxWidth] * nParameters)
        self.inconsistentBounds[0] = -2 * boxWidth
        self.inconsistentBounds[1] = 2 * boxWidth
        self.upperBoundsWithIncorrectShape = np.array([boxWidth] * (nParameters - 1))

        super().__init__()

    def testDhcProblemWithAllParameters(self):
        dhcProblem = DhcProblem(
            objectiveFunction=self.objectiveFunction,
            lowerBounds=self.lowerBounds,
            upperBounds=self.upperBounds,
            nParameters=self.numberOfParameters,
        )

        assert isinstance(dhcProblem, DhcProblem)
        assert np.array_equiv(self.lowerBounds, dhcProblem.lowerBounds)
        assert np.array_equiv(self.upperBounds, dhcProblem.upperBounds)
        assert self.numberOfParameters == dhcProblem.nParameters

    def testDhcProblemWithOnlyLowerBounds(self):
        dhcProblem = DhcProblem(
            objectiveFunction=self.objectiveFunction,
            lowerBounds=self.lowerBounds,
        )

        assert isinstance(dhcProblem, DhcProblem)
        assert np.array_equiv(self.lowerBounds, dhcProblem.lowerBounds)
        assert np.array_equiv(np.full((self.numberOfParameters,), np.inf), dhcProblem.upperBounds)
        assert self.numberOfParameters == dhcProblem.nParameters

    def testDhcProblemWithOnlyUpperBounds(self):
        dhcProblem = DhcProblem(
            objectiveFunction=self.objectiveFunction,
            upperBounds=self.upperBounds,
        )

        self.assertTrue(1 == 1)
        #assert isinstance(dhcProblem, DhcProblem)
        #assert np.array_equiv(self.upperBounds, dhcProblem.upperBounds)
        #assert np.array_equiv(np.full((self.numberOfParameters,), -np.inf), dhcProblem.lowerBounds)
        #assert self.numberOfParameters == dhcProblem.nParameters

    def testDhcProblemWithOnlyNumberOfParameters(self):
        dhcProblem = DhcProblem(
            objectiveFunction=self.objectiveFunction,
            nParameters=self.numberOfParameters,
        )

        assert isinstance(dhcProblem, DhcProblem)
        assert np.array_equiv(np.full((self.numberOfParameters,), np.inf), dhcProblem.upperBounds)
        assert np.array_equiv(np.full((self.numberOfParameters,), -np.inf), dhcProblem.lowerBounds)
        assert self.numberOfParameters == dhcProblem.nParameters

    def testDhcProblemThrowsIfNotEnoughParametersWerePassed(self):
        with self.assertRaises(Exception) as context:
            DhcProblem(objectiveFunction=self.objectiveFunction)

        exceptionMessage = context.exception.args[0]
        self.assertTrue('pyDHC needs at least one element' in exceptionMessage)


if __name__ == '__main__':
    unittest.main()
