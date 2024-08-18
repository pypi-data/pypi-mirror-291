import pytest
import os
import numpy
import scipy.special
import dadi

def test_to_file():
    """
    Saving spectrum to file.
    """
    comments = ['comment 1', 'comment 2']
    filename = 'test.fs'
    data = numpy.random.rand(3,3)

    fs = dadi.Spectrum(data)

    fs.to_file(filename, comment_lines=comments)
    os.remove(filename)

    fs.to_file(filename, comment_lines=comments, foldmaskinfo=False)
    os.remove(filename)

def test_from_file():
    """
    Loading spectrum from file.
    """
    commentsin = ['comment 1', 'comment 2']
    filename = 'test.fs'
    data = numpy.random.rand(3,3)

    fsin = dadi.Spectrum(data)
    fsin.to_file(filename, comment_lines=commentsin)

    # Read the file.
    fsout,commentsout = dadi.Spectrum.from_file(filename, 
                                                return_comments=True)
    os.remove(filename)
    # Ensure that fs was read correctly.
    assert(numpy.allclose(fsout.data, fsin.data))
    assert(numpy.all(fsout.mask == fsin.mask))
    assert(fsout.folded == fsin.folded)
    # Ensure comments were read correctly.
    for ii,line in enumerate(commentsin):
        assert(line == commentsout[ii])

    # Test using old file format
    fsin.to_file(filename, comment_lines=commentsin, foldmaskinfo=False)

    # Read the file.
    fsout,commentsout = dadi.Spectrum.from_file(filename, 
                                                return_comments=True)
    os.remove(filename)
    # Ensure that fs was read correctly.
    assert(numpy.allclose(fsout.data, fsin.data))
    assert(numpy.all(fsout.mask == fsin.mask))
    assert(fsout.folded == fsin.folded)
    # Ensure comments were read correctly.
    for ii,line in enumerate(commentsin):
        assert(line == commentsout[ii])
    
    #
    # Now test a file with folding and masking
    #
    fsin = dadi.Spectrum(data).fold()
    fsin.mask[0,1] = True
    fsin.to_file(filename)

    fsout = dadi.Spectrum.from_file(filename)
    os.remove(filename)

    # Ensure that fs was read correctly.
    assert(numpy.allclose(fsout.data, fsin.data))
    assert(numpy.all(fsout.mask == fsin.mask))
    assert(fsout.folded == fsin.folded)

def test_folding():
    """
    Folding a 2D spectrum.
    """
    data = numpy.reshape(numpy.arange(12), (3,4))
    fs = dadi.Spectrum(data)
    ff = fs.fold()

    # Ensure no SNPs have gotten lost.
    assert(numpy.allclose(fs.sum(), ff.sum()))
    assert(numpy.allclose(fs.data.sum(), ff.data.sum()))
    # Ensure that the empty entries are actually empty.
    assert(numpy.all(ff.data[::-1] == numpy.tril(ff.data[::-1])))

    # This turns out to be the correct result.
    correct = numpy.tri(4)[::-1][-3:]*11
    assert(numpy.allclose(correct, ff.data))

def test_ambiguous_folding():
    """
    Test folding when the minor allele is ambiguous.
    """
    data = numpy.zeros((4,4))
    # Both these entries correspond to a an allele seen in 3 of 6 samples.
    # So the minor allele is ambiguous. In this case, we average the two
    # possible assignments.
    data[0,3] = 1
    data[3,0] = 3
    fs = dadi.Spectrum(data)
    ff = fs.fold()

    correct = numpy.zeros((4,4))
    correct[0,3] = correct[3,0] = 2
    assert(numpy.allclose(correct, ff.data))

def test_masked_folding():
    """
    Test folding when the minor allele is ambiguous.
    """
    data = numpy.zeros((5,6))
    fs = dadi.Spectrum(data)
    # This folds to an entry that will already be masked.
    fs.mask[1,2] = True
    # This folds to (1,1), which needs to be masked.
    fs.mask[3,4] = True
    ff = fs.fold()
    # Ensure that all those are masked.
    for entry in [(1,2), (3,4), (1,1)]:
        assert(ff.mask[entry])

def test_folded_slices():
    ns = (3,4)
    fs1 = dadi.Spectrum(numpy.random.rand(*ns))
    folded1 = fs1.fold()

    assert(fs1[:].folded == False)
    assert(folded1[:].folded == True)

    assert(fs1[0].folded == False)
    assert(folded1[1].folded == True)

    assert(fs1[:,0].folded == False)
    assert(folded1[:,1].folded == True)

def test_folded_arithmetic():
    """
    Test that arithmetic operations respect and propogate .folded attribute.
    """
    # Disable logging of warnings because arithmetic may generate Spectra
    # with entries < 0, but we don't care at this point.
    import logging
    dadi.Spectrum_mod.logger.setLevel(logging.ERROR)

    ns = (3,4)
    fs1 = dadi.Spectrum(numpy.random.uniform(size=ns))
    fs2 = dadi.Spectrum(numpy.random.uniform(size=ns))

    folded1 = fs1.fold()
    folded2 = fs2.fold()

    # We'll iterate through each of these arithmetic functions.
    from operator import add,sub,mul,truediv,floordiv,pow,abs,pos,neg

    arr = numpy.random.uniform(size=ns)
    marr = numpy.random.uniform(size=ns)

    # I found some difficulties with multiplication by numpy.float64, so I
    # want to explicitly test this case.
    numpyfloat = numpy.float64(2.0)

    for op in [add,sub,mul,truediv,floordiv,pow]:
        # Check that binary operations propogate folding status.
        # Need to check cases both on right-hand-side of operator and
        # left-hand-side

        # Note that numpy.power(2.0,fs2) does not properly propagate type
        # or status. I'm not sure how to fix this.

        result = op(fs1,fs2)
        assert(result.folded == False)
        assert(numpy.all(result.mask == fs1.mask))

        result = op(fs1,2.0)
        assert(result.folded == False)
        assert(numpy.all(result.mask == fs1.mask))

        result = op(2.0,fs2)
        assert(result.folded == False)
        assert(numpy.all(result.mask == fs2.mask))

        result = op(fs1,numpyfloat)
        assert(result.folded == False)
        assert(numpy.all(result.mask == fs1.mask))

        result = op(numpyfloat,fs2)
        assert(result.folded == False)
        assert(numpy.all(result.mask == fs2.mask))

        result = op(fs1,arr)
        assert(result.folded == False)
        assert(numpy.all(result.mask == fs1.mask))

        result = op(arr,fs2)
        assert(result.folded == False)
        assert(numpy.all(result.mask == fs2.mask))

        result = op(fs1,marr)
        assert(result.folded == False)
        assert(numpy.all(result.mask == fs1.mask))

        result = op(marr,fs2)
        assert(result.folded == False)
        assert(numpy.all(result.mask == fs2.mask))

        # Now with folded Spectra

        result = op(folded1,folded2)
        assert(result.folded)
        assert(numpy.all(result.mask == folded1.mask))

        result = op(folded1,2.0)
        assert(result.folded)
        assert(numpy.all(result.mask == folded1.mask))

        result = op(2.0,folded2)
        assert(result.folded)
        assert(numpy.all(result.mask == folded2.mask))

        result = op(folded1,numpyfloat)
        assert(result.folded)
        assert(numpy.all(result.mask == folded1.mask))

        result = op(numpyfloat,folded2)
        assert(result.folded)
        assert(numpy.all(result.mask == folded2.mask))

        result = op(folded1,arr)
        assert(result.folded)
        assert(numpy.all(result.mask == folded1.mask))

        result = op(arr,folded2)
        assert(result.folded)
        assert(numpy.all(result.mask == folded2.mask))

        result = op(folded1,marr)
        assert(result.folded)
        assert(numpy.all(result.mask == folded1.mask))

        result = op(marr,folded2)
        assert(result.folded)
        assert(numpy.all(result.mask == folded2.mask))

        # Check that exceptions are properly raised when folding status 
        # differs
        with pytest.raises(ValueError) as e_info:
            op(fs1, folded2)
            op(folded1, fs2)

    for op in [abs,pos,neg,scipy.special.gammaln]:
        # Check that unary operations propogate folding status.
        result = op(fs1)
        assert(result.folded == False)
        result = op(folded1)
        assert(result.folded)

    try:
        # The in-place methods aren't in operator in python 2.4...
        from operator import iadd,isub,imul,idiv,itruediv,ifloordiv,ipow
        for op in [iadd,isub,imul,idiv,itruediv,ifloordiv,ipow]:
            fs1origmask = fs1.mask.copy()

            # Check that in-place operations preserve folding status.
            op(fs1,fs2)
            assert(fs1.folded == False)
            assert(numpy.all(fs1.mask == fs1origmask))

            op(fs1,2.0)
            assert(fs1.folded == False)
            assert(numpy.all(fs1.mask == fs1origmask))

            op(fs1,numpyfloat)
            assert(fs1.folded == False)
            assert(numpy.all(fs1.mask == fs1origmask))

            op(fs1,arr)
            assert(fs1.folded == False)
            assert(numpy.all(fs1.mask == fs1origmask))

            op(fs1,marr)
            assert(fs1.folded == False)
            assert(numpy.all(fs1.mask == fs1origmask))

            # Now folded Spectra
            folded1origmask = folded1.mask.copy()

            op(folded1,folded2)
            assert(folded1.folded)
            assert(numpy.all(folded1.mask == folded1origmask))

            op(folded1,2.0)
            assert(folded1.folded)
            assert(numpy.all(folded1.mask == folded1origmask))

            op(folded1,numpyfloat)
            assert(folded1.folded)
            assert(numpy.all(folded1.mask == folded1origmask))

            op(folded1,arr)
            assert(folded1.folded)
            assert(numpy.all(folded1.mask == folded1origmask))

            op(folded1,marr)
            assert(folded1.folded)
            assert(numpy.all(folded1.mask == folded1origmask))

            # Check that exceptions are properly raised.
            with pytest.raises(ValueError) as e_info:
                op(fs1, folded2)
                op(folded1, fs2)
    except ImportError:
        pass

    # Restore logging of warnings
    dadi.Spectrum_mod.logger.setLevel(logging.WARNING)

