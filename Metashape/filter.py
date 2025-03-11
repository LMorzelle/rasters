import pdal
pdal.__version__
import json
import pandas as pd
import numpy as np
import pdal
from pathlib import Path # KW_dense_cloud-22-58.las
import geopandas as gpd
from shapely.geometry import Point
from shapely import wkt
from osgeo import gdal
import rasterio
import rioxarray as rxr
from rasterio.features import shapes

def get_bin_statistics(ins, outs):

    if len(ins["X"]) == 0:
        return False

    outs["X"] = np.array(np.floor(np.min(ins["X"]))+1/2)
    outs["Y"] = np.array(np.floor(np.min(ins["Y"]))+1/2)
    outs["count"] = np.array(len(ins["X"])).astype(np.int8)
    outs["conf"] = (np.array(np.sum(ins["confidence"])/len(ins["X"]))).astype(np.float32)
    
    return True

def get_bin_statistics_without_conf(array, length=1):
    df = pd.DataFrame(array)
    metadata = {
        "bin_x": np.floor(df.loc[:,"X"].min())+length/2,
        "bin_y": np.floor(df.loc[:,"Y"].min())+length/2,
        "bin_count": len(array)
        #"bin_conf_sum": df.loc[:,"Confidence"].sum()
    }
    
    return pd.DataFrame([metadata])