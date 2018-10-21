'''
Created on 19-03-2012

@author: WZ
'''
from math import exp, tanh, pi, atan, sinh, cosh, pow

def ThresholdActivationFunction( x ):
    return ( x > 0.0 ) if 1.0 else 0.0 

def  LogisticActivationFunction( x ):
    """Logistic activation function."""
    return ( 1 / ( 1 + exp( -x ) ) )

def  LogisticDerivActivationFunction( x ):
    """Logistic activation derivative function."""
    return LogisticActivationFunction( x ) * ( 1 - LogisticActivationFunction( x ) )

def HiperbolicTangensActivationFunction( x ):
    """Hyperbolic tangent activation function."""
    return tanh( x )

def HiperbolicTangensDerivActivationFunction( x ):
    """Hyperbolic tangent activation derivative function."""
    return ( 1.0 - pow( tanh( x ), 2.0 ) )

def Kenue1ActivationFunction( x ):
    """Sigmoidal activation function proposed by Kenue."""
    return ( 2.0 / pi ) * atan( sinh( x ) );

def Kenue1DerivActivationFunction( x ):
    """Sigmoidal activation derivative function proposed by Kenue."""
    return ( 2.0 / pi ) * pow( cosh( x ), -1.0 );

def Kenue2ActivationFunction( x ):
    """Sigmoidal activation function proposed by Kenue (approach 2)."""
    return ( 2.0 / pi ) * ( tanh( x ) / cosh( x ) + atan( sinh( x ) ) );

def Kenue2DerivActivationFunction( x ):
    """Sigmoidal activation derivative function proposed by Kenue (approach 2)."""
    return ( 4.0 / pi ) * pow( pow( cosh( x ), -1.0 ), 3.0 );