def test_unfolding():
    ns = (3,4)

    # We add some unusual masking.
    fs = dadi.Spectrum(numpy.random.uniform(size=ns))
    fs.mask[0,1] = fs.mask[1,1] = True

    folded = fs.fold()
    unfolded = folded.unfold()

    # Check that it was properly recorded
    assert(unfolded.folded == False)

    # Check that no data was lost
    assert(numpy.allclose(fs.data.sum(), folded.data.sum()))
    assert(numpy.allclose(fs.data.sum(), unfolded.data.sum()))

    # Note that fs.sum() need not be equal to folded.sum(), if fs had
    # some masked values.
    assert(numpy.allclose(folded.sum(), unfolded.sum()))

    # Check that the proper entries are masked.
    assert(unfolded.mask[0,1])
    assert(unfolded.mask[(ns[0]-1),(ns[1]-1)-1])
    assert(unfolded.mask[1,1])
    assert(unfolded.mask[(ns[0]-1)-1,(ns[1]-1)-1])

def test_marginalize():
    ns = (7,8,6)

    fs = dadi.Spectrum(numpy.random.uniform(size=ns))
    folded = fs.fold()

    marg1 = fs.marginalize([1])
    # Do manual marginalization.
    manual = dadi.Spectrum(fs.data.sum(axis=1))

    # Check that these are equal in the unmasked entries.
    assert(numpy.allclose(numpy.where(marg1.mask, 0, marg1.data),
                                numpy.where(manual.mask, 0, manual.data)))

    # Check folded Spectrum objects. I should get the same result if I
    # marginalize then fold, as if I fold then marginalize.
    mf1 = marg1.fold()
    mf2 = folded.marginalize([1])
    assert(numpy.allclose(mf1,mf2))

