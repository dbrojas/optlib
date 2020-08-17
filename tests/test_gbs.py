import unittest
import logging

from optlib.gbs import (
    _psi,
    _phi,
    _cbnd,
    _bjerksund_stensland_1993,
    _bjerksund_stensland_2002,
    _american_option,
    _gbs,
    _approx_implied_vol,
    _gbs_implied_vol,
    _american_implied_vol,
    merton,
    black_76,
    garman_kohlhagen,
    black_scholes,
    kirks_76,
    asian_76
)

logging.basicConfig(
    format="[%(asctime)s %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)


def assert_close(a, b, prec=.000001):
    """This function tests that two floating point numbers are the same.

    Numbers less than 1 million are considered the same if they are within .000001 of each other
    Numbers larger than 1 million are considered the same if they are within .0001% of each other
    User can override the default precision if necessary
    """

    if (a < 1000000.0) and (b < 1000000.0):
        d = abs(a - b)
        d_type = "Difference"
    else:
        d = abs((a - b) / a)
        d_type = "Percent Difference"

    logging.debug("Comparing {0} and {1}. Difference is {2}, Difference Type is {3}".format(a, b, d, d_type))

    result = True if d < prec else False
    if (__name__ == "__main__") and (result is False):
        raise AssertionError("FAILED TEST. Comparing {0} and {1}. Difference is {2}, Difference Type is {3}".format(a, b, d, d_type))

    return result


class TestGBS(unittest.TestCase):

    def test_american_option_intermediate_calc(self):

        # ---------------------------
        # unit tests for _psi()
        # _psi(FS, t2, gamma, H, I2, I1, t1, r, b, V):
        logging.info("Testing _psi (American Option Intermediate Calculation)")
        assert_close(_psi(fs=120, t2=3, gamma=1, h=375, i2=375, i1=300, t1=1, r=.05, b=0.03, v=0.1), 112.87159814023171)
        assert_close(_psi(fs=125, t2=2, gamma=1, h=100, i2=100, i1=75, t1=1, r=.05, b=0.03, v=0.1), 1.7805459905819128)

        # ---------------------------
        # unit tests for _phi()
        logging.info("Testing _phi (American Option Intermediate Calculation)")
        # _phi(FS, T, gamma, h, I, r, b, V):
        assert_close(_phi(fs=120, t=3, gamma=4.51339343051624, h=151.696096685711, i=151.696096685711, r=.02, b=-0.03, v=0.14),
                    1102886677.05955)
        assert_close(_phi(fs=125, t=3, gamma=1, h=374.061664206768, i=374.061664206768, r=.05, b=0.03, v=0.14),
                        117.714544103477)

        # ---------------------------
        # unit tests for _CBND
        logging.info("Testing _CBND (Cumulative Binomial Normal Distribution)")
        assert_close(_cbnd(0, 0, 0), 0.25)
        assert_close(_cbnd(0, 0, -0.5), 0.16666666666666669)
        assert_close(_cbnd(-0.5, 0, 0), 0.15426876936299347)
        assert_close(_cbnd(0, -0.5, 0), 0.15426876936299347)
        assert_close(_cbnd(0, -0.99999999, -0.99999999), 0.0)
        assert_close(_cbnd(0.000001, -0.99999999, -0.99999999), 0.0)

        assert_close(_cbnd(0, 0, 0.5), 0.3333333333333333)
        assert_close(_cbnd(0.5, 0, 0), 0.3457312306370065)
        assert_close(_cbnd(0, 0.5, 0), 0.3457312306370065)
        assert_close(_cbnd(0, 0.99999999, 0.99999999), 0.5)
        assert_close(_cbnd(0.000001, 0.99999999, 0.99999999), 0.5000003989422803)

    def test_american_options_testing(self):

        logging.info("Testing _Bjerksund_Stensland_2002()")
        # _american_option(option_type, X, FS, T, b, r, V)
        assert_close(_bjerksund_stensland_2002(fs=90, x=100, t=0.5, r=0.1, b=0, v=0.15)[0], 0.8099, prec=.001)
        assert_close(_bjerksund_stensland_2002(fs=100, x=100, t=0.5, r=0.1, b=0, v=0.25)[0], 6.7661, prec=.001)
        assert_close(_bjerksund_stensland_2002(fs=110, x=100, t=0.5, r=0.1, b=0, v=0.35)[0], 15.5137, prec=.001)

        assert_close(_bjerksund_stensland_2002(fs=100, x=90, t=0.5, r=.1, b=0, v=0.15)[0], 10.5400, prec=.001)
        assert_close(_bjerksund_stensland_2002(fs=100, x=100, t=0.5, r=.1, b=0, v=0.25)[0], 6.7661, prec=.001)
        assert_close(_bjerksund_stensland_2002(fs=100, x=110, t=0.5, r=.1, b=0, v=0.35)[0], 5.8374, prec=.001)

        logging.info("Testing _Bjerksund_Stensland_1993()")
        # Prices for 1993 model slightly different than those presented in Haug"s Complete Guide to Option Pricing Formulas
        # Possibly due to those results being based on older CBND calculation?
        assert_close(_bjerksund_stensland_1993(fs=90, x=100, t=0.5, r=0.1, b=0, v=0.15)[0], 0.8089, prec=.001)
        assert_close(_bjerksund_stensland_1993(fs=100, x=100, t=0.5, r=0.1, b=0, v=0.25)[0], 6.757, prec=.001)
        assert_close(_bjerksund_stensland_1993(fs=110, x=100, t=0.5, r=0.1, b=0, v=0.35)[0], 15.4998, prec=.001)

        logging.info("Testing _american_option()")
        assert_close(_american_option("p", fs=90, x=100, t=0.5, r=0.1, b=0, v=0.15)[0], 10.5400, prec=.001)
        assert_close(_american_option("p", fs=100, x=100, t=0.5, r=0.1, b=0, v=0.25)[0], 6.7661, prec=.001)
        assert_close(_american_option("p", fs=110, x=100, t=0.5, r=0.1, b=0, v=0.35)[0], 5.8374, prec=.001)

        assert_close(_american_option("c", fs=100, x=95, t=0.00273972602739726, r=0.000751040922831883, b=0, v=0.2)[0], 5.0, prec=.01)
        assert_close(_american_option("c", fs=42, x=40, t=0.75, r=0.04, b=-0.04, v=0.35)[0], 5.28, prec=.01)
        assert_close(_american_option("c", fs=90, x=100, t=0.1, r=0.10, b=0, v=0.15)[0], 0.02, prec=.01)

        logging.info("Testing that American valuation works for integer inputs")
        assert_close(_american_option("c", fs=100, x=100, t=1, r=0, b=0, v=0.35)[0], 13.892, prec=.001)
        assert_close(_american_option("p", fs=100, x=100, t=1, r=0, b=0, v=0.35)[0], 13.892, prec=.001)

        logging.info("Testing valuation works at minimum/maximum values for T")
        assert_close(_american_option("c", 100, 100, 0.00396825396825397, 0.000771332656950173, 0, 0.15)[0], 0.3769, prec=.001)
        assert_close(_american_option("p", 100, 100, 0.00396825396825397, 0.000771332656950173, 0, 0.15)[0], 0.3769, prec=.001)
        assert_close(_american_option("c", 100, 100, 100, 0.042033868311581, 0, 0.15)[0], 18.61206, prec=.001)
        assert_close(_american_option("p", 100, 100, 100, 0.042033868311581, 0, 0.15)[0], 18.61206, prec=.001)

        logging.info("Testing valuation works at minimum/maximum values for X")
        assert_close(_american_option("c", 100, 0.01, 1, 0.00330252458693489, 0, 0.15)[0], 99.99, prec=.001)
        assert_close(_american_option("p", 100, 0.01, 1, 0.00330252458693489, 0, 0.15)[0], 0, prec=.001)
        assert_close(_american_option("c", 100, 2147483248, 1, 0.00330252458693489, 0, 0.15)[0], 0, prec=.001)
        assert_close(_american_option("p", 100, 2147483248, 1, 0.00330252458693489, 0, 0.15)[0], 2147483148, prec=.001)

        logging.info("Testing valuation works at minimum/maximum values for F/S")
        assert_close(_american_option("c", 0.01, 100, 1, 0.00330252458693489, 0, 0.15)[0], 0, prec=.001)
        assert_close(_american_option("p", 0.01, 100, 1, 0.00330252458693489, 0, 0.15)[0], 99.99, prec=.001)
        assert_close(_american_option("c", 2147483248, 100, 1, 0.00330252458693489, 0, 0.15)[0], 2147483148, prec=.001)
        assert_close(_american_option("p", 2147483248, 100, 1, 0.00330252458693489, 0, 0.15)[0], 0, prec=.001)

        logging.info("Testing valuation works at minimum/maximum values for b")
        assert_close(_american_option("c", 100, 100, 1, 0, -1, 0.15)[0], 0.0, prec=.001)
        assert_close(_american_option("p", 100, 100, 1, 0, -1, 0.15)[0], 63.2121, prec=.001)
        assert_close(_american_option("c", 100, 100, 1, 0, 1, 0.15)[0], 171.8282, prec=.001)
        assert_close(_american_option("p", 100, 100, 1, 0, 1, 0.15)[0], 0.0, prec=.001)

        logging.info("Testing valuation works at minimum/maximum values for r")
        assert_close(_american_option("c", 100, 100, 1, -1, 0, 0.15)[0], 16.25133, prec=.001)
        assert_close(_american_option("p", 100, 100, 1, -1, 0, 0.15)[0], 16.25133, prec=.001)
        assert_close(_american_option("c", 100, 100, 1, 1, 0, 0.15)[0], 3.6014, prec=.001)
        assert_close(_american_option("p", 100, 100, 1, 1, 0, 0.15)[0], 3.6014, prec=.001)

        logging.info("Testing valuation works at minimum/maximum values for V")
        assert_close(_american_option("c", 100, 100, 1, 0.05, 0, 0.005)[0], 0.1916, prec=.001)
        assert_close(_american_option("p", 100, 100, 1, 0.05, 0, 0.005)[0], 0.1916, prec=.001)
        assert_close(_american_option("c", 100, 100, 1, 0.05, 0, 1)[0], 36.4860, prec=.001)
        assert_close(_american_option("p", 100, 100, 1, 0.05, 0, 1)[0], 36.4860, prec=.001)

    def test_generalized_black_scholes(self):

        logging.info("Testing GBS Premium")
        assert_close(_gbs("c", 100, 95, 0.00273972602739726, 0.000751040922831883, 0, 0.2)[0], 4.99998980469552)
        assert_close(_gbs("c", 92.45, 107.5, 0.0876712328767123, 0.00192960198828152, 0, 0.3)[0], 0.162619795863781)
        assert_close(_gbs("c", 93.0766666666667, 107.75, 0.164383561643836, 0.00266390125346286, 0, 0.2878)[0],
                    0.584588840095316)
        assert_close(_gbs("c", 93.5333333333333, 107.75, 0.249315068493151, 0.00319934651984034, 0, 0.2907)[0],
                    1.27026849732877)
        assert_close(_gbs("c", 93.8733333333333, 107.75, 0.331506849315069, 0.00350934592318849, 0, 0.2929)[0],
                    1.97015685523537)
        assert_close(_gbs("c", 94.1166666666667, 107.75, 0.416438356164384, 0.00367360967852615, 0, 0.2919)[0],
                    2.61731599547608)
        assert_close(_gbs("p", 94.2666666666667, 107.75, 0.498630136986301, 0.00372609838856132, 0, 0.2888)[0],
                    16.6074587545269)
        assert_close(_gbs("p", 94.3666666666667, 107.75, 0.583561643835616, 0.00370681407974257, 0, 0.2923)[0],
                    17.1686196701434)
        assert_close(_gbs("p", 94.44, 107.75, 0.668493150684932, 0.00364163303865433, 0, 0.2908)[0], 17.6038273793172)
        assert_close(_gbs("p", 94.4933333333333, 107.75, 0.750684931506849, 0.00355604221290591, 0, 0.2919)[0],
                    18.0870982577296)
        assert_close(_gbs("p", 94.49, 107.75, 0.835616438356164, 0.00346100468320478, 0, 0.2901)[0], 18.5149895730975)
        assert_close(_gbs("p", 94.39, 107.75, 0.917808219178082, 0.00337464630758452, 0, 0.2876)[0], 18.9397688539483)

        logging.info("Testing that valuation works for integer inputs")
        assert_close(_gbs("c", fs=100, x=95, t=1, r=1, b=0, v=1)[0], 14.6711476484)
        assert_close(_gbs("p", fs=100, x=95, t=1, r=1, b=0, v=1)[0], 12.8317504425)

        logging.info("Testing valuation works at minimum/maximum values for T")
        assert_close(_gbs("c", 100, 100, 0.00396825396825397, 0.000771332656950173, 0, 0.15)[0], 0.376962465712609)
        assert_close(_gbs("p", 100, 100, 0.00396825396825397, 0.000771332656950173, 0, 0.15)[0], 0.376962465712609)
        assert_close(_gbs("c", 100, 100, 100, 0.042033868311581, 0, 0.15)[0], 0.817104022604705)
        assert_close(_gbs("p", 100, 100, 100, 0.042033868311581, 0, 0.15)[0], 0.817104022604705)

        logging.info("Testing valuation works at minimum/maximum values for X")
        assert_close(_gbs("c", 100, 0.01, 1, 0.00330252458693489, 0, 0.15)[0], 99.660325245681)
        assert_close(_gbs("p", 100, 0.01, 1, 0.00330252458693489, 0, 0.15)[0], 0)
        assert_close(_gbs("c", 100, 2147483248, 1, 0.00330252458693489, 0, 0.15)[0], 0)
        assert_close(_gbs("p", 100, 2147483248, 1, 0.00330252458693489, 0, 0.15)[0], 2140402730.16601)

        logging.info("Testing valuation works at minimum/maximum values for F/S")
        assert_close(_gbs("c", 0.01, 100, 1, 0.00330252458693489, 0, 0.15)[0], 0)
        assert_close(_gbs("p", 0.01, 100, 1, 0.00330252458693489, 0, 0.15)[0], 99.660325245681)
        assert_close(_gbs("c", 2147483248, 100, 1, 0.00330252458693489, 0, 0.15)[0], 2140402730.16601)
        assert_close(_gbs("p", 2147483248, 100, 1, 0.00330252458693489, 0, 0.15)[0], 0)

        logging.info("Testing valuation works at minimum/maximum values for b")
        assert_close(_gbs("c", 100, 100, 1, 0.05, -1, 0.15)[0], 1.62505648981223E-11)
        assert_close(_gbs("p", 100, 100, 1, 0.05, -1, 0.15)[0], 60.1291675389721)
        assert_close(_gbs("c", 100, 100, 1, 0.05, 1, 0.15)[0], 163.448023481557)
        assert_close(_gbs("p", 100, 100, 1, 0.05, 1, 0.15)[0], 4.4173615264761E-11)

        logging.info("Testing valuation works at minimum/maximum values for r")
        assert_close(_gbs("c", 100, 100, 1, -1, 0, 0.15)[0], 16.2513262267156)
        assert_close(_gbs("p", 100, 100, 1, -1, 0, 0.15)[0], 16.2513262267156)
        assert_close(_gbs("c", 100, 100, 1, 1, 0, 0.15)[0], 2.19937783786316)
        assert_close(_gbs("p", 100, 100, 1, 1, 0, 0.15)[0], 2.19937783786316)

        logging.info("Testing valuation works at minimum/maximum values for V")
        assert_close(_gbs("c", 100, 100, 1, 0.05, 0, 0.005)[0], 0.189742620249)
        assert_close(_gbs("p", 100, 100, 1, 0.05, 0, 0.005)[0], 0.189742620249)

        assert_close(_gbs("c", 100, 100, 1, 0.05, 0, 1)[0], 36.424945370234)
        assert_close(_gbs("p", 100, 100, 1, 0.05, 0, 1)[0], 36.424945370234)

        logging.info("Checking that Greeks work for calls")
        assert_close(_gbs("c", 100, 100, 1, 0.05, 0, 0.15)[0], 5.68695251984796)
        assert_close(_gbs("c", 100, 100, 1, 0.05, 0, 0.15)[1], 0.50404947485)
        assert_close(_gbs("c", 100, 100, 1, 0.05, 0, 0.15)[2], 0.025227988795588)
        assert_close(_gbs("c", 100, 100, 1, 0.05, 0, 0.15)[3], -2.55380111351125)
        assert_close(_gbs("c", 100, 100, 2, 0.05, 0.05, 0.25)[4], 50.7636345571413)
        assert_close(_gbs("c", 100, 100, 1, 0.05, 0, 0.15)[5], 44.7179949651117)

        logging.info("Checking that Greeks work for puts")
        assert_close(_gbs("p", 100, 100, 1, 0.05, 0, 0.15)[0], 5.68695251984796)
        assert_close(_gbs("p", 100, 100, 1, 0.05, 0, 0.15)[1], -0.447179949651)
        assert_close(_gbs("p", 100, 100, 1, 0.05, 0, 0.15)[2], 0.025227988795588)
        assert_close(_gbs("p", 100, 100, 1, 0.05, 0, 0.15)[3], -2.55380111351125)
        assert_close(_gbs("p", 100, 100, 2, 0.05, 0.05, 0.25)[4], 50.7636345571413)
        assert_close(_gbs("p", 100, 100, 1, 0.05, 0, 0.15)[5], -50.4049474849597)

    def test_implied_volatility(self):

        logging.info("Testing at-the-money approximation")
        assert_close(_approx_implied_vol(option_type="c", fs=100, x=100, t=1, r=.05, b=0, cp=5),0.131757)
        assert_close(_approx_implied_vol(option_type="c", fs=59, x=60, t=0.25, r=.067, b=0.067, cp=2.82),0.239753)

        logging.info("Testing GBS Implied Vol")
        assert_close(_gbs_implied_vol("c", 92.45, 107.5, 0.0876712328767123, 0.00192960198828152, 0, 0.162619795863781),0.3)
        assert_close(_gbs_implied_vol("c", 93.0766666666667, 107.75, 0.164383561643836, 0.00266390125346286, 0, 0.584588840095316),0.2878)
        assert_close(_gbs_implied_vol("c", 93.5333333333333, 107.75, 0.249315068493151, 0.00319934651984034, 0, 1.27026849732877),0.2907)
        assert_close(_gbs_implied_vol("c", 93.8733333333333, 107.75, 0.331506849315069, 0.00350934592318849, 0, 1.97015685523537),0.2929)
        assert_close(_gbs_implied_vol("c", 94.1166666666667, 107.75, 0.416438356164384, 0.00367360967852615, 0, 2.61731599547608),0.2919)
        assert_close(_gbs_implied_vol("p", 94.2666666666667, 107.75, 0.498630136986301, 0.00372609838856132, 0, 16.6074587545269),0.2888)
        assert_close(_gbs_implied_vol("p", 94.3666666666667, 107.75, 0.583561643835616, 0.00370681407974257, 0, 17.1686196701434),0.2923)
        assert_close(_gbs_implied_vol("p", 94.44, 107.75, 0.668493150684932, 0.00364163303865433, 0, 17.6038273793172),0.2908)
        assert_close(_gbs_implied_vol("p", 94.4933333333333, 107.75, 0.750684931506849, 0.00355604221290591, 0, 18.0870982577296),0.2919)
        assert_close(_gbs_implied_vol("p", 94.39, 107.75, 0.917808219178082, 0.00337464630758452, 0, 18.9397688539483),0.2876)

        logging.info("Testing that GBS implied vol works for integer inputs")
        assert_close(_gbs_implied_vol("c", fs=100, x=95, t=1, r=1, b=0, cp=14.6711476484), 1)
        assert_close(_gbs_implied_vol("p", fs=100, x=95, t=1, r=1, b=0, cp=12.8317504425), 1)

        logging.info("Testing American Option implied volatility")
        assert_close(_american_implied_vol("p", fs=90, x=100, t=0.5, r=0.1, b=0, cp=10.54), 0.15, prec=0.01)
        assert_close(_american_implied_vol("p", fs=100, x=100, t=0.5, r=0.1, b=0, cp=6.7661), 0.25, prec=0.0001)
        assert_close(_american_implied_vol("p", fs=110, x=100, t=0.5, r=0.1, b=0, cp=5.8374), 0.35, prec=0.0001)
        assert_close(_american_implied_vol("c", fs=42, x=40, t=0.75, r=0.04, b=-0.04, cp=5.28), 0.35, prec=0.01)
        assert_close(_american_implied_vol("c", fs=90, x=100, t=0.1, r=0.10, b=0, cp=0.02), 0.15, prec=0.01)

        logging.info("Testing that American implied volatility works for integer inputs")
        assert_close(_american_implied_vol("c", fs=100, x=100, t=1, r=0, b=0, cp=13.892), 0.35, prec=0.01)
        assert_close(_american_implied_vol("p", fs=100, x=100, t=1, r=0, b=0, cp=13.892), 0.35, prec=0.01)

    def test_external_interface(self):

        # BlackScholes(option_type, X, FS, T, r, V)
        logging.info("Testing: GBS.BlackScholes")
        assert_close(black_scholes("c", 102, 100, 2, 0.05, 0.25)[0], 20.02128028)
        assert_close(black_scholes("p", 102, 100, 2, 0.05, 0.25)[0], 8.50502208)

        # Merton(option_type, X, FS, T, r, q, V)
        logging.info("Testing: GBS.Merton")
        assert_close(merton("c", 102, 100, 2, 0.05, 0.01, 0.25)[0], 18.63371484)
        assert_close(merton("p", 102, 100, 2, 0.05, 0.01, 0.25)[0], 9.13719197)

        # Black76(option_type, X, FS, T, r, V)
        logging.info("Testing: GBS.Black76")
        assert_close(black_76("c", 102, 100, 2, 0.05, 0.25)[0], 13.74803567)
        assert_close(black_76("p", 102, 100, 2, 0.05, 0.25)[0], 11.93836083)

        # garman_kohlhagen(option_type, X, FS, T, b, r, rf, V)
        logging.info("Testing: GBS.garman_kohlhagen")
        assert_close(garman_kohlhagen("c", 102, 100, 2, 0.05, 0.01, 0.25)[0], 18.63371484)
        assert_close(garman_kohlhagen("p", 102, 100, 2, 0.05, 0.01, 0.25)[0], 9.13719197)

        # Asian76(option_type, X, FS, T, TA, r, V):
        logging.info("Testing: Asian76")
        assert_close(asian_76("c", 102, 100, 2, 1.9, 0.05, 0.25)[0], 13.53508930)
        assert_close(asian_76("p", 102, 100, 2, 1.9, 0.05, 0.25)[0], 11.72541446)

        # Kirks76(option_type, X, F1, F2, T, r, V1, V2, corr)
        logging.info("Testing: Kirks")
        assert_close(kirks_76("c", f1=37.384913362, f2=42.1774, x=3.0, t=0.043055556, r=0, v1=0.608063, v2=0.608063, corr=.8)[0],0.007649192)
        assert_close(kirks_76("p", f1=37.384913362, f2=42.1774, x=3.0, t=0.043055556, r=0, v1=0.608063, v2=0.608063, corr=.8)[0],7.80013583)

    def test_model_validation(self):
        logging.info("Testing GBS.BlackScholes")
        assert_close(black_scholes("c", fs=60, x=65, t=0.25, r=0.08, v=0.30)[0], 2.13336844492)

        logging.info("Testing GBS.Merton")
        assert_close(merton("p", fs=100, x=95, t=0.5, r=0.10, q=0.05, v=0.20)[0], 2.46478764676)

        logging.info("Testing GBS.Black76")
        assert_close(black_76("c", fs=19, x=19, t=0.75, r=0.10, v=0.28)[0], 1.70105072524)

        logging.info("Testing GBS.garman_kohlhagen")
        assert_close(garman_kohlhagen("c", fs=1.56, x=1.60, t=0.5, r=0.06, rf=0.08, v=0.12)[0], 0.0290992531494)

        logging.info("Testing Delta")
        assert_close(black_76("c", fs=105, x=100, t=0.5, r=0.10, v=0.36)[1], 0.5946287)
        assert_close(black_76("p", fs=105, x=100, t=0.5, r=0.10, v=0.36)[1], -0.356601)

        logging.info("Testing Gamma")
        assert_close(black_scholes("c", fs=55, x=60, t=0.75, r=0.10, v=0.30)[2], 0.0278211604769)
        assert_close(black_scholes("p", fs=55, x=60, t=0.75, r=0.10, v=0.30)[2], 0.0278211604769)

        logging.info("Testing Theta")
        assert_close(merton("p", fs=430, x=405, t=0.0833, r=0.07, q=0.05, v=0.20)[3], -31.1923670565)

        logging.info("Testing Vega")
        assert_close(black_scholes("c", fs=55, x=60, t=0.75, r=0.10, v=0.30)[4], 18.9357773496)
        assert_close(black_scholes("p", fs=55, x=60, t=0.75, r=0.10, v=0.30)[4], 18.9357773496)

        logging.info("Testing Rho")
        assert_close(black_scholes("c", fs=72, x=75, t=1, r=0.09, v=0.19)[5], 38.7325050173)


if __name__ == "__main__":
    unittest.main()
