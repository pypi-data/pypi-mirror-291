from ..._data import Concordance, Dimension, Parameter

dimension = Dimension("data/", productcode="metal", atctivitycode="metal_production")

parameter = Parameter(["data/industry/metal"])

concordance = Concordance("data/")
