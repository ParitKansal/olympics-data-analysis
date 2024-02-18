import pandas as pd
def preprocess(df, region_df):
    # filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    df = df.drop(df[df['Year'] == 1906].index)

    # simplify region_df
    region_df.loc[region_df['NOC'] == 'ANZ', 'region'] = 'Australasia'
    region_df.loc[region_df['NOC'] == 'HKG', 'region'] = 'Hong Kong (China)'
    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    df['Gold'] = df['Gold'].astype('int')
    df['Silver'] = df['Silver'].astype('int')
    df['Bronze'] = df['Bronze'].astype('int')
    return df