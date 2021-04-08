import pandas as pd

def quality_cuts(df):
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
