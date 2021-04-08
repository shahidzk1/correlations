def tree_importer(path,treename):

    """
    Import of root file by using uproot

    Parameters

    ----------

    path: str
          path to root file
    treename: str
           name of the tree to be analyzed
    """

    import uproot
    from concurrent.futures import ThreadPoolExecutor
    import pandas as pd
    executor = ThreadPoolExecutor(8)
    file = uproot.open(path+':'+treename+'', library='pd', decompression_executor=executor,
                                  interpretation_executor=executor).arrays(library='np',decompression_executor=executor,
                                  interpretation_executor=executor)
    df= pd.DataFrame(data=file)
    return df
