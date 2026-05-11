from pydantic import BaseModel, ConfigDict, Field


class HouseFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    MSSubClass: int | None = None
    MSZoning: str | None = None
    LotFrontage: float | None = None
    LotArea: int | None = None
    Street: str | None = None
    Alley: str | None = None
    LotShape: str | None = None
    LandContour: str | None = None
    Utilities: str | None = None
    LotConfig: str | None = None
    LandSlope: str | None = None
    Neighborhood: str | None = None
    Condition1: str | None = None
    Condition2: str | None = None
    BldgType: str | None = None
    HouseStyle: str | None = None
    OverallQual: int | None = None
    OverallCond: int | None = None
    YearBuilt: int | None = None
    YearRemodAdd: int | None = None
    RoofStyle: str | None = None
    RoofMatl: str | None = None
    Exterior1st: str | None = None
    Exterior2nd: str | None = None
    MasVnrType: str | None = None
    MasVnrArea: float | None = None
    ExterQual: str | None = None
    ExterCond: str | None = None
    Foundation: str | None = None
    BsmtQual: str | None = None
    BsmtCond: str | None = None
    BsmtExposure: str | None = None
    BsmtFinType1: str | None = None
    BsmtFinSF1: float | None = None
    BsmtFinType2: str | None = None
    BsmtFinSF2: float | None = None
    BsmtUnfSF: float | None = None
    TotalBsmtSF: float | None = None
    Heating: str | None = None
    HeatingQC: str | None = None
    CentralAir: str | None = None
    Electrical: str | None = None
    first_flr_sf: float | None = Field(default=None, alias="1stFlrSF")
    second_flr_sf: float | None = Field(default=None, alias="2ndFlrSF")
    LowQualFinSF: float | None = None
    GrLivArea: float | None = None
    BsmtFullBath: float | None = None
    BsmtHalfBath: float | None = None
    FullBath: int | None = None
    HalfBath: int | None = None
    BedroomAbvGr: int | None = None
    KitchenAbvGr: int | None = None
    KitchenQual: str | None = None
    TotRmsAbvGrd: int | None = None
    Functional: str | None = None
    Fireplaces: int | None = None
    FireplaceQu: str | None = None
    GarageType: str | None = None
    GarageYrBlt: float | None = None
    GarageFinish: str | None = None
    GarageCars: float | None = None
    GarageArea: float | None = None
    GarageQual: str | None = None
    GarageCond: str | None = None
    PavedDrive: str | None = None
    WoodDeckSF: int | None = None
    OpenPorchSF: int | None = None
    EnclosedPorch: int | None = None
    three_ssn_porch: int | None = Field(default=None, alias="3SsnPorch")
    ScreenPorch: int | None = None
    PoolArea: int | None = None
    PoolQC: str | None = None
    Fence: str | None = None
    MiscFeature: str | None = None
    MiscVal: int | None = None
    MoSold: int | None = None
    YrSold: int | None = None
    SaleType: str | None = None
    SaleCondition: str | None = None


class PredictionResponse(BaseModel):
    predicted_price: float
