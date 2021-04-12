import pandas as pd

def quality_cuts(df):

    """
     This function removes numerical artifacts ( $\chi$2 < 0), inf and nan values from a data-frame object which includes proton and pion pairs for lambda
     reconstruction. It also applies quality cuts based on detector geometry. Full description could be found in
     https://docs.google.com/document/d/11f0ZKPW8ftTVhTxeWiog1g6qdsGgN1mlIE3vd5FHLbc/edit?usp=sharing

     Parameters

     ------------------

     df: dataframe
         dataframe to be cleaned

    """

    with pd.option_context('mode.use_inf_as_na', True):
        df = df.dropna()

    df = df.dropna()

    chi2_cut = (df['chi2geo'] > 0) & (df['chi2primpos'] > 0) & (df['chi2primneg'] > 0) &\
           (df['chi2topo'] > 0)
    mass_cut = (df['mass'] > 1.077)
    angle_cut = (df['cosinepos'] > 0) & (df['cosineneg']>0)
    coord_cut = (df['z'] > 0 ) & (abs(df['x']) < 50) & (abs(df['y']) < 50)
    dist_l_cut = (df['distance'] > 0) &  (df['distance'] < 100) &\
                     (df['l'] > 0 )  & (df['ldl'] > 0 ) & (abs(df['l']) < 80)

    pz_cut = (df['pz'] > 0)

    cuts = (chi2_cut) & (mass_cut) & (angle_cut) & (coord_cut) & (dist_l_cut) &\
    (pz_cut)

    return df[cuts]
