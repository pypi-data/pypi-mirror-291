import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import bonsai_ipcc

TEST_DATA_PATH = Path(os.path.dirname(__file__)) / "data/"

from bonsai_ipcc._sequence import Sequence
from bonsai_ipcc.industry.metal import elementary as elem
from bonsai_ipcc.industry.metal._data import concordance as conc
from bonsai_ipcc.industry.metal._data import dimension as dim
from bonsai_ipcc.industry.metal._data import parameter as par

bonsai_ipcc.industry.metal.dimension.agent_type = pd.DataFrame(
    {"code": ["a", "b"], "description": ["test a", "test b"]}
).set_index(["code"])

bonsai_ipcc.industry.metal.parameter.m_agent = pd.DataFrame(
    {
        "year": [2019, 2019, 2019, 2019, 2019],
        "region": ["DE", "DE", "DE", "IT", "DE"],
        "product": [
            "ferrosilicon_45perc_si",
            "silicon_metal",
            "ferrosilicon_45perc_si",
            "ferrosilicon_45perc_si",
            "ferrosilicon_45perc_si",
        ],
        "agent_type": ["a", "b", "b", "b", "b"],
        "property": ["def", "def", "def", "def", "max"],
        "value": [100.0, 50.0, 50.0, 50.0, 1000000.0],
        "unit": ["t/yr", "t/yr", "t/yr", "t/yr", "t/yr"],
    }
).set_index(["year", "region", "product", "agent_type", "property"])

bonsai_ipcc.industry.metal.parameter.ef_agent = pd.DataFrame(
    {
        "year": [2019, 2019, 2019, 2019],
        "region": ["DE", "DE", "IT", "IT"],
        "agent_type": ["a", "b", "a", "b"],
        "property": ["def", "def", "def", "def"],
        "value": [1.0, 2.0, 50.0, 50.0],
        "unit": ["t/t", "t/t", "t/t", "t/t"],
    }
).set_index(["year", "region", "agent_type", "property"])


def test_get_dimension_levels_one(
    tables=["m_agent", "ef_agent"],
    uncert="def",
    year=2019,
    region="DE",
    product="silicon_metal",
):

    seq = Sequence(dim, par, elem, conc, uncert="def")
    l = seq.get_dimension_levels(year, region, product, uncert=uncert, table=tables[0])

    value = 0.0
    for a in l:
        seq.read_parameter(
            name=tables[0],
            table=tables[0],
            coords=[year, region, product, a],
        )
        seq.read_parameter(
            name=tables[1],
            table=tables[1],
            coords=[year, region, a],
        )
        value += seq.elementary.co2_in_agent_tier2_(
            m=seq.step.m_agent.value, ef=seq.step.ef_agent.value
        )
    assert l == ["b"]
    assert value == 100.0


def test_get_dimension_levels_multiple(
    tables=["m_agent", "ef_agent"],
    uncert="def",
    year=2019,
    region="DE",
    product="ferrosilicon_45perc_si",
):

    seq = Sequence(dim, par, elem, conc, uncert="def")
    l = seq.get_dimension_levels(year, region, product, uncert=uncert, table=tables[0])

    value = 0.0
    for a in l:
        seq.read_parameter(
            name=tables[0],
            table=tables[0],
            coords=[year, region, product, a],
        )
        seq.read_parameter(
            name=tables[1],
            table=tables[1],
            coords=[year, region, a],
        )
        value += seq.elementary.co2_in_agent_tier2_(
            m=seq.step.m_agent.value, ef=seq.step.ef_agent.value
        )
    assert l == ["a", "b"]
    assert value == 200.0


def test_metadata(volume="industry", chapter="chemical", paramter="pp_i"):
    par_metadata = bonsai_ipcc.IPCC.metadata(volume, chapter, paramter)
    assert par_metadata["name"] == f"par_{paramter}"


def test_to_frames_bonsai():
    my_ipcc = bonsai_ipcc.IPCC()

    d = {
        "year": [2006, 2006, 2006, 2006, 2006, 2006, 2006, 2006, 2006, 2006],
        "region": ["GB", "GB", "GB", "GB", "GB", "GB", "GB", "GB", "GB", "GB"],
        "product": [
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
        ],
        "feedstocktype": [
            "natural_gas",
            "natural_gas",
            "natural_gas",
            "natural_gas",
            "natural_gas",
            "naphta",
            "naphta",
            "naphta",
            "naphta",
            "naphta",
        ],
        "property": [
            "def",
            "min",
            "max",
            "abs_min",
            "abs_max",
            "def",
            "min",
            "max",
            "abs_min",
            "abs_max",
        ],
        "value": [
            10000,
            1000,
            110000,
            0.0,
            np.inf,
            1,
            0.9,
            1.1,
            0.0,
            np.inf,
        ],
        "unit": [
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
        ],
    }
    fa_i_k = pd.DataFrame(d).set_index(
        ["year", "region", "product", "feedstocktype", "property"]
    )
    my_ipcc.industry.chemical.parameter.fa_i_k = fa_i_k

    s = my_ipcc.industry.chemical.sequence.tier1_co2_fa(
        year=2006, region="GB", product="methanol", uncertainty="def"
    )
    df = s.to_frames(bonsai=True)
    assert df["bonsai"]["use"].loc[0]["product"] == "natural_gas"
    assert df["bonsai"]["use"].loc[1]["product"] == "naphta"
    assert df["bonsai"]["use"].loc[0]["value"] == 10000.0
    assert df["bonsai"]["use"].loc[1]["value"] == 1.0
    assert pd.isna(df["bonsai"]["use"].loc[0]["standard_deviation"]) == True
    assert pd.isna(df["bonsai"]["use"].loc[1]["standard_deviation"]) == True


def test_to_frames_bonsai_montecarlo():
    my_ipcc = bonsai_ipcc.IPCC()

    d = {
        "year": [2006, 2006, 2006, 2006, 2006, 2006, 2006, 2006, 2006, 2006],
        "region": ["GB", "GB", "GB", "GB", "GB", "GB", "GB", "GB", "GB", "GB"],
        "product": [
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
            "methanol",
        ],
        "feedstocktype": [
            "natural_gas",
            "natural_gas",
            "natural_gas",
            "natural_gas",
            "natural_gas",
            "naphta",
            "naphta",
            "naphta",
            "naphta",
            "naphta",
        ],
        "property": [
            "def",
            "min",
            "max",
            "abs_min",
            "abs_max",
            "def",
            "min",
            "max",
            "abs_min",
            "abs_max",
        ],
        "value": [
            10000,
            1000,
            110000,
            0.0,
            np.inf,
            1,
            0.9,
            1.1,
            0.0,
            np.inf,
        ],
        "unit": [
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
            "t/year",
        ],
    }
    fa_i_k = pd.DataFrame(d).set_index(
        ["year", "region", "product", "feedstocktype", "property"]
    )
    my_ipcc.industry.chemical.parameter.fa_i_k = fa_i_k

    s = my_ipcc.industry.chemical.sequence.tier1_co2_fa(
        year=2006, region="GB", product="methanol", uncertainty="monte_carlo"
    )
    df = s.to_frames(bonsai=True)
    assert df["bonsai"]["use"].loc[0]["product"] == "natural_gas"
    assert df["bonsai"]["use"].loc[1]["product"] == "naphta"
    assert abs((24931.436 - df["bonsai"]["use"].loc[0]["value"]) / 24931.436) <= 0.25
    assert abs((0.992 - df["bonsai"]["use"].loc[1]["value"]) / 0.992) <= 0.25
    assert pd.isna(df["bonsai"]["use"].loc[0]["standard_deviation"]) == False
    assert pd.isna(df["bonsai"]["use"].loc[1]["standard_deviation"]) == False
