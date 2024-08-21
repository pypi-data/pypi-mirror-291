
import pandas as pd
import numpy as np
import itertools
import statsmodels.api as sm
from utils import dedupe, remove_all, combine_all


## I referred to the code in the link below :
## https://github.com/owkin/PyDESeq2/blob/main/pydeseq2/utils.py

def check_count_data(count_data) :
    
    """
    Parameters
    ----------
    count_data : pandas.DataFrame
        Raw counts.
    """
    
    if isinstance(count_data, pd.DataFrame) :  
        if count_data.isna().any().any() :
            raise ValueError("Missing values are not allowed.")  
        elif not set(count_data.dtypes) <= {np.dtype('int64'), np.dtype('float64')} :
            raise ValueError("Only numbers are allowed.")
        elif len(set(count_data.columns)) != len(count_data.columns) :
            raise ValueError('Same column names are not allowed.')
        elif len(set(count_data.index)) != len(count_data.index) :
            raise ValueError('Same row names are not allowed.')
    else :
        raise ValueError('count_data must be pandas.DataFrame.')
    
    if ((count_data % 1 != 0).any() | (count_data < 0).any()).any() :
        raise ValueError("Only positive integers(or 0) are alllowed")   
    elif (count_data.sum(axis=0) == 0).any() or (count_data.sum(axis=1) == 0).any() :
        raise ValueError('There is a row or column with a sum of 0.')
        

# after check_count_data
def check_metadata(metadata, count_data) :
    
    """
    Parameters
    ----------
    metadata : pandas.DataFrame
        Sample metadata.
    
    count_data : pandas.DataFrame
        Raw counts.
    """
    
    if isinstance(metadata, pd.DataFrame) : 
        if metadata.isna().any().any() :
            raise ValueError("Missing values are not allowed.")
        elif len(set(metadata.columns)) != len(metadata.columns) :
            raise ValueError('Same column names are not allowed.')
        elif len(set(metadata.index)) != len(metadata.index) :
            raise ValueError('Same row names are not allowed.')
        elif set(metadata.index) != set(count_data.columns) :
            raise ValueError('The samples in metadata and the samples in count_data must be the same.')
    else :
        raise ValueError('metadata must be pandas.DataFrame.')
        
    for colname in metadata.columns :
        if '~' in colname or '+' in colname or ':' in colname :
            raise ValueError("Any column name of metadata must not contain '~', '+', ':'")
            
            
# after check_metadata
def obtain_design_factors(design, metadata) :
    
    """
    Parameters
    ----------
    design : str
        Design formula.
    
    metadata : pandas.DataFrame
        Sample metadata.
        
    Returns
    -------
    list
        Column names of metadata to be used as design factors.
    """
    
    assert design.strip().startswith('~'), 'The design formula must start with tilde(~).'
    
    table = design.maketrans({'~' : ' ', '+' : ' '})
    design_factors = design.translate(table).split(' ')
    design_factors = remove_all(design_factors, '')
    
    if design_factors == [] : 
        raise ValueError('There are no design factors.')
        
    for i in range(len(design_factors)) :
        factor = design_factors[i]
        if ':' in factor :
            inter = factor.split(':')
            inter = [factor.strip() for factor in inter]
            design_factors[i] = tuple(inter)
            if len(inter) != 2 or len(set(inter)) != 2 :
                raise ValueError('An interaction term must contain only two different factors.')

    if len(dedupe(design_factors)) != len(design_factors) :
        raise ValueError('Same design terms are not allowed.')
        
    for factor in design_factors :
        if type(factor) == tuple :
            inter = factor
            factor1, factor2 = inter
            if (factor2, factor1) in design_factors :
                raise ValueError('Same design terms are not allowed')
            elif factor1 not in design_factors or factor2 not in design_factors :
                raise ValueError('There is a factor with interaction that does not belong to the design factors.')
        else :
            if factor not in metadata.columns :
                raise ValueError('There is a design factor that does not belong to columns of metadata.')
    
    return design_factors


# after obtain_design_factors
def obtain_design_matrix(design_factors, metadata) :
    
    """
    Parameters
    ----------
    design_factors : list
        Design factors.
    
    metadata : pandas.DataFrame
        Sample metadata.
        
    Returns
    -------
    pandas.DataFrame
        A Dataframe with experiment design informatiion. 
    """
           
    total =[]
    inters = []
    for factor in design_factors :
        if type(factor) == tuple :
            inters.append(factor)
        else :
            total.append(factor)

    non_inters = total
    for factor in dedupe(combine_all(inters)) :
        non_inters = remove_all(non_inters, factor)
    
    design_matrix = metadata[non_inters]
    design_matrix = pd.get_dummies(design_matrix, dtype='int', drop_first=True)
    
    if inters != [] :
        for inter in inters :
            factor1, factor2 = inter 
            dm_factor1 = pd.get_dummies(metadata[factor1], dtype='int', drop_first=True)
            dm_factor2 = pd.get_dummies(metadata[factor2], dtype='int', drop_first=True)
            dm_inter = pd.DataFrame(index = dm_factor1.index)
            for level1, level2 in itertools.product(dm_factor1.columns, dm_factor2.columns) :
                dm_inter['{}_{}_and_{}_{}'.format(factor1, level1, factor2, level2)] = dm_factor1[level1] * dm_factor2[level2]
            dm_inter = pd.concat([dm_factor1, dm_factor2, dm_inter], axis=1)
            design_matrix = pd.concat([design_matrix, dm_inter], axis=1)
            
    design_matrix = sm.add_constant(design_matrix)
    design_matrix.columns.values[0] = 'intercept'
    
    return design_matrix


def check_contrast(contrast, design_factors, metadata) :
    
    """
    Parameters
    ----------
    contrast : list
        A list in the form of [factor of interest, treat, control].
    
    design_factors : list
        Design factors.
    
    metadata : pandas.DataFrame
        Sample metadata.
    """
    
    assert type(contrast) == list, 'contrast must be a list.'

    if len(contrast) != 3 :
        raise ValueError("contrast must be length of 3.")
    else :
        factor, treat, control = contrast[0], contrast[1], contrast[2]   
        
    levels = dedupe(metadata[factor])
    
    if control == treat :
        raise ValueError("control and treat must be different.")
    elif control not in levels or treat not in levels :
        raise ValueError("control and treat must belong to the levels of factor of interest.")
        

# after check_contrast
def obtain_contrast_vec(contrast, design_matrix) : 
    
    """
    Parameters
    ----------
    contrast : list
        A list in the form of [factor of interest, treat, control].
    
    design_matrix : pandas.DataFrame
        Design matrix.
        
    Returns
    -------
    numpy.ndarray
        Vector encoding the contrast.
    """
    
    factor, treat, control = contrast[0], contrast[1], contrast[2]   
    
    design_levels = design_matrix.columns
    contrast_vec = pd.Series(0, index=design_levels)
    
    control_level = '{}_{}'.format(factor, control)
    treat_level = '{}_{}'.format(factor, treat)
    if control_level in design_levels and treat_level not in design_levels :
        contrast_vec['{}_{}'.format(factor, control)] = -1
    elif treat_level in design_levels and control_level not in design_levels :
        contrast_vec['{}_{}'.format(factor, treat)] = -1
    elif control_level in design_levels and treat_level in design_levels :
        contrast_vec['{}_{}'.format(factor, control)] = -1
        contrast_vec['{}_{}'.format(factor, treat)] = 1
    else :
        raise ValueError('Invalid contrast.')
    
    return np.array(contrast_vec)
    
    