import unittest
import waveforms

class TestWaveforms(unittest.TestCase):

    def test_CV(self):
        
        first_case = waveforms.CV(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.001, sr = 0.1, ns  = 1)
        second_case = waveforms.CV(Eini = -0.5, Eupp = 0.5, Elow = -0.5, dE = 0.001, sr = 0.1, ns  = 1)
        third_case = waveforms.CV(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.005, sr = 0.1, ns  = 1)
        fourth_case = waveforms.CV(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.001, sr = 0.2, ns  = 3)

        fifth_case = waveforms.CV(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.001, sr = 0.1, ns  = 1)
        sixth_case = waveforms.CV(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.001, sr = 0.1, ns  = 1)
        seventh_case = waveforms.CV(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.001, sr = 0.1, ns  = 1)
        eighth_case = waveforms.CV(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.001, sr = 0.1, ns  = 1)

        ninth = waveforms.CV(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.001, sr = 0.1, ns  = 1)
        tenth_case = waveforms.CV(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.001, sr = 0.1, ns  = 1)
        eleventh_case = waveforms.CV(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.001, sr = 0.1, ns  = 1)
        twelfth_case = waveforms.CV(Eini = 0.0, Eupp = 0.5, Elow = 0.0, dE = 0.001, sr = 0.1, ns  = 1)
        
        self.assertEqual