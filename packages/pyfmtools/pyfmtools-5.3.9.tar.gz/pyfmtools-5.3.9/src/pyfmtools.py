###
# Python wrapper for Pyfmtools. Simplifies the usage of Pyfmtools by handling all Numpy and CFFI calls
###
"""Python wrapper for Pyfmtools. Simplifies the usage of Pyfmtools by 
handling all Numpy and CFFI calls

Pyfmtools provides various tools for handling fuzzy measures, 
calculating various indices, Choquet and Sugeno integrals, as well as 
fitting fuzzy measures to empirical data. This package is designed 
for Python , but it also includes the C++ source files and a user manual.
Chapter 2 of the user manual provides some background on fuzzy measures. 
A more detailed overview can be found in [4, 5, 12, 16] and references 
therein. Chapter 3 of the user manual outlines computational methods used 
to fit fuzzy measures to empirical data. The description of the programming 
library pyfmtools is given in Chapter 4. Examples of its usage are provided 
in Section 4.6.
To cite pyfmtools package, use references [2–6,21–24]. 
New in version 4
Random generation of fuzzy measures of different types, including k-additive, 
k-interactive, supermodular and submodular, sparse representation of k- additive 
fuzzy measures.

This file can also be imported as a module and contains the following
functions:
    * fm_init - initializes the package and returns env
    * fm_free - frees env
    * ShowCoalitions
    * generate_fm_2additive_concave
    * ShowCoalitionsCard
    * generate_fmconvex_tsort
    * generate_fm_tsort
    * ConvertCard2Bit
    * IsMeasureSupermodular
    * IsMeasureAdditive
    * export_maximal_chains
    * Choquet
    * Sugeno
    * ExpandKinteractive2Bit
    * Shapley
    * Banzhaf
    * ShapleyMob
    * BanzhafMob
    * ConstructLambdaMeasure
    * ConstructLambdaMeasureMob
    * dualm
    * dualmMob
    * FuzzyMeasureFit
    * FuzzyMeasureFitMob
    * FuzzyMeasureFitKtolerant
    * FuzzyMeasureFitLPKmaxitive
    * FuzzyMeasureFitLPKinteractive
    * FuzzyMeasureFitLPKinteractiveMaxChains
    * FuzzyMeasureFitLPKinteractiveAutoK
    * FuzzyMeasureFitLPKinteractiveMarginal
    * FuzzyMeasureFitLPKinteractiveMarginalMaxChain
    * FuzzyMeasureFitLP
    * FuzzyMeasureFitLPMob
    * fittingOWA
    * fittingWAM
    * Interaction
    * InteractionB
    * InteractionMob
    * InteractionBMob
    * BipartitionShapleyIndex
    * BipartitionBanzhafIndex
    * BNonadditivityIndexMob
    * NonadditivityIndex
    * NonmodularityIndex
    * NonmodularityIndexMob
    * NonmodularityIndexKinteractive
    * NonmodularityIndexMobkadditive
    * Mobius
    * Zeta
    * dualMobKadd
    * Shapley2addMob
    * Banzhaf2addMob
    * prepare_fm_sparse
    * ShapleyMob_sparse
    * BanzhafMob_sparse
    * populate_fm_2add_sparse
    * add_pair_sparse
    * add_tuple_sparse
    * populate_fm_2add_sparse_from2add
    * expand_2add_full
    * expand_sparse_full
    * sparse_get_singletons
    * Nonmodularityindex_sparse
    * SizeArraykinteractive
    * IsSubsetC
    * IsElementC
    * IsMeasureBalanced
    * IsMeasureSelfdual
    * IsMeasureSubadditive
    * IsMeasureSubmodular
    * IsMeasureSuperadditive
    * IsMeasureSymmetric
    * IsMeasureKMaxitive
    * IsMeasureAdditiveMob
    * IsMeasureBalancedMob
    * IsMeasureSelfdualMob
	* IsMeasureSubadditiveMob
    * IsMeasureSubmodularMob
    * IsMeasureSuperadditiveMob
    * IsMeasureSupermodularMob
    * IsMeasureSymmetricMob
    * IsMeasureKMaxitiveMob
    * fm_arraysize
    * generate_fm_minplus
    * generate_fm_2additive_convex
    * generate_fm_2additive_convex_withsomeindependent
    * tuple_cardinality_sparse
    * get_num_tuples(struct
    * get_sizearray_tuples(struct
    * is_inset_sparse
    * is_subset_sparse
    * sparse_get_pairs
    * sparse_get_tuples
    * generate_fm_2additive_convex_sparse
    * generate_fm_kadditive_convex_sparse
    * min_subset
    * max_subset
    * min_subsetC
    * max_subsetNegC
    * ChoquetKinter
    * ChoquetMob
    * Entropy
    * Orness
    * OWA
    * WAM
    * Choquet2addMob
    * min_subset_sparse
    * max_subset_sparse
    * ChoquetMob_sparse
"""



import sys
import numpy as np
import types
import math
import re
from  _pyfmtools import ffi, lib as fm


CB = None
# call-back function
@ffi.def_extern()
def py_user_defined_measurecheck(  n, x):
    # print( "py_user_defined")
    # User defined python function
    return CB( n, x)

# Retrieve C call-back function based on Python call-back function
def get_c_callback_function( py_cb):
    try:
        # check if this is a function
        if not( isinstance( py_cb, types.FunctionType)): raise ValueError( "no call-back function")

        # Check if Python call-back function is one of the pre-defined call-backs
        if( py_cb == py_user_defined_measurecheck): p_c_cb = fm.py_user_defined_measurecheck
        else: raise ValueError( "undefined call-back function")

        return p_c_cb
    except ValueError:
        raise
        
        

###
# Helper functions
###

# global variable to support trace-info while testing
isTest = False

# Trace function
def trace( str):
    if isTest == True: print( "-- ", str, " --")


# convert Python float to CFFI double * 
def convert_float_to_CFFI_double( x):
    if x.dtype != "float64": x = x.astype(float)
    px = ffi.cast( "double *", x.ctypes.data)
    return px

# use numpy to create an intc array with n zeros and cast to CFFI 
def create_intc_zeros_as_CFFI_int( n):
    x = np.zeros( int(n), np.intc)
    px = ffi.cast( "int *", x.ctypes.data)
    return x, px

# use numpy to create an float array with n zeros and cast to CFFI 
def create_float_zeros_as_CFFI_double( n):
    x = np.zeros( int(n), dtype=np.float64)
    px = ffi.cast( "double *", x.ctypes.data)
    return x, px

    # use numpy to create an float array with n zeros and cast to CFFI 
def create_zeros_as_CFFI_uint64( n):
    x = np.zeros( int(n), dtype=np.uint64)
    px = ffi.cast( "unsigned long long int *", x.ctypes.data)
    return x, px


# version of the function using np.ascontiguousarray() 
def convert_py_float_to_cffi_cont( x):
    if x is not None:
        if isinstance( x, np.ndarray) and ( x.flags.c_contiguous == True) and ( x.dtype == np.float64):
            px = x
        else:
            px =  np.ascontiguousarray( x, dtype = 'float64')
        pxcffi = ffi.cast( "double *", px.ctypes.data)
    else:
        # handle None
        px = np.array( 0)
        pxcffi = ffi.cast( "double *", 0)
    return px, pxcffi

# version of the function using np.array() 
def convert_py_float_to_cffi( x):
    if x is not None:
        if isinstance( x, np.ndarray) and ( x.flags.c_contiguous == True) and ( x.dtype == np.float64):
            px = x
        else:
            px =  np.array( x, dtype = 'float64')
        pxcffi = ffi.cast( "double *", px.ctypes.data)
    else:
        # handle None
        px = np.array( 0)
        pxcffi = ffi.cast( "double *", 0)
    return px, pxcffi

# version of the function using np.ascontiguousarray() 
def convert_py_int_to_cffi_cont( x):
    if x is not None:
        if isinstance( x, np.ndarray) and ( x.flags.c_contiguous == True) and ( x.dtype == np.int32):
            px = x
        else:
            px =  np.ascontiguousarray( x, dtype = 'int32')
        pxcffi = ffi.cast( "int *", px.ctypes.data)
    else:
        # handle None
        px = np.array( 0)
        pxcffi = ffi.cast( "int *", 0)
    return px, pxcffi

# version of the function using np.array() 
def convert_py_int_to_cffi( x):
    if x is not None:
        if isinstance( x, np.ndarray) and ( x.flags.c_contiguous == True) and ( x.dtype == np.int32):
            px = x
        else:
            px =  np.array( x, dtype = 'int32')
        pxcffi = ffi.cast( "int *", px.ctypes.data)
    else:
        # handle None
        px = np.array( 0)
        pxcffi = ffi.cast( "int *", 0)
    return px, pxcffi

###
# The python minimum wrapper for py_ functions from wrapper.cpp
###

# void py_fm_init(int n, struct fm_env* env)
def fm_init( n):
    try:
        trace( "py_fm_init")
        env = ffi.new( "struct fm_env *")
        fm.py_fm_init( n, env)
        return env
    except ValueError:
        raise

# void py_fm_free( struct fm_env* env)
def fm_free( env):
    try:
        trace( "py_fm_free")
        if( env == None): raise ValueError( "Env not initialised") 
        fm.py_fm_free( env)
        return None
    except ValueError:
        raise

# void py_ShowCoalitions(int* coalition, struct fm_env* env)
def ShowCoalitions( env):
    trace( "py_ShowCoalitions")
    A, pA = create_intc_zeros_as_CFFI_int( env.m) 
    fm.py_ShowCoalitions( pA, env)
    return A

# int py_generate_fm_2additive_concave(int num, int n, double * vv)
def generate_fm_2additive_concave( ti, n, env):
    trace( "py_generate_fm_2additive_concave")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    size = fm.py_generate_fm_2additive_concave( ti, n, pv)
    return size, v

# void py_ShowCoalitionsCard(int* coalition, struct fm_env* env)
def ShowCoalitionsCard( env):
    trace( "py_ShowCoalitionsCard")
    A, pA = create_intc_zeros_as_CFFI_int( env.m) 
    A = fm.py_ShowCoalitionsCard( pA, env)
    return A

# py_generate_fmconvex_tsort(ti,n, n-1 , 1000, 8, 1, pv,env)
def generate_fmconvex_tsort( num, n, kint, markov, option, K, env):
    trace( "py_generate_fmconvex_tsort")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    size = fm.py_generate_fmconvex_tsort( num ,n, kint, markov, option, K, pv, env)
    return size, v

# py_generate_fm_tsort(ti,n, 2 , 10, 0, 0.1, pv,env)
def generate_fm_tsort( num, n, kint, markov, option, K, env):
    trace( "py_generate_fm_tsort")
    v, pv = create_float_zeros_as_CFFI_double( env.m)
    size = fm.py_generate_fm_tsort( num ,n, kint, markov, option, K, env)
    return size, v

# py_ConvertCard2Bit(pvb,pv,env)
def ConvertCard2Bit( v, env):
    trace( "py_ConvertCard2Bit")
    
    pv = convert_float_to_CFFI_double( v)
    vb, pvb = create_float_zeros_as_CFFI_double( env.m)
    fm.py_ConvertCard2Bit( pvb, pv, env)
    return vb 

# py_IsMeasureSupermodular(pvb,env)
def IsMeasureSupermodular( vb, env):
    trace( "py_IsMeasureSupermodular")
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_IsMeasureSupermodular( pvb, env)

# py_IsMeasureAdditive(pvb,env)
def IsMeasureAdditive( vb, env):
    trace( "y_IsMeasureAdditive")
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_IsMeasureAdditive( pvb, env)

# py_export_maximal_chains(n,pvb,pmc,env)
def export_maximal_chains( n, vb, env):
    trace( "py_export_maximal_chains")
    pvb = convert_float_to_CFFI_double( vb)
    mc, pmc = create_float_zeros_as_CFFI_double( math.factorial(n) * n)
    fm.py_export_maximal_chains( n, pvb, pmc, env)
    return mc

# py_Choquet(px,pvb,env)
def Choquet( x, vb, env):
    trace( "y_Choquet")
    npx = np.array( x)
    pnpx = ffi.cast( "double *", npx.ctypes.data)
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_Choquet( pnpx, pvb, env)

# double py_Sugeno(double* x, double* v, struct fm_env* env)
def Sugeno( x, vb, env):
    trace( "py_Sugeno")
    npx = np.array( x)
    pnpx = ffi.cast( "double *", npx.ctypes.data)
    pvb = convert_float_to_CFFI_double( vb)
    return fm.py_Sugeno( pnpx, pvb, env)



###
# The python wrapper for all other py_ functions from wrapper.cpp
###


#    double py_min_subset(double* x, int n, int_64 S)
def min_subset(x, n, S):
    trace( "double py_min_subset(double* x, int n, int_64 S)")
    pxnp, px = convert_py_float_to_cffi( x)
    yy = fm.py_min_subset( px, n, S)
    return yy



#    double py_max_subset(double* x, int n, int_64 S)
def max_subset(x, n, S):
    trace( "double py_max_subset(double* x, int n, int_64 S)")
    pxnp, px = convert_py_float_to_cffi( x)
    yy = fm.py_max_subset( px, n, S)
    return yy



#    double py_min_subsetC(double* x, int n, int_64 S, struct fm_env* env)
def min_subsetC(x, n, S, env):
    trace( "double py_min_subsetC(double* x, int n, int_64 S, struct fm_env* env)")
    pxnp, px = convert_py_float_to_cffi( x)
    yy = fm.py_min_subsetC( px, n, S, env)
    return yy



#    double py_max_subsetNegC(double* x, int n, int_64 S, struct fm_env* env)
def max_subsetNegC(x, n, S, env):
    trace( "double py_max_subsetNegC(double* x, int n, int_64 S, struct fm_env* env)")
    pxnp, px = convert_py_float_to_cffi( x)
    yy = fm.py_max_subsetNegC( px, n, S, env)
    return yy



#    int py_SizeArraykinteractive(int n, int k, struct fm_env* env)
def SizeArraykinteractive(n, k, env):
    trace( "int py_SizeArraykinteractive(int n, int k, struct fm_env* env)")
    yy = fm.py_SizeArraykinteractive( n, k, env)
    return yy



#    int py_IsSubsetC(int i, int j, struct fm_env* env)
def IsSubsetC(i, j, env):
    trace( "int py_IsSubsetC(int i, int j, struct fm_env* env)")
    yy = fm.py_IsSubsetC( i, j, env)
    return yy



#    int py_IsElementC(int i, int j, struct fm_env* env)
def IsElementC(i, j, env):
    trace( "int py_IsElementC(int i, int j, struct fm_env* env)")
    yy = fm.py_IsElementC( i, j, env)
    return yy



