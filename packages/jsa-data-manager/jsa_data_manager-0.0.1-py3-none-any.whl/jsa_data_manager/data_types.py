import dataclasses
import datetime
from enum import StrEnum
from typing import Literal

import pandas
import pydantic
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

# from pydantic import BaseModel as PydanticBaseModel


class TimeStampColumnMetaData(BaseModel):
    index_column_number: int
    index_column_name: str
    start_column_number: int
    start_column_name: str
    end_column_number: int
    end_column_name: str


class TimeSeriesColumnEntryMetaData(BaseModel):
    column_number: int
    column_name: str
    unit: str
    # optional
    description: str | None = None
    tags: list[str] | None = None
    min: float | None = None
    max: float | None = None
    sum: float | None = None


# @dataclass(kw_only=True)
# class TimeSeriesColumnEntryMetaData:
#     column_number: int
#     column_name: str
#     unit: str
#     # optional
#     description: str | None = "Electricity"
#     tags: list[str] | None = None
#     min: float | None = None
#     max: float | None = None
#     sum: float | None = None


class DataSourceTypes(StrEnum):
    SOFTWARE_SOURCE = "SoftwareSource"
    DATA_SOURCE = "DataSource"


class DataSource(BaseModel):
    source_type: Literal[DataSourceTypes.DATA_SOURCE]
    source_name: str
    user_name: str
    reference: str  # URL, doi or other reference to the data set
    guid: str


# @dataclass(kw_only=True)
# class DataSource:
#     source_name: SMARD
#     description: https://www.smard.de/page/home/marktdaten/78?marketDataAttributes=%7B%22resolution%22:%22hour%22,%22from%22:1717970400000,%22to%22:1718920799999,%22moduleIds%22:%5B1004066,1001226,1001225,1004067,1004068,1001228,1001223,1004069,1004071,1004070,1001227,5000410,6000411,2005097%5D,%22selectedCategory%22:1,%22activeChart%22:false,%22style%22:%22color%22,%22categoriesModuleOrder%22:%7B%7D,%22region%22:%22DE%22%7D
#     user_name: k-schulze
#     guid: 530cd955-a392-4c48-8355-f7753ac3a3e3


class SoftwareSource(BaseModel):
    source_type: Literal[DataSourceTypes.SOFTWARE_SOURCE]
    software_name: str
    version: str  # 2.2.1
    user_name: (
        str  # Your Linux User Name on the cluster that was used to create the data
    )
    guid: str


# @dataclass(kw_only=True)
# class SoftwareSource:
#     software_name="FINE"
#     version: "2.2.1"
#     user_name: j-belina
#     run_guid: "1f2e2503-d0db-4736-97f2-c1e504b8dbcb"


class TimeSeriesStandards(StrEnum):
    V1_0 = "JSA TimeSeriesStandard 1.0"


class TimeSeriesFileMetaDataWODataFrame(BaseModel):
    name: str
    data_source: DataSource | SoftwareSource
    time_stamp_column_meta_data: TimeStampColumnMetaData
    column_list: list[TimeSeriesColumnEntryMetaData]
    delimiter: Literal[","]
    data_format_standard: Literal[TimeSeriesStandards.V1_0]


# @dataclass(config={"arbitrary_types_allowed": True})
class TimeSeriesFileMetaData(BaseModel):
    name: str
    data_frame: pandas.DataFrame = Field(exclude=True, title="data_frame")
    data_source: DataSource | SoftwareSource
    time_stamp_column_meta_data: TimeStampColumnMetaData
    column_list: list[TimeSeriesColumnEntryMetaData]
    delimiter: Literal[","]
    data_format_standard: Literal[TimeSeriesStandards.V1_0]

    class Config:
        # Allows not validated datatypes like pandas data frame
        arbitrary_types_allowed = True


# @dataclass(kw_only=True)
# class TimeSeriesFileMetaData:
#     name = "Private Household Profile 2022"
#     data_frame: pandas.DataFrame
#     data_source: SoftwareSource
#     time_stamp_column_meta_data: TimeStampColumnMetaData
#     column_list: list[TimeSeriesColumnEntryMetaData]
#     delimiter = ","
#     data_format_standard= "JSA TimeSeriesStandard 1.0"
