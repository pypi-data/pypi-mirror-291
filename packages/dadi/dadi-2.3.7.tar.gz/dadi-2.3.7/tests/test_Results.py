import os
import numpy
import dadi

def test_1d_ic():
    # This just the standard neutral model
    func_ex = dadi.Numerics.make_extrap_log_func(dadi.Demographics1D.snm_1d)
    fs = func_ex([], (17,), [100,120,140])

    answer = dadi.Spectrum(1./numpy.arange(18))

    assert(numpy.ma.allclose(fs, answer, atol=1e-3))

def test_1d_stationary():
    func_ex = dadi.Numerics.\
            make_extrap_log_func(dadi.Demographics1D.two_epoch)
    # We let a two-epoch model equilibrate for tau=10, which should
    # eliminate almost all traces of the size change.
    fs = func_ex((0.5,10), (17,), [40,50,60])
    answer = dadi.Spectrum(0.5/numpy.arange(18))

    assert(numpy.ma.allclose(fs, answer, atol=1e-2))

def test_IM():
    func_ex = dadi.Numerics.\
            make_extrap_log_func(dadi.Demographics2D.IM)
    params = (0.8, 2.0, 0.6, 0.45, 5.0, 0.3)
    ns = (7,13)
    pts_l = [40,50,60]
    theta = 1000.
    fs = theta*func_ex(params, ns, pts_l)

    #mscore = dadi.Demographics2D.IM_mscore(params)
    #mscommand = dadi.Misc.ms_command(1,ns,mscore,1e6)
    #msfs = theta*dadi.Spectrum.from_ms_file(os.popen(mscommand))
    #msfs.to_file('IM.fs')
    msfs = dadi.Spectrum.from_file('tests/IM.fs')

    resid = dadi.Inference.Anscombe_Poisson_residual(fs,msfs)

    assert(abs(resid).max() < 0.2)