#    void py_ExpandKinteractive2Bit(double* out_dest, double* src, struct fm_env* env, int kint, int arraysize)
def ExpandKinteractive2Bit(src, env, kint):
    trace( "void py_ExpandKinteractive2Bit(double* out_dest, double* src, struct fm_env* env, int kint, int arraysize)")
    pout_destnp, pout_dest = create_float_zeros_as_CFFI_double( env.m)
    psrcnp, psrc = convert_py_float_to_cffi( src)
    arraysize = fm.py_SizeArraykinteractive( env.n, kint, env)
    fm.py_ExpandKinteractive2Bit( pout_dest, psrc, env, kint, arraysize)
    return pout_destnp


#    void py_Shapley(double* v, double* out_x, struct fm_env* env)
def Shapley(v, env):
    trace( "void py_Shapley(double* v, double* out_x, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_xnp, pout_x = create_float_zeros_as_CFFI_double( env.n)
    fm.py_Shapley( pv, pout_x, env)
    return pout_xnp



#    void py_Banzhaf(double* v, double* out_B, struct fm_env* env)
def Banzhaf(v, env):
    trace( "void py_Banzhaf(double* v, double* out_B, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_Bnp, pout_B = create_float_zeros_as_CFFI_double( env.n)
    fm.py_Banzhaf( pv, pout_B, env)
    return pout_Bnp



#    void py_ShapleyMob(double* Mob, double* out_x, struct fm_env* env)
def ShapleyMob(Mob, env):
    trace( "void py_ShapleyMob(double* Mob, double* out_x, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    pout_xnp, pout_x = create_float_zeros_as_CFFI_double( env.n)
    fm.py_ShapleyMob( pMob, pout_x, env)
    return pout_xnp



#    void py_BanzhafMob(double* Mob, double* out_B, struct fm_env* env)
def BanzhafMob(Mob, env):
    trace( "void py_BanzhafMob(double* Mob, double* out_B, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    pout_Bnp, pout_B = create_float_zeros_as_CFFI_double( env.n)
    fm.py_BanzhafMob( pMob, pout_B, env)
    return pout_Bnp



#    double py_ChoquetKinter(double* x, double* v, int kint, struct fm_env* env)
def ChoquetKinter(x, v, kint, env):
    trace( "double py_ChoquetKinter(double* x, double* v, int kint, struct fm_env* env)")
    pxnp, px = convert_py_float_to_cffi( x)
    pvnp, pv = convert_py_float_to_cffi( v)
    yy = fm.py_ChoquetKinter( px, pv, kint, env)
    return yy



#    double py_ChoquetMob(double* x, double* Mob, struct fm_env* env)
def ChoquetMob(x, Mob, env):
    trace( "double py_ChoquetMob(double* x, double* Mob, struct fm_env* env)")
    pxnp, px = convert_py_float_to_cffi( x)
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_ChoquetMob( px, pMob, env)
    return yy



#    void py_ConstructLambdaMeasure(double* singletons, double* out_lambdax, double* out_v, struct fm_env* env)
def ConstructLambdaMeasure(singletons, env):
    trace( "void py_ConstructLambdaMeasure(double* singletons, double* out_lambdax, double* out_v, struct fm_env* env)")
    psingletonsnp, psingletons = convert_py_float_to_cffi( singletons)
    # lambda is an array of size 1 
    pout_lambdaxnp, pout_lambdax = create_float_zeros_as_CFFI_double( 1)
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    fm.py_ConstructLambdaMeasure( psingletons, pout_lambdax, pout_v, env)
    return pout_lambdaxnp, pout_vnp



#    void py_ConstructLambdaMeasureMob(double* singletons, double* out_lambdax, double* out_Mob, struct fm_env* env)
def ConstructLambdaMeasureMob(singletons, env):
    trace( "void py_ConstructLambdaMeasureMob(double* singletons, double* out_lambdax, double* out_Mob, struct fm_env* env)")
    psingletonsnp, psingletons = convert_py_float_to_cffi( singletons)
    # lambda is an array of size 1 
    pout_lambdaxnp, pout_lambdax = create_float_zeros_as_CFFI_double( 1)
    pout_Mobnp, pout_Mob = create_float_zeros_as_CFFI_double( env.m)
    fm.py_ConstructLambdaMeasureMob( psingletons, pout_lambdax, pout_Mob, env)
    return pout_lambdaxnp, pout_Mobnp



#    void py_dualm(double* v, double* out_w, struct fm_env* env)
def dualm(v, env):
    trace( "void py_dualm(double* v, double* out_w, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_wnp, pout_w = create_float_zeros_as_CFFI_double( env.m)
    fm.py_dualm( pv, pout_w, env)
    return pout_wnp



#    void py_dualmMob(double* v, double* out_w, struct fm_env* env)
def dualmMob(v, env):
    trace( "void py_dualmMob(double* v, double* out_w, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_wnp, pout_w = create_float_zeros_as_CFFI_double( env.m)
    fm.py_dualmMob( pv, pout_w, env)
    return pout_wnp



#    double py_Entropy(double* v, struct fm_env* env)
def Entropy(v, env):
    trace( "double py_Entropy(double* v, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    yy = fm.py_Entropy( pv, env)
    return yy



#    void py_FuzzyMeasureFit(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
def FuzzyMeasureFit(datanum, additive, env, dataset):
    trace( "void py_FuzzyMeasureFit(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    fm.py_FuzzyMeasureFit( datanum, additive, env, pout_v, pdataset)
    return pout_vnp



#    void py_FuzzyMeasureFitMob(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
def FuzzyMeasureFitMob(datanum, additive, env, dataset):
    trace( "void py_FuzzyMeasureFitMob(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    fm.py_FuzzyMeasureFitMob( datanum, additive, env, pout_v, pdataset)
    return pout_vnp



#    void py_FuzzyMeasureFitKtolerant(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
def FuzzyMeasureFitKtolerant(datanum, additive, env, dataset):
    trace( "void py_FuzzyMeasureFitKtolerant(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    fm.py_FuzzyMeasureFitKtolerant( datanum, additive, env, pout_v, pdataset)
    return pout_vnp



#    void py_FuzzyMeasureFitLPKmaxitive(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)
def FuzzyMeasureFitLPKmaxitive(datanum, additive, env, dataset):
    trace( "void py_FuzzyMeasureFitLPKmaxitive(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    fm.py_FuzzyMeasureFitLPKmaxitive( datanum, additive, env, pout_v, pdataset)
    return pout_vnp



#    void py_FuzzyMeasureFitLPKinteractive(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K)
def FuzzyMeasureFitLPKinteractive(datanum, additive, env, K, dataset):
    trace( "void py_FuzzyMeasureFitLPKinteractive(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    pKnp, pK = convert_py_float_to_cffi_cont( K)
    fm.py_FuzzyMeasureFitLPKinteractive( datanum, additive, env, pout_v, pdataset, pK)
    return pout_vnp



#    void py_FuzzyMeasureFitLPKinteractiveMaxChains(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K)
def FuzzyMeasureFitLPKinteractiveMaxChains(datanum, additive, env, K, dataset):
    trace( "void py_FuzzyMeasureFitLPKinteractiveMaxChains(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi( dataset)
    pKnp, pK = convert_py_float_to_cffi( K)
    fm.py_FuzzyMeasureFitLPKinteractiveMaxChains( datanum, additive, env, pout_v, pdataset, pK)
    return pout_vnp



#    void py_FuzzyMeasureFitLPKinteractiveAutoK(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int* maxiters)
def FuzzyMeasureFitLPKinteractiveAutoK(datanum, additive, env, K, maxiters, dataset):
    trace( "void py_FuzzyMeasureFitLPKinteractiveAutoK(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int* maxiters)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    pKnp, pK = convert_py_float_to_cffi_cont( K)
    pmaxitersnp, pmaxiters = convert_py_int_to_cffi_cont( maxiters)
    fm.py_FuzzyMeasureFitLPKinteractiveAutoK( datanum, additive, env, pout_v, pdataset, pK, pmaxiters)
    return pout_vnp



#    void py_FuzzyMeasureFitLPKinteractiveMarginal(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int submod)
def FuzzyMeasureFitLPKinteractiveMarginal(datanum, additive, env, K, submod, dataset):
    trace( "void py_FuzzyMeasureFitLPKinteractiveMarginal(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int submod)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    pKnp, pK = convert_py_float_to_cffi_cont( K)
    fm.py_FuzzyMeasureFitLPKinteractiveMarginal( datanum, additive, env, pout_v, pdataset, pK, submod)
    return pout_vnp

#    void py_FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int* maxiters, int submod)
def FuzzyMeasureFitLPKinteractiveMarginalMaxChain(datanum, additive, env, K, maxiters, submod, dataset):
    trace( "void py_FuzzyMeasureFitLPKinteractiveMarginalMaxChain(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, double* K, int* maxiters, int submod)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    pKnp, pK = convert_py_float_to_cffi_cont( K)
    pmaxitersnp, pmaxiters = convert_py_int_to_cffi_cont( maxiters)
    fm.py_FuzzyMeasureFitLPKinteractiveMarginalMaxChain( datanum, additive, env, pout_v, pdataset, pK, pmaxiters, submod)
    return pout_vnp


#    void py_FuzzyMeasureFitLP(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)
def FuzzyMeasureFitLP(datanum, additive, env, options, indexlow, indexhihg, option1, orness, dataset):
    trace( "void py_FuzzyMeasureFitLP(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    poptionsnp, poptions = convert_py_int_to_cffi_cont( options)
    pindexlownp, pindexlow = convert_py_float_to_cffi_cont( indexlow)
    pindexhihgnp, pindexhihg = convert_py_float_to_cffi_cont( indexhihg)
    poption1np, poption1 = convert_py_int_to_cffi_cont( option1)
    pornessnp, porness = convert_py_float_to_cffi_cont( orness)
    fm.py_FuzzyMeasureFitLP( datanum, additive, env, pout_v, pdataset, poptions, pindexlow, pindexhihg, poption1, porness)
    return pout_vnp


#    void py_FuzzyMeasureFitLPMob(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)
def FuzzyMeasureFitLPMob(datanum, additive, env, options, indexlow, indexhihg, option1, orness, dataset):
    trace( "void py_FuzzyMeasureFitLPMob(int datanum, int additive, struct fm_env* env, double* out_v, double* dataset, int* options, double* indexlow, double* indexhihg, int* option1, double* orness)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    poptionsnp, poptions = convert_py_int_to_cffi_cont( options)
    pindexlownp, pindexlow = convert_py_float_to_cffi_cont( indexlow)
    pindexhihgnp, pindexhihg = convert_py_float_to_cffi_cont( indexhihg)
    poption1np, poption1 = convert_py_int_to_cffi_cont( option1)
    pornessnp, porness = convert_py_float_to_cffi_cont( orness)
    fm.py_FuzzyMeasureFitLPMob( datanum, additive, env, pout_v, pdataset, poptions, pindexlow, pindexhihg, poption1, porness)
    return pout_vnp


#    void py_fittingOWA(int datanum, struct fm_env* env, double* out_v, double* dataset)
def fittingOWA(datanum, env, dataset):
    trace( "void py_fittingOWA(int datanum, struct fm_env* env, double* out_v, double* dataset)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    fm.py_fittingOWA( datanum, env, pout_v, pdataset)
    return pout_vnp, dataset


#    void py_fittingWAM(int datanum, struct fm_env* env, double* out_v, double* dataset)
def fittingWAM(datanum, env, dataset):
    trace( "void py_fittingWAM(int datanum, struct fm_env* env, double* out_v, double* dataset)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    fm.py_fittingWAM( datanum, env, pout_v, pdataset)
    return pout_vnp


#    void py_Interaction(double* Mob, double* out_v, struct fm_env* env)
def Interaction(Mob, env):
    trace( "void py_Interaction(double* Mob, double* out_v, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    length = len( Mob)
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( length)
    fm.py_Interaction( pMob, pout_v, env)
    return pout_vnp



#    void py_InteractionB(double* Mob, double* out_v, struct fm_env* env)
def InteractionB(Mob, env):
    trace( "void py_InteractionB(double* Mob, double* out_v, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    length = len( Mob)
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( length)
    fm.py_InteractionB( pMob, pout_v, env)
    return pout_vnp


#    void py_InteractionMob(double* Mob, double* out_v, struct fm_env* env)
def InteractionMob(Mob, env):
    trace( "void py_InteractionMob(double* Mob, double* out_v, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    length = len( Mob)
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( length)
    fm.py_InteractionMob( pMob, pout_v, env)
    return pout_vnp



#    void py_InteractionBMob(double* Mob, double* out_v, struct fm_env* env)
def InteractionBMob(Mob, env):
    trace( "void py_InteractionBMob(double* Mob, double* out_v, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    length = len( Mob)
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( length)
    fm.py_InteractionBMob( pMob, pout_v, env)
    return pout_vnp


#    void py_BipartitionShapleyIndex(double* v, double* out_w, struct fm_env* env)
def BipartitionShapleyIndex(v, env):
    trace( "void py_BipartitionShapleyIndex(double* v, double* out_w, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_wnp, pout_w = create_float_zeros_as_CFFI_double( env.m)
    fm.py_BipartitionShapleyIndex( pv, pout_w, env)
    return pout_wnp



#    void py_BipartitionBanzhafIndex(double* v, double* out_w, struct fm_env* env)
def BipartitionBanzhafIndex(v, env):
    trace( "void py_BipartitionBanzhafIndex(double* v, double* out_w, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_wnp, pout_w = create_float_zeros_as_CFFI_double( env.m)
    fm.py_BipartitionBanzhafIndex( pv, pout_w, env)
    return pout_wnp



#    void py_NonadditivityIndexMob(double* Mob, double* out_w, struct fm_env* env)
def NonadditivityIndexMob(Mob, env):
    trace( "void py_NonadditivityIndexMob(double* Mob, double* out_w, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    pout_wnp, pout_w = create_float_zeros_as_CFFI_double( env.m)
    fm.py_NonadditivityIndexMob( pMob, pout_w, env)
    return pout_wnp



#    void py_NonadditivityIndex(double* v, double* out_w, struct fm_env* env)
def NonadditivityIndex(v, env):
    trace( "void py_NonadditivityIndex(double* v, double* out_w, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_wnp, pout_w = create_float_zeros_as_CFFI_double( env.m)
    fm.py_NonadditivityIndex( pv, pout_w, env)
    return pout_wnp



#    void py_NonmodularityIndex(double* v, double* out_w, struct fm_env* env)
def NonmodularityIndex(v, env):
    trace( "void py_NonmodularityIndex(double* v, double* out_w, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_wnp, pout_w = create_float_zeros_as_CFFI_double( env.m)
    fm.py_NonmodularityIndex( pv, pout_w, env)
    return pout_wnp



#    void py_NonmodularityIndexMob(double* Mob, double* out_w, struct fm_env* env)
def NonmodularityIndexMob(Mob, env):
    trace( "void py_NonmodularityIndexMob(double* Mob, double* out_w, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    pout_wnp, pout_w = create_float_zeros_as_CFFI_double( env.m)
    fm.py_NonmodularityIndexMob( pMob, pout_w, env)
    return pout_wnp



#    void py_NonmodularityIndexKinteractive(double* v, double* out_w, int kint,  struct fm_env* env)
def NonmodularityIndexKinteractive(v, kint, env):
    trace( "void py_NonmodularityIndexKinteractive(double* v, double* out_w, int kint,  struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_wnp, pout_w = create_float_zeros_as_CFFI_double( env.m)
    fm.py_NonmodularityIndexKinteractive( pv, pout_w, kint, env)
    return pout_wnp



#    void py_NonmodularityIndexMobkadditive(double* Mob, double* out_w, int k,  struct fm_env* env)
def NonmodularityIndexMobkadditive(Mob, k, env):
    trace( "void py_NonmodularityIndexMobkadditive(double* Mob, double* out_w, int k,  struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    pout_wnp, pout_w = create_float_zeros_as_CFFI_double( env.m)
    fm.py_NonmodularityIndexMobkadditive( pMob, pout_w, k, env)
    return pout_wnp



#    int py_IsMeasureBalanced(double* v, struct fm_env* env)
def IsMeasureBalanced(v, env):
    trace( "int py_IsMeasureBalanced(double* v, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureBalanced( pv, env)
    return yy



#    int py_IsMeasureSelfdual(double* v, struct fm_env* env)
def IsMeasureSelfdual(v, env):
    trace( "int py_IsMeasureSelfdual(double* v, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureSelfdual( pv, env)
    return yy



#    int py_IsMeasureSubadditive(double* v, struct fm_env* env)
def IsMeasureSubadditive(v, env):
    trace( "int py_IsMeasureSubadditive(double* v, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureSubadditive( pv, env)
    return yy



#    int py_IsMeasureSubmodular(double* v, struct fm_env* env)
def IsMeasureSubmodular(v, env):
    trace( "int py_IsMeasureSubmodular(double* v, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureSubmodular( pv, env)
    return yy



#    int py_IsMeasureSuperadditive(double* v, struct fm_env* env)
def IsMeasureSuperadditive(v, env):
    trace( "int py_IsMeasureSuperadditive(double* v, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureSuperadditive( pv, env)
    return yy



#    int py_IsMeasureSymmetric(double* v, struct fm_env* env)
def IsMeasureSymmetric(v, env):
    trace( "int py_IsMeasureSymmetric(double* v, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureSymmetric( pv, env)
    return yy



#    int py_IsMeasureKMaxitive(double* v, struct fm_env* env)
def IsMeasureKMaxitive(v, env):
    trace( "int py_IsMeasureKMaxitive(double* v, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    yy = fm.py_IsMeasureKMaxitive( pv, env)
    return yy



#    int py_IsMeasureAdditiveMob(double* Mob, struct fm_env* env)
def IsMeasureAdditiveMob(Mob, env):
    trace( "int py_IsMeasureAdditiveMob(double* Mob, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureAdditiveMob( pMob, env)
    return yy



#    int py_IsMeasureBalancedMob(double* Mob, struct fm_env* env)
def IsMeasureBalancedMob(Mob, env):
    trace( "int py_IsMeasureBalancedMob(double* Mob, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureBalancedMob( pMob, env)
    return yy



#    int py_IsMeasureSelfdualMob(double* Mob, struct fm_env* env)
def IsMeasureSelfdualMob(Mob, env):
    trace( "int py_IsMeasureSelfdualMob(double* Mob, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSelfdualMob( pMob, env)
    return yy



#    int py_IsMeasureSubadditiveMob(double* Mob, struct fm_env* env)
def IsMeasureSubadditiveMob(Mob, env):
    trace( "int py_IsMeasureSubadditiveMob(double* Mob, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSubadditiveMob( pMob, env)
    return yy



#    int py_IsMeasureSubmodularMob(double* Mob, struct fm_env* env)
def IsMeasureSubmodularMob(Mob, env):
    trace( "int py_IsMeasureSubmodularMob(double* Mob, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSubmodularMob( pMob, env)
    return yy



#    int py_IsMeasureSuperadditiveMob(double* Mob, struct fm_env* env)
def IsMeasureSuperadditiveMob(Mob, env):
    trace( "int py_IsMeasureSuperadditiveMob(double* Mob, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSuperadditiveMob( pMob, env)
    return yy



#    int py_IsMeasureSupermodularMob(double* Mob, struct fm_env* env)
def IsMeasureSupermodularMob(Mob, env):
    trace( "int py_IsMeasureSupermodularMob(double* Mob, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSupermodularMob( pMob, env)
    return yy



#    int py_IsMeasureSymmetricMob(double* Mob, struct fm_env* env)
def IsMeasureSymmetricMob(Mob, env):
    trace( "int py_IsMeasureSymmetricMob(double* Mob, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureSymmetricMob( pMob, env)
    return yy



#    int py_IsMeasureKMaxitiveMob(double* Mob, struct fm_env* env)
def IsMeasureKMaxitiveMob(Mob, env):
    trace( "int py_IsMeasureKMaxitiveMob(double* Mob, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_IsMeasureKMaxitiveMob( pMob, env)
    return yy



#    void py_Mobius(double* v, double* out_MobVal, struct fm_env* env)
def Mobius(v, env):
    trace( "void py_Mobius(double* v, double* out_MobVal, struct fm_env* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_MobValnp, pout_MobVal = create_float_zeros_as_CFFI_double( env.m)
    fm.py_Mobius( pv, pout_MobVal, env)
    return pout_MobValnp



#    double py_Orness(double* Mob, struct fm_env* env)
def Orness(Mob, env):
    trace( "double py_Orness(double* Mob, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_Orness( pMob, env)
    return yy



#    double py_OWA(double* x, double* v, struct fm_env* env)
def OWA(x, v, env):
    trace( "double py_OWA(double* x, double* v, struct fm_env* env)")
    pxnp, px = convert_py_float_to_cffi( x)
    pvnp, pv = convert_py_float_to_cffi( v)
    yy = fm.py_OWA( px, pv, env)
    return yy



#    double py_WAM(double* x, double* v, struct fm_env* env)
def WAM(x, v, env):
    trace( "double py_WAM(double* x, double* v, struct fm_env* env)")
    pxnp, px = convert_py_float_to_cffi( x)
    pvnp, pv = convert_py_float_to_cffi( v)
    yy = fm.py_WAM( px, pv, env)
    return yy



#    void py_Zeta(double* Mob, double* out_v, struct fm_env* env)
def Zeta(Mob, env):
    trace( "void py_Zeta(double* Mob, double* out_v, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( env.m)
    fm.py_Zeta( pMob, pout_v, env)
    return pout_vnp



#    void py_dualMobKadd(int m, int length, int k, double* src, double* out_dest, struct fm_env* env)
def dualMobKadd(k, src, env):
    trace( "void py_dualMobKadd(int m, int length, int k, double* src, double* out_dest, struct fm_env* env)")
    psrcnp, psrc = convert_py_float_to_cffi( src)
    pout_destnp, pout_dest = create_float_zeros_as_CFFI_double( env.m)
    length = fm.py_fm_arraysize_kadd( env.n, k, env)
    fm.py_dualMobKadd( env.m, length, k, psrc, pout_dest, env)
    return pout_destnp, length



#    void py_Shapley2addMob(double* v, double* out_x, int n)
def Shapley2addMob(v, n):
    trace( "void py_Shapley2addMob(double* v, double* out_x, int n)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_xnp, pout_x = create_float_zeros_as_CFFI_double( n)
    fm.py_Shapley2addMob( pv, pout_x, n)
    return pout_xnp



#    void py_Banzhaf2addMob(double* v, double* out_x, int n)
def Banzhaf2addMob(v, n):
    trace( "void py_Banzhaf2addMob(double* v, double* out_x, int n)")
    pvnp, pv = convert_py_float_to_cffi( v)
    pout_xnp, pout_x = create_float_zeros_as_CFFI_double( n)
    fm.py_Banzhaf2addMob( pv, pout_x, n)
    return pout_xnp



#    double py_Choquet2addMob(double* x, double* Mob, int n)
def Choquet2addMob(x, Mob, n):
    trace( "double py_Choquet2addMob(double* x, double* Mob, int n)")
    pxnp, px = convert_py_float_to_cffi( x)
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_Choquet2addMob( px, pMob, n)
    return yy



#    int py_fm_arraysize(int n, int kint, struct fm_env* env)
def fm_arraysize(n, kint, env):
    trace( "int py_fm_arraysize(int n, int kint, struct fm_env* env)")
    yy = fm.py_fm_arraysize( n, kint, env)
    return yy

def fm_arraysize_kadd(n, kint, env):
    trace( "int py_fm_arraysize(int n, int kint, struct fm_env* env)")
    yy = fm.py_fm_arraysize_kadd( n, kint, env)
    return yy

#    int py_generate_fm_minplus(int num, int n, int kint, int markov, int option, double K, double* out_vv, struct fm_env* env)
def generate_fm_minplus(num, n, kint, markov, option, K, env):
    trace( "int py_generate_fm_minplus(int num, int n, int kint, int markov, int option, double K, double* out_vv, struct fm_env* env)")
    length = fm.py_fm_arraysize(n, kint, env)
    pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double( num * length)
    yy = fm.py_generate_fm_minplus( num, n, kint, markov, option, K, pout_vv, env)
    return yy, pout_vvnp, length



#    int py_generate_fm_2additive_convex(int num, int n,  double* out_vv)
def generate_fm_2additive_convex(num, n):
    trace( "int py_generate_fm_2additive_convex(int num, int n,  double* vv)")
    length = n * n
    pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double( num * length)
    yy = fm.py_generate_fm_2additive_convex( num, n, pout_vv)
    return yy, pout_vvnp, length



#    int py_generate_fm_2additive_convex_withsomeindependent(int num, int n, double* out_vv)
def generate_fm_2additive_convex_withsomeindependent(num, n):
    trace( "int py_generate_fm_2additive_convex_withsomeindependent(int num, int n, double* vv)")
    length = n * n
    pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double( num * length)
    yy = fm.py_generate_fm_2additive_convex_withsomeindependent( num, n, pout_vv)
    return yy, pout_vvnp, length



#    void py_prepare_fm_sparse(int n, int tupsize, int* tuples, struct fm_env_sparse* out_env)
def prepare_fm_sparse( n, tupsize):
    try:
        trace( "void py_prepare_fm_sparse(int n, int tupsize, int* tuples, struct fm_env_sparse* out_env)")
        ptuplesnp, ptuples = create_intc_zeros_as_CFFI_int( tupsize)
        pout_env_sparse = ffi.new( "struct fm_env_sparse *")
        fm.py_prepare_fm_sparse( n, tupsize, ptuples, pout_env_sparse)
        return pout_env_sparse
    except ValueError:
        raise



#    void py_free_fm_sparse( struct fm_env_sparse* env)
def free_fm_sparse(env_sparse):
    try:
        trace( "void py_free_fm_sparse( struct fm_env_sparse* env)")
        if( env_sparse == None): raise ValueError( "Env sparse not initialised") 
        fm.py_free_fm_sparse( env_sparse)
        return None
    except ValueError:
        raise


#    int py_tuple_cardinality_sparse(int i, struct fm_env_sparse* env)
def tuple_cardinality_sparse(i, env):
    trace( "int py_tuple_cardinality_sparse(int i, struct fm_env_sparse* env)")
    yy = fm.py_tuple_cardinality_sparse( i, env)
    return yy



#    int py_get_num_tuples(struct fm_env_sparse* env)
def get_num_tuples(env):
    trace( "int py_get_num_tuples(struct fm_env_sparse* env)")
    yy = fm.py_get_num_tuples( env)
    return yy



#    int py_get_sizearray_tuples(struct fm_env_sparse* env)
def get_sizearray_tuples(env):
    trace( "int py_get_sizearray_tuples(struct fm_env_sparse* env)")
    yy = fm.py_get_sizearray_tuples( env)
    return yy



#    int py_is_inset_sparse(int A, int card, int i, struct fm_env_sparse* env)
def is_inset_sparse(A, card, i, env):
    trace( "int py_is_inset_sparse(int A, int card, int i, struct fm_env_sparse* env)")
    yy = fm.py_is_inset_sparse( A, card, i, env)
    return yy



#    int py_is_subset_sparse(int A, int cardA, int B, int cardB, struct fm_env_sparse* env)
def is_subset_sparse(A, cardA, B, cardB, env):
    trace( "int py_is_subset_sparse(int A, int cardA, int B, int cardB, struct fm_env_sparse* env)")
    yy = fm.py_is_subset_sparse( A, cardA, B, cardB, env)
    return yy



#    double py_min_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)
def min_subset_sparse(x, n, S, cardS, env):
    trace( "double py_min_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)")
    pxnp, px = convert_py_float_to_cffi( x)
    yy = fm.py_min_subset_sparse( px, n, S, cardS, env)
    return yy



#    double py_max_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)
def max_subset_sparse(x, n, S, cardS, env):
    trace( "double py_max_subset_sparse(double* x, int n, int S, int cardS, struct fm_env_sparse* env)")
    pxnp, px = convert_py_float_to_cffi( x)
    yy = fm.py_max_subset_sparse( px, n, S, cardS, env)
    return yy



#    double py_ChoquetMob_sparse(double* x, int n, struct fm_env_sparse* env)
def ChoquetMob_sparse(x, env):
    trace( "double py_ChoquetMob_sparse(double* x, int n, struct fm_env_sparse* env)")
    n = len( x)
    pxnp, px = convert_py_float_to_cffi( x)
    yy = fm.py_ChoquetMob_sparse( px, n, env)
    return yy



#    void py_add_tuple_sparse(int tupsize, int* tuple, double v, struct fm_env_sparse* env)
def add_tuple_sparse(tuple, v, env):
    trace( "void py_add_tuple_sparse(int tupsize, int* tuple, double v, struct fm_env_sparse* env)")
    # ptuplenp, ptuple = convert_py_int_to_cffi( tuple)
    tupsize = len( tuple)
    ptuplenp, ptuple = convert_py_int_to_cffi( tuple)
    fm.py_add_tuple_sparse( tupsize, ptuple, v, env)



#    void py_ShapleyMob_sparse(double* out_v, int n, struct fm_env_sparse* env)
def ShapleyMob_sparse(n, env):
    trace( "void py_ShapleyMob_sparse(double* out_v, int n, struct fm_env_sparse* env)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( n)
    fm.py_ShapleyMob_sparse( pout_v, n, env)
    return pout_vnp



#    void py_BanzhafMob_sparse(double* out_v, int n, struct fm_env_sparse* env)
def BanzhafMob_sparse(n, env):
    trace( "void py_BanzhafMob_sparse(double* out_v, int n, struct fm_env_sparse* env)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( n)
    fm.py_BanzhafMob_sparse( pout_v, n, env)
    return pout_vnp




#    void py_populate_fm_2add_sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2, struct fm_env_sparse* env)
def populate_fm_2add_sparse(singletons, numpairs, pairs, indicesp1, indicesp2, env):
    trace( "void py_populate_fm_2add_sparse(double* singletons, int numpairs, double* pairs, int* indicesp1, int* indicesp2, struct fm_env_sparse* env)")
    psingletonsnp, psingletons = convert_py_float_to_cffi( singletons)
    ppairsnp, ppairs = convert_py_float_to_cffi( pairs)
    pindicesp1np, pindicesp1 = convert_py_int_to_cffi( indicesp1)
    pindicesp2np, pindicesp2 = convert_py_int_to_cffi( indicesp2)
    fm.py_populate_fm_2add_sparse( psingletons, numpairs, ppairs, pindicesp1, pindicesp2, env)



#    void py_add_pair_sparse(int i, int j, double v, struct fm_env_sparse* env)
def add_pair_sparse(i, j, v, env):
    trace( "void py_add_pair_sparse(int i, int j, double v, struct fm_env_sparse* env)")
    fm.py_add_pair_sparse( i, j, v, env)



#    void py_populate_fm_2add_sparse_from2add(int n, double* v, struct fm_env_sparse* env)
def populate_fm_2add_sparse_from2add(n, v, env):
    trace( "void py_populate_fm_2add_sparse_from2add(int n, double* v, struct fm_env_sparse* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    fm.py_populate_fm_2add_sparse_from2add( n, pv, env)



#    void py_expand_2add_full(double* out_v, struct fm_env_sparse* env)
def expand_2add_full(n, env):
    trace( "void py_expand_2add_full(double* out_v, struct fm_env_sparse* env)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( 2 ** n)
    fm.py_expand_2add_full( pout_v, env)
    return pout_vnp



#    void py_expand_sparse_full(double* v, struct fm_env_sparse* env)
def expand_sparse_full(v, env):
    trace( "void py_expand_sparse_full(double* v, struct fm_env_sparse* env)")
    pvnp, pv = convert_py_float_to_cffi( v)
    fm.py_expand_sparse_full( pv, env)



#    void py_sparse_get_singletons(int n, double* out_v, struct fm_env_sparse* env)
def sparse_get_singletons(n, env):
    trace( "void py_sparse_get_singletons(int n, double* out_v, struct fm_env_sparse* env)")
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( 2 ** n)
    fm.py_sparse_get_singletons( n, pout_v, env)
    return pout_vnp



#    int py_sparse_get_pairs(int* out_pairs, double* out_v, struct fm_env_sparse* env)
def sparse_get_pairs(n, env):
    trace( "int py_sparse_get_pairs(int* out_pairs, double* out_v, struct fm_env_sparse* env)")
    pout_pairsnp, pout_pairs = create_intc_zeros_as_CFFI_int( 2 * n * n)
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( 2 * n * n)
    yy = fm.py_sparse_get_pairs( pout_pairs, pout_v, env)
    return pout_pairsnp, pout_vnp



#    int py_sparse_get_tuples(int* out_tuples, double* out_v, struct fm_env_sparse* env)
def sparse_get_tuples(env):
    trace( "int py_sparse_get_tuples(int* out_tuples, double* out_v, struct fm_env_sparse* env)")
    n_tup = fm.py_get_num_tuples( env)
    size_tup = fm.py_get_sizearray_tuples( env) 
    pout_tuplesnp, pout_tuples = create_intc_zeros_as_CFFI_int( n_tup)
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( size_tup)
    yy = fm.py_sparse_get_tuples( pout_tuples, pout_v, env)
    return pout_tuplesnp, pout_vnp



#    int   py_generate_fm_2additive_convex_sparse(int n, struct fm_env_sparse* env)
def generate_fm_2additive_convex_sparse(n, env):
    trace( "int   py_generate_fm_2additive_convex_sparse(int n, struct fm_env_sparse* env)")
    yy = fm.py_generate_fm_2additive_convex_sparse( n, env)
    return yy



#    int   py_generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct fm_env_sparse* env)
def generate_fm_kadditive_convex_sparse(n, k, nonzero, env):
    trace( "int   py_generate_fm_kadditive_convex_sparse(int n, int k, int nonzero, struct fm_env_sparse* env)")
    yy = fm.py_generate_fm_kadditive_convex_sparse( n, k, nonzero, env)
    return yy



#    void py_Nonmodularityindex_sparse(double* out_w, int n, struct fm_env_sparse* env)
def Nonmodularityindex_sparse(n, env):
    trace( "void py_Nonmodularityindex_sparse(double* out_w, int n, struct fm_env_sparse* env)")
    pout_wnp, pout_w = create_float_zeros_as_CFFI_double( 2 ** n)
    fm.py_Nonmodularityindex_sparse( pout_w, n, env)
    return pout_wnp
    
    
# from version 5

def generate_fm_randomwalk( num, n , kint, markov, option, step, env, F):
    trace( "generate_fm_randomwalk( num, n , kint, markov, option, step, env, F)")
    try:
        global CB
        if (F != None) :
            CB = F
            F =  py_user_defined_measurecheck
            p_c_cb =  get_c_callback_function( F)
        else:
            p_c_cb = ffi.cast( "void *", 0)
            
               # Use CFFI type conversion
        # Retrieve C call-back function
        if ((option & 127) ==3) or ((option & 127)==5):
            length = fm.py_fm_arraysize_kadd(n, kint, env)
        else:
            length=pow(2,n)
        
        pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double( num * length)

        yy = fm.py_generate_fm_randomwalk(num, n, kint, markov, option, step, pout_vv, env, p_c_cb)
        return yy, pout_vvnp, length
        
    except ValueError:
        raise
        
def generate_fm_kinteractivedualconvex( num, n , kint, markov, step, env, F):
    trace( "generate_fm_kinteractivedualconvex( num, n , kint, markov, step, env, F)")
    try:
        global CB
        if (F != None) :
            CB = F
            F =  py_user_defined_measurecheck
            p_c_cb =  get_c_callback_function( F)
        else:
            p_c_cb = ffi.cast( "void *", 0)
            
               # Use CFFI type conversion
        # Retrieve C call-back function
        length = fm.py_fm_arraysize_kadd(n, kint, env)+n

        pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double( num * length)
        if(kint>n-2) :
            print("kint must be at most n-2")
            return 0, pout_vvnp, 0

        yy = fm.py_generate_fm_kinteractivedualconvex(num, n, kint, markov, length, step, pout_vv, env, p_c_cb)
        return yy, pout_vvnp, length
        
    except ValueError:
        raise


def generate_fm_kinteractivedualconcave( num, n , kint, markov, step, env, F):
    trace( "generate_fm_kinteractivedualconcave( num, n , kint, markov, step, env, F)")
    try:
        global CB
        if (F != None) :
            CB = F
            F =  py_user_defined_measurecheck
            p_c_cb =  get_c_callback_function( F)
        else:
            p_c_cb = ffi.cast( "void *", 0)
            
               # Use CFFI type conversion
        # Retrieve C call-back function
        

        length = fm.py_fm_arraysize_kadd(n, kint, env)+n

        pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double( num * length)
        if(kint>n-2) :
            print("kint must be at most n-2")
            return 0, pout_vvnp, 0

        yy = fm.py_generate_fm_kinteractivedualconcave(num, n, kint, markov, length, step, pout_vv, env, p_c_cb)
        return yy, pout_vvnp, length
        
    except ValueError:
        raise
        
def generate_fm_2additive_randomwalk2( num, n ,markov, option, step, F):
    trace( "generate_fm_2additive_randomwalk2( num, n ,markov, option, step, F)")
    try:
        global CB
        if (F != None) :
            CB = F
            F =  py_user_defined_measurecheck
            p_c_cb =  get_c_callback_function( F)
        else:
            p_c_cb = ffi.cast( "void *", 0)
            
               # Use CFFI type conversion
        # Retrieve C call-back function
        length = n*(n-1)/2+n

        pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double( num * length)

        yy = fm.py_generate_fm_2additive_randomwalk2(num, n, markov, option, step, pout_vv,  p_c_cb)
        return yy, pout_vvnp, int(length)
        
    except ValueError:
        raise



def generate_fm_2additive(num , n):
    trace( "int py_generate_fm_2additive(int num, int n,  double* vv)")
    length = (n * (n-1)/2+n)
    pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double(num* length)
    yy = fm.py_generate_fm_2additive( num, n, pout_vv)
    return yy, pout_vvnp, int(length)


def generateAntibuoyant(n, env):
    trace( "int py_GenerateAntibuoyant( int n,  double* vv)")
    length = pow(2,n)
    pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double( length)
    fm.py_GenerateAntibuoyant( pout_vv, env )
    return pout_vvnp
    
def generate_fm_belief(num, n, kadd, env):
    trace( "int py_generate_fm_belief(int num, int n,  double* vv)")
    length = py_fm_arraysize_kadd(n,kadd)
    pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double(num* length)
    yy=fm.py_generate_fm_belief( num, n, kadd, pout_vv,env)
    return yy,pout_vvnp,length
    

def generate_fm_balanced(num, n,  env):
    trace( "int py_generate_fm_balanced(int num, int n,  double* vv)")
    length = pow(2,n)
    pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double(num* length)
    yy=fm.py_generate_fm_balanced( num, n,  pout_vv, env)
    return yy,pout_vvnp,length
    


def generate_fm_sorting( num, n , markov, option,  env):
    trace( "int py_generate_fm_sorting( num, n , markov, option,  env)")
    try:
        length = pow(2,n)
        pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double( num * length)

        fm.py_generate_fm_sorting(num, n, markov, option,  pout_vv, env)
        return  pout_vvnp
        
    except ValueError:
        raise
        
        
        
def CheckMonotonicitySortMerge(n, v, env):
    trace( "int CheckMonotonicitySortMerge(n, v, indices, env)")
    pMobnp, pMob = convert_py_float_to_cffi( v)
    pout_indicesnp, pout_indices = create_float_zeros_as_CFFI_double(pow(2,n))
    yy = fm.py_CheckMonotonicitySortMerge( pMob,pout_indices, env)
    return yy, pout_indicesnp
    
    
def CheckMonotonicitySortInsert(n, v, indices, env):
    trace( "int py_CheckMonotonicitySortInsert(n, v, indices, env)")
    pMobnp, pMob = convert_py_float_to_cffi( v)
    pout_indicesnp, pout_indices = convert_py_float_to_cffi( indices )
    yy = fm.py_CheckMonotonicitySortInsert( pMob, pout_indices, env)
    return yy, pout_indicesnp
   
   
def CheckMonotonicitySimple(v, env):
    trace( "int py_CheckMonotonicitySimple(double* v, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( v)
    yy = fm.py_CheckMonotonicitySimple( pMob,  env)
    return yy

def CheckMonMob2additive2(v, n):
    trace( "int py_CheckMonMob2additive2(double* v, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( v)
    length=n*(n-1)+n
    out_indicesnp, temp = create_float_zeros_as_CFFI_double(length+1)
    yy = fm.py_CheckMonMob2additive2( pMob, n, length, temp)
    return yy

def CheckMonotonicityMob(v, len,  env):
    trace( "int py_CheckMonotonicityMob(double* Mob, len, struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( v)
    yy = fm.py_CheckMonotonicityMob( pMob, len,  env)
    return yy

def CheckConvexityMonMob(v,  len, env):
    trace( "int py_CheckConvexityMonMob(double* Mob, len , struct fm_env* env)")
    pMobnp, pMob = convert_py_float_to_cffi( v)
    yy = fm.py_CheckConvexityMonMob( pMob, len, env)
    return yy


def ConvertCoMob2Kinter(n, kint, len, v, fullmu, env):
    trace( "int py_ConvertCoMob2KinterCall(n, kint, len, v, fullmu, env)")
    pMobnp, pMob = convert_py_float_to_cffi( v)
    pout_munp, pout_mu= create_float_zeros_as_CFFI_double(n*n)
    fm.py_ConvertCoMob2KinterCall( n, kint, len, pout_mu, pMob, fullmu, env)
    return pout_munp


   
def ChoquetCoMobKInter(x, Mob, kint, len, env):
    trace( "double py_ChoquetCoMobKInter(double* x, double* Mob, int n)")
    pxnp, px = convert_py_float_to_cffi( x)
    pMobnp, pMob = convert_py_float_to_cffi( Mob)
    yy = fm.py_ChoquetCoMobKInter( px, pMob, kint, len, env)
    return yy


def FuzzyMeasureFit2Additive(datanum, n, options, indexlow, indexhihg, option1, orness, dataset):
    trace( "void FuzzyMeasureFit2Additive( datanum, n, options, indexlow, indexhihg, option1, orness, dataset)")
    len=n*(n-1)/2+n
    pout_vnp, pout_v = create_float_zeros_as_CFFI_double( len)
    pdatasetnp, pdataset = convert_py_float_to_cffi_cont( dataset)
    #poptionsnp, poptions = convert_py_int_to_cffi_cont( options)
    pindexlownp, pindexlow = convert_py_float_to_cffi_cont( indexlow)
    pindexhihgnp, pindexhihg = convert_py_float_to_cffi_cont( indexhihg)
   # poption1np, poption1 = convert_py_int_to_cffi_cont( option1)
    pornessnp, porness = convert_py_float_to_cffi_cont( orness)
    fm.py_fitting2additive( int(datanum), int(n), int(len),  pout_v, pdataset, int(options), pindexlow, pindexhihg, int(option1), porness)
    return pout_vnp


def generate_fm_minimals( num, n , markov, ratio, weights, env):
    trace( "int generate_fm_minimals( num, n , markov, ratio,  env)")
    try:
        ppW, pW = convert_py_float_to_cffi( weights) #can be None
        length = pow(2,n)
        pout_vvnp, pout_vv = create_float_zeros_as_CFFI_double( num * length)

        fm.py_generate_fm_minimals(num, n, markov, ratio, pW, pout_vv, env)
        return  pout_vvnp
        
    except ValueError:
        raise

def generate_fm_minimals_le( num, n , markov, ratio, weights, env):
    trace( "int generate_fm_minimals_le( num, n , markov, ratio,  env)")
    try:
        ppW, pW = convert_py_float_to_cffi( weights) #can be None
        length = pow(2,n)
        pout_vvnp, pout_vv = create_zeros_as_CFFI_uint64( num * length)
        # these are int_64
        fm.py_generate_fm_minimals_le(num, n, markov, ratio, pW, pout_vv, env)
        return  pout_vvnp
        
    except ValueError:
        raise