def test_projection():
    # Test that projecting a multi-dimensional Spectrum succeeds
    ns = (7,8,6)
    fs = dadi.Spectrum(numpy.random.uniform(size=ns))
    p = fs.project([3,4,5])
    # Also that we don't lose any data
    assert(numpy.allclose(fs.data.sum(), p.data.sum()))

    # Check that when I project an equilibrium spectrum, I get back an
    # equilibrium spectrum
    fs = dadi.Spectrum(1./numpy.arange(100))
    p = fs.project([17])
    assert(numpy.allclose(p[1:-1], 1./numpy.arange(1,len(p)-1)))

    # Check that masked values are propagated correctly.
    fs = dadi.Spectrum(1./numpy.arange(20))
    # All values with 3 or fewer observed should be masked.
    fs.mask[3] = True
    p = fs.project([10])
    assert(numpy.all(p.mask[:4]))

    # Check that masked values are propagated correctly.
    fs = dadi.Spectrum(1./numpy.arange(20))
    fs.mask[-3] = True
    # All values with 3 or fewer observed should be masked.
    p = fs.project([10])
    assert(numpy.all(p.mask[-3:]))

    # A more complicated two dimensional projection problem...
    fs = dadi.Spectrum(numpy.random.uniform(size=(9,7)))
    fs.mask[2,3] = True
    p = fs.project([4,4])
    assert(numpy.all(p.mask[:3,1:4]))

    # Test that projecting a folded multi-dimensional Spectrum succeeds
    # Should get the same result if I fold then project as if I project
    # then fold.
    ns = (7,8,6)
    fs = dadi.Spectrum(numpy.random.uniform(size=ns))
    fs.mask[2,3,1] = True
    folded = fs.fold()

    p = fs.project([3,4,5])
    pf1 = p.fold()
    pf2 = folded.project([3,4,5])

    # Check equality
    assert(numpy.all(pf1.mask == pf2.mask))
    assert(numpy.allclose(pf1.data, pf2.data))

def test_filter_pops():
    """
    Test filtering populations in Spectrum.
    """
    ns = (7,8,6)

    fs = dadi.Spectrum(numpy.random.uniform(size=ns))
    folded = fs.fold()

    marg1 = fs.filter_pops([1,3])
    assert marg1.shape, (ns[0],ns[2])

    marg1 = fs.filter_pops([2])
    assert marg1.shape, (ns[1],)

def test_combine_two_pops():
    """
    Test combining two populations
    """
    ns = (2,3,4)
    fs = dadi.Spectrum(numpy.random.uniform(size=[_+1 for _ in ns]),
            pop_ids=['A','B','C'])
    fs.mask[2,2,3] = True

    new_fs = fs.combine_two_pops([3,1])

    # Test shape correct
    assert(numpy.array_equal(new_fs.sample_sizes, (6,3)))
    # Test data combined correctly
    assert(numpy.allclose(new_fs[2,1], fs[0,1,2]+fs[1,1,1]+fs[2,1,0]))
    # Test pop_ids formatted correctly
    assert new_fs.pop_ids[0], 'A+C'
    # Test that masked correctly
    assert(new_fs.mask[5,2])

def test_combine_pops():
    """
    Test combining multiple populations
    """
    ns = (1,2,3,4,5,6)
    fs = dadi.Spectrum(numpy.random.uniform(size=[_+1 for _ in ns]),
            pop_ids = 'ABCDEF')
    fs.mask[0,1,2,2,3,4] = True

    new_fs = fs.combine_pops([3,2,5])

    # Test shape correct
    assert(numpy.array_equal(new_fs.sample_sizes, (1,10,4,6)))
    # Test data combined correctly. For this entry, we need all ways the combined
    # pops can have 3 derived alleles.
    combos = [[0,0,3],[0,1,2],[0,2,1],[0,3,0],[1,0,2],[1,1,1],[1,2,0],[2,0,1],[2,1,0]]
    assert(numpy.allclose(new_fs[1,3,3,5], numpy.sum([fs[1,_[0],_[1],3,_[2],5] for _ in combos])))
    # Test pop_ids formatted correctly
    assert(new_fs.pop_ids[1] == 'B+C+E')
    # Test that masked correctly
    assert(new_fs.mask[0,6,2,4])

def test_reorder_pops():
    """
    Test fs.reorder_pops
    """
    fs = dadi.Spectrum(numpy.random.uniform(size=[4,5,6,7]), pop_ids=['A','B','C','D'])
    neworder = [2,4,3,1]
    reordered = fs.reorder_pops(neworder)

    # Assert that subsets of spectrum are correct
    assert(numpy.allclose(fs.filter_pops([2,3]), reordered.filter_pops([1,3])))
    # In this case, we need the transpose, because order has reversed
    assert(numpy.allclose(fs.filter_pops([1,2]).data, reordered.filter_pops([1,4]).transpose().data))
    # Assert that pop_ids are correct
    assert [fs.pop_ids[_-1] for _ in neworder], reordered.pop_ids
    # Test error checking
    with pytest.raises(ValueError) as e_info:
        fs.reorder_pops([1])
        fs.reorder_pops([2,1,2,3])
