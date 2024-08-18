"""Tests for sliderule parquet support."""

import pytest
from pathlib import Path
import numpy
import geopandas
import pyarrow.parquet as pq
import os
import os.path
import json
import ctypes
import sliderule
from sliderule import icesat2

TESTDIR = Path(__file__).parent

@pytest.mark.network
class TestParquet:
    def test_atl06(self, init):
        resource = "ATL03_20190314093716_11600203_005_01.h5"
        region = sliderule.toregion(os.path.join(TESTDIR, "data/dicksonfjord.geojson"))
        parms = { "poly": region['poly'],
                  "cnf": "atl03_high",
                  "ats": 20.0,
                  "cnt": 10,
                  "len": 40.0,
                  "res": 20.0,
                  "maxi": 1,
                  "output": { "path": "testfile1.parquet", "format": "parquet", "open_on_complete": True } }
        gdf = icesat2.atl06p(parms, resources=[resource])
        metadata = pq.read_metadata("testfile1.parquet")
        sliderule_metadata = ctypes.create_string_buffer(metadata.metadata[b'sliderule']).value.decode('ascii')
        metadata_dict = json.loads(sliderule_metadata)
        os.remove("testfile1.parquet")
        assert init
        assert len(gdf) == 957
        assert len(gdf.keys()) == 17
        assert gdf["rgt"].iloc[0] == 1160
        assert gdf["cycle"].iloc[0] == 2
        assert gdf['segment_id'].describe()["min"] == 405231
        assert gdf['segment_id'].describe()["max"] == 405902
        assert metadata_dict["recordinfo"]["time"] == "time", f'invalid time column: {metadata_dict["recordinfo"]["time"]}'
        assert metadata_dict["recordinfo"]["x"] == "longitude", f'invalid x column: {metadata_dict["recordinfo"]["x"]}'
        assert metadata_dict["recordinfo"]["y"] == "latitude", f'invalid y column: {metadata_dict["recordinfo"]["y"]}'

    def test_atl06_non_geo(self, init):
        resource = "ATL03_20190314093716_11600203_005_01.h5"
        region = sliderule.toregion(os.path.join(TESTDIR, "data/dicksonfjord.geojson"))
        parms = { "poly": region['poly'],
                  "cnf": "atl03_high",
                  "ats": 20.0,
                  "cnt": 10,
                  "len": 40.0,
                  "res": 20.0,
                  "maxi": 1,
                  "output": { "path": "testfile2.parquet", "format": "parquet", "open_on_complete": True, "as_geo": False } }
        gdf = icesat2.atl06p(parms, resources=[resource])
        os.remove("testfile2.parquet")
        assert init
        assert len(gdf) == 957
        assert len(gdf.keys()) == 18
        assert gdf["rgt"].iloc[0] == 1160
        assert gdf["cycle"].iloc[0] == 2
        assert gdf['segment_id'].describe()["min"] == 405231
        assert gdf['segment_id'].describe()["max"] == 405902

    def test_atl03(self, init):
        resource = "ATL03_20190314093716_11600203_005_01.h5"
        region = sliderule.toregion(os.path.join(TESTDIR, "data/dicksonfjord.geojson"))
        parms = { "poly": region['poly'],
                  "cnf": "atl03_high",
                  "ats": 20.0,
                  "cnt": 10,
                  "len": 40.0,
                  "res": 20.0,
                  "maxi": 1,
                  "output": { "path": "testfile3.parquet", "format": "parquet", "open_on_complete": True } }
        gdf = icesat2.atl03sp(parms, resources=[resource])
        os.remove("testfile3.parquet")
        assert init
        assert len(gdf) == 190491
        assert len(gdf.keys()) == 22
        assert gdf["rgt"].iloc[0] == 1160
        assert gdf["cycle"].iloc[0] == 2
        assert gdf['segment_id'].describe()["min"] == 405231
        assert gdf['segment_id'].describe()["max"] == 405902

    def test_atl06_index(self, init):
        resource = "ATL03_20181017222812_02950102_005_01.h5"
        region = sliderule.toregion(os.path.join(TESTDIR, "data/grandmesa.geojson"))
        parms = {
            "poly": region["poly"],
            "srt": icesat2.SRT_LAND,
            "cnf": icesat2.CNF_SURFACE_HIGH,
            "ats": 10.0,
            "cnt": 10,
            "len": 40.0,
            "res": 20.0,
            "output": { "path": "testfile4.parquet", "format": "parquet", "open_on_complete": True } }
        gdf = icesat2.atl06p(parms, resources=[resource])
        os.remove("testfile4.parquet")
        assert init
        assert len(gdf) == 265
        assert gdf.index.values.min() == numpy.datetime64('2018-10-17T22:31:17.350047744')
        assert gdf.index.values.max() == numpy.datetime64('2018-10-17T22:31:19.582527744')

    def test_atl03_index(self, init):
        resource = "ATL03_20181017222812_02950102_005_01.h5"
        region = sliderule.toregion(os.path.join(TESTDIR, "data/grandmesa.geojson"))
        parms = {
            "poly": region["poly"],
            "srt": icesat2.SRT_LAND,
            "cnf": icesat2.CNF_SURFACE_HIGH,
            "ats": 10.0,
            "cnt": 10,
            "len": 40.0,
            "res": 20.0,
            "output": { "path": "testfile5.parquet", "format": "parquet", "open_on_complete": True } }
        gdf = icesat2.atl03sp(parms, resources=[resource])
        os.remove("testfile5.parquet")
        assert init
        assert len(gdf) == 20642
        assert gdf.index.values.min() == numpy.datetime64('2018-10-17T22:31:17.349347328')
        assert gdf.index.values.max() == numpy.datetime64('2018-10-17T22:31:19.582347520')

    def test_atl08_ancillary(self, init):
        # Boreal Tiles (in WGS84)
        boreal_tiles = geopandas.read_file(os.path.join(TESTDIR, 'data/boreal_tiles_v004_model_ready.gpkg')).to_crs(4326)

        # Ancillary Fields
        ancillary_fields = ["canopy/h_canopy_uncertainty","h_dif_ref","msw_flag","sigma_topo","segment_landcover","canopy/segment_cover","segment_snowcover","terrain/h_te_uncertainty"]
        ancillary_outputs = [field[field.find("/")+1:] for field in ancillary_fields]

        # SlideRule ATL08/PhoREAL Parameters
        parms = {
            "poly": sliderule.toregion(boreal_tiles.geometry[0])["poly"],
            "t0": f'2020-06-01T00:00:00Z',
            "t1": f'2020-09-30T00:00:00Z',
            "srt": icesat2.SRT_LAND,
            "len": 30,
            "res": 30,
            "pass_invalid": True,
            "atl08_class": ["atl08_ground", "atl08_canopy", "atl08_top_of_canopy"],
            "atl08_fields": ancillary_fields,
            "phoreal": {"binsize": 1.0, "geoloc": "center", "above_classifier": True, "use_abs_h": False, "send_waveform": False},
            "output": {
                "path": "testfile6.parquet",
                "format": "parquet",
                "as_geo": True,
                "ancillary": ancillary_outputs,
                "open_on_complete": True
            }
        }

        # Make Parquet Processing Request
        atl08_pq = icesat2.atl08p(parms, resources=['ATL03_20200906053544_11130802_006_02.h5'], keep_id=True)

        # Make DataFrame Processing Request
        del parms["output"]
        atl08_df = icesat2.atl08p(parms, resources=['ATL03_20200906053544_11130802_006_02.h5'], keep_id=True)

        # Sort Data Frames
        pq = atl08_pq.sort_values('extent_id')
        df = atl08_df.sort_values('extent_id')

        # Clean up
        os.remove("testfile6.parquet")

        # Compare Data Frames
        for i in range(len(ancillary_fields)):
            anc_field = ancillary_fields[i]
            anc_output = ancillary_outputs[i]
            pq_col = pq[anc_output]
            df_col = df[anc_field]
            num_mismatches = 0
            for k in range(len(df_col)):
                if pq_col.iloc[k] != df_col.iloc[k]:
                    num_mismatches += 1
            assert num_mismatches == 0, f'there were mismatches in {anc_field}'

    def test_atl06_csv(self, init):
        resource = "ATL03_20190314093716_11600203_005_01.h5"
        region = sliderule.toregion(os.path.join(TESTDIR, "data/dicksonfjord.geojson"))
        parms = { "poly": region['poly'],
                  "cnf": "atl03_high",
                  "ats": 20.0,
                  "cnt": 10,
                  "len": 40.0,
                  "res": 20.0,
                  "maxi": 1,
                  "output": { "path": "", "format": "", "open_on_complete": True, "as_geo": False } }

        # create parquet file
        parms["output"]["path"] = "testfile7.parquet"
        parms["output"]["format"] = "parquet"
        gdf_from_parquet = icesat2.atl06p(parms, resources=[resource], keep_id=True)
        os.remove("testfile7.parquet")

        # create csv file
        parms["output"]["path"] = "testfile7.csv"
        parms["output"]["format"] = "csv"
        gdf_from_csv = icesat2.atl06p(parms, resources=[resource], keep_id=True)
        os.remove("testfile7.csv")
        os.remove("testfile7_metadata.json")

        # sort values
        gdf_from_parquet = gdf_from_parquet.sort_values('extent_id')
        gdf_from_csv = gdf_from_csv.sort_values('extent_id')

        # checks
        assert init
        assert len(gdf_from_parquet) == 957
        assert len(gdf_from_parquet.keys()) == 18, f'keys are {list(gdf_from_parquet.keys())}'
        assert len(gdf_from_csv) == 957
        assert len(gdf_from_csv.keys()) == 19, f'keys are {list(gdf_from_csv.keys())}' # time column counts as a key
        columns_to_check = ["dh_fit_dx","n_fit_photons","longitude"]
        for column in columns_to_check:
            for row in range(len(gdf_from_parquet)):
                parquet_val = gdf_from_parquet[column].iloc[row]
                csv_val = gdf_from_csv[column].iloc[row]
                assert abs(parquet_val - csv_val) < 0.0001, f'mismatch in column <{column}>: {parquet_val} != {csv_val}'


    def test_atl06_feather(self, init):
        resource = "ATL03_20190314093716_11600203_005_01.h5"
        region = sliderule.toregion(os.path.join(TESTDIR, "data/dicksonfjord.geojson"))
        parms = { "poly": region['poly'],
                  "cnf": "atl03_high",
                  "ats": 20.0,
                  "cnt": 10,
                  "len": 40.0,
                  "res": 20.0,
                  "maxi": 1,
                  "output": { "path": "", "format": "", "open_on_complete": True, "as_geo": False } }

        # create parquet file
        parms["output"]["path"] = "testfile8.parquet"
        parms["output"]["format"] = "parquet"
        gdf_from_parquet = icesat2.atl06p(parms, resources=[resource], keep_id=True)
        os.remove("testfile8.parquet")

        # create feather file
        parms["output"]["path"] = "testfile8.feather"
        parms["output"]["format"] = "feather"
        gdf_from_feather = icesat2.atl06p(parms, resources=[resource], keep_id=True)
        print(gdf_from_feather)
        os.remove("testfile8.feather")
        os.remove("testfile8_metadata.json")

        # sort values
        gdf_from_parquet = gdf_from_parquet.sort_values('extent_id')
        gdf_from_feather = gdf_from_feather.sort_values('extent_id')

        # checks
        assert init
        assert len(gdf_from_parquet) == 957
        assert len(gdf_from_parquet.keys()) == 18, f'parquet keys are {list(gdf_from_parquet.keys())}'
        assert len(gdf_from_feather) == 957
        assert len(gdf_from_feather.keys()) == 19, f'fetaher keys are {list(gdf_from_feather.keys())}' # parquet treats time as an index, where feather treats time as a regular column
        columns_to_check = ["dh_fit_dx","n_fit_photons","longitude"]
        for column in columns_to_check:
            for row in range(len(gdf_from_parquet)):
                parquet_val = gdf_from_parquet[column].iloc[row]
                feather_val = gdf_from_feather[column].iloc[row]
                assert abs(parquet_val - feather_val) < 0.0001, f'mismatch in column <{column}>: {parquet_val} != {feather_val}'



### TODO: for CSV and Feather, check that the metadata files are created