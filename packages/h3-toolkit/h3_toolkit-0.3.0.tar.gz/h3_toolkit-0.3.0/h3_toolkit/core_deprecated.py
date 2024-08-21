# """
# A core module for h3_toolkit

# .. module:: core

# .. moduleauthor:: Ian Huang

# """

# from __future__ import annotations
# from enum import Enum
# from typing import Literal, Callable, Optional
# import logging

# import polars as pl
# import h3ronpy.polars
# import geopandas as gpd

# from h3_toolkit.hbase.client import HBaseClient
# from h3_toolkit.aggregation.strategy import SumAggregation, AvgAggregation, CountAggregation, SumAggregationUp, AvgAggregationUp
# # from h3_toolkit.aggregation.aggregator import _sum, _avg, _count, _major, _percentage
# # from h3_toolkit.aggregation.aggregator_up import _sum_agg, _avg_agg
# from h3_toolkit.processing.geom_processor import geom_to_wkb, wkb_to_cells


# # TODO: 將重複的邏輯抽取出來

# class H3Aggregator:
#     def __init__(self):
#         self.strategy:Callable[[pl.DataFrame, ]] = None
#         self.target_cols:list[str] = []
#         self.agg_col: str | None = None
#         self.geometry_col:str = None
#         self.hex_id:str = None
#         self.resolution:int = 12

#     def _apply_strategy(self, df: pl.DataFrame) -> pl.DataFrame:
#         # 可以不指定strategy，不指定strategy就直接回傳hexegon中心點對應到的值
#         if self.strategy is None:
#             return df
#             # raise ValueError("Aggregation strategy must be set before processing data")
#         return  self.strategy.apply(df, self.target_cols, self.agg_col)

#     def sum(self, target_cols: list[str], agg_col: str) -> H3Aggregator:
#         """This function is used to divide the value equally of target columns based on the aggregation column

#         Args:
#             target_cols (list[str]): The columns to be aggregated
#             agg_col (str): The column to be aggregated by, usually is a boundary
#         Returns:
#             H3Aggregator: The H3Aggregator object
#         """
#         self.strategy = SumAggregation()
#         self.target_cols = target_cols
#         self.agg_col = agg_col
#         return self
    
#     def avg(self, target_cols: list[str], agg_col=None) -> H3Aggregator:
#         self.strategy = AvgAggregation()
#         self.target_cols = target_cols
#         return self
    
#     def count(self, target_cols: list[str], agg_col=None) -> H3Aggregator:
#         self.strategy = CountAggregation()
#         self.target_cols = target_cols
#         return self
    
#     def set_resolution(self, resolution: int) -> H3Aggregator:
#         self.resolution = resolution
#         return self
    
#     def set_geometry(self, geometry_col: str=None) -> H3Aggregator:
#         """
#         要處理地理空間資料之前一定要set_geometry
#         """
#         self.geometry_col = geometry_col
#         return self
    
#     # TODO: 好像要刪除???
#     # def set_hexegon(self, hex_col: str=None) -> H3Aggregator:
#     #     """
#     #     要傳入的如果是hex_id，就要set_hexegon
#     #     """
#     #     self.hex_col = hex_col
#     #     return self

#     def set_target_cols(self, target_cols: list[str]) -> H3Aggregator:
#         self.target_cols = target_cols
#         return self
    
#     def process(self, data: gpd.GeoDataFrame | pl.DataFrame)-> pl.DataFrame:
#         if isinstance(data, gpd.GeoDataFrame):
#             logging.info("Converting GeoDataFrame to polars.DataFrame")
#             data = geom_to_wkb(data, self.geometry_col)

#         selected_cols = []
#         if self.agg_col:
#             selected_cols.append(self.agg_col)
#         selected_cols.extend(self.target_cols)

#         logging.info(f"Start converting data to h3 cells in resolution {self.resolution}")
#         result = (
#             data
#             .fill_nan(0)
#             .lazy()
#             .pipe(wkb_to_cells, self.resolution, self.geometry_col, selected_cols) # convert geometry to h3 cells
#             .pipe(self._apply_strategy) # apply the aggregation strategy
#             .select(  # Convert the cell(unit64) to string
#                 pl.col('cell').h3.cells_to_string().alias('hex_id'),
#                 pl.exclude('cell')
#             )
#             .collect(streaming=True)
#         )
#         logging.info(result.head(5))
#         logging.info(f"Successfully converting data to h3 cells with resolution {self.resolution}")

#         return result

# class H3AggregatorUp:
#     def __init__(self):
#         self.client:HBaseClient = None
#         self.strategy:Callable[[pl.DataFrame, ]] = None
#         self.target_cols:list[str] = []
#         self.agg_col:Optional[str] = None
#         self.geometry_col:str = 'geometry'
#         self.resolution_source:int = 12
#         self.resolution_target:int = 7

#     def set_client(self, client:HBaseClient) -> H3AggregatorUp:
#         self.client = client
#         return self
    
#     def set_resolution_source(self, resolution: int) -> H3AggregatorUp:
#         self.resolution_source = resolution
#         return self
    
#     def set_resolution_target(self, resolution: int) -> H3AggregatorUp:
#         self.resolution_target = resolution
#         return self
    
#     def set_geometry(self, geometry_col: str) -> H3AggregatorUp:
#         self.geometry_col = geometry_col
#         return self

#     def _apply_strategy(self, df: pl.DataFrame) -> pl.DataFrame:
#         if self.strategy is None:
#             raise ValueError("Aggregation strategy must be set before processing data") 
#         return  self.strategy.apply(df, self.target_cols, self.agg_col)
            
#     def sum(self, target_cols: list[str], agg_col=None) -> H3AggregatorUp:
#         self.strategy = SumAggregationUp()
#         self.target_cols = target_cols
#         return self
    
#     def avg(self, target_cols: list[str], agg_col=None) -> H3AggregatorUp:
#         self.strategy = AvgAggregationUp()
#         self.target_cols = target_cols
#         return self

#     def fetch_hbase_data(self, 
#                          table_name:str, 
#                          column_family:str,
#                          column_qualifier: list[str],
#                          data: pl.DataFrame | gpd.GeoDataFrame,
#         ) -> H3AggregatorUp:

#         """
#         data只需傳入geometry的資訊即可，需要去hbase抓資料, based on geometry的hex_id
#         """

#         data = data if isinstance(data, pl.DataFrame) else geom_to_wkb(data, self.geometry_col)

#         if not self.client:
#             raise ValueError("HBase client must be set before fetching data, use `set_client()` to set the client")
        
#         rowkeys = (
#             data
#             .fill_nan(0) 
#             .lazy() 
#             .pipe(wkb_to_cells, self.resolution_source, self.geometry_col) # convert geometry to h3 cells
#             .select(
#                 pl.col('cell')
#                 .h3.cells_to_string()
#                 .unique()
#                 .alias('hex_id'), # scale down to resolution 12
#             )
#             .collect(streaming=True)
#         )
#         self.data = self.client.fetch_data(
#             table_name=table_name,
#             cf=column_family,
#             cq_list=column_qualifier,
#             rowkeys=rowkeys['hex_id'].to_list(),
#         )
#         return self

#     def process(self) -> pl.DataFrame:

#         result = (
#             self.data
#             .lazy()
#             .with_columns(
#                 # 根據hex_id做resolution的轉換
#                 pl.col('hex_id')
#                 .h3.cells_parse()
#                 .h3.change_resolution(self.resolution_target)
#                 .alias('cell')
#             )
#             .pipe(self._apply_strategy)
#             .select(
#                 pl.col('cell')
#                     .h3.cells_to_string()
#                     .alias('hex_id'),
#                 pl.exclude('cell'))
#             .collect(streaming=True)
#         )
#         return result



# # class AggFunc(Enum):
# #     """
# #     5 ways to aggregate the data
# #     """
# #     SUM = 'sum'
# #     AVG = 'avg'
# #     COUNT = 'count'
# #     MAJOR = 'major'
# #     PERCENTAGE = 'percentage'

# # # TODO: Deprecated function
# # def vector_to_cell(
# #     data: pl.DataFrame | gpd.GeoDataFrame,
# #     agg_func: Literal['sum', 'avg', 'count', 'major', 'percentage'],
# #     target_cols: list[str],
# #     agg_col: Optional[str] = None,
# #     geometry_col: str = 'geometry_wkb',
# #     resolution: int = 12,
# # )->pl.DataFrame:
# #     """
# #     Args:
# #         data: pl.DataFrame | gpd.GeoDataFrame, the input data
# #         agg_func: Literal['sum', 'avg', 'count', 'major', 'percentage'], the aggregation function
# #         target_cols: list[str], the columns to be aggregated
# #         agg_cols: Optional[list[str]], the columns to be aggregated by, usually is a boundary, must to have if agg_func is 'sum'
# #         geometry_col: str, the geometry column name
# #         resolution: int, the h3 resolution
# #     Returns:
# #         pl.DataFrame, the aggregated target data in h3 cells 
# #     """

# #     selected_cols:list[str] = [agg_col] + target_cols if agg_col else target_cols

# #     if isinstance(data, gpd.GeoDataFrame):
# #         """
# #         convert GeoDataFrame to polars.DataFrame
# #         """
# #         logging.info("Converting GeoDataFrame to polars.DataFrame")
# #         data = geom_to_wkb(data)

# #     aggregation_func: dict[AggFunc, list[Callable[..., pl.DataFrame]]] = {
# #         AggFunc.SUM.value: lambda df: _sum(df, target_cols, agg_col),
# #         AggFunc.AVG.value: lambda df: _avg(df, target_cols),
# #         AggFunc.COUNT.value: lambda df: _count(df, target_cols, include_nan=True),
# #         AggFunc.MAJOR.value: _major,
# #         AggFunc.PERCENTAGE.value: _percentage,
# #     }

# #     func = aggregation_func.get(agg_func)
# #     logging.info(f"======Start converting the data to h3 cells with resolution {resolution}======")
# #     # resolution 12 （基底resolution），aggregate後存入hbase
    
# #     result = (
# #         data
# #         .fill_nan(0) 
# #         .lazy() 
# #         .pipe(wkb_to_cells, resolution, selected_cols, geometry_col) # convert geometry to h3 cells
# #         .pipe(func) # aggregate the data
# #         .select(  # Convert the cell(unit64) to string
# #             pl.col('cell')
# #             .h3.cells_to_string().alias('hex_id'),
# #             pl.exclude('cell')
# #         )
# #         .collect(streaming=True)
# #     )
# #     logging.info(result.head(5))
# #     logging.info(f"======Finish converting the data to h3 cells with resolution {resolution}======")

# #     return result

# # # TODO: Deprecated function
# # def vector_to_cell_scale_up(
# #     client: HBaseClient,
# #     table_name:str,
# #     column_family:str,
# #     column_qualifier: list[str],
# #     data: pl.DataFrame | gpd.GeoDataFrame,
# #     agg_func: Literal['sum', 'avg', 'count', 'major', 'percentage'],
# #     geometry_col: str = 'geometry_wkb',
# #     resolution_source: int = 12,
# #     resolution_target: int = 7,
# # )->pl.DataFrame:  
# #     """
# #     Args:
# #         client: HBaseClient, the hbase client
# #         table_name: str, the table name in hbase
# #         column_family: str, the column family in hbase ex: 'demographic', 'economic'
# #         column_qualifier: list[str], the column qualifier in hbase ex: ['p_cnt', 'h_cnt', 'm_cnt', 'f_cnt']
# #         data: pl.DataFrame | gpd.GeoDataFrame, the input data, represent the geometry boundary
# #         agg_func: Literal['sum', 'avg', 'count', 'major', 'percentage'], the aggregation function
# #         geometry_col: str, the geometry column name
# #         resolution: int, the h3 resolution

# #     Returns:
# #         pl.DataFrame, the aggregated target data in h3 cells 
# #     """
# #     # target_cols = [f"{target_cols}" for target_cols in target_cols]
# #     # target_cols = [f"{target_cols}_{agg_func}" for target_cols in target_cols]


# #     # get the r12 cells (rowkeys)
# #     rowkeys_df = (
# #         data
# #         .fill_nan(0) 
# #         .lazy() 
# #         .pipe(wkb_to_cells, resolution_source, geometry_col) # convert geometry to h3 cells
# #         .select(
# #             pl.col('cell')
# #             .h3.change_resolution(resolution_source)
# #             .h3.cells_to_string()
# #             .unique()
# #             .alias('hex_id'), # scale down to resolution 12
# #         )
# #         .collect(streaming=True)
# #     )

# #     logging.info(f"======Start getting data from hbase======")
# #     # call hbase api to get the data based on the r12 cells
# #     data = client.fetch_data(
# #         table_name = table_name,
# #         cf = column_family,
# #         cq_list = column_qualifier,
# #         rowkeys = rowkeys_df['hex_id'].to_list(),
# #     )
# #     logging.info(f"======Successfully get data from hbase======")

# #     aggregation_func: dict[AggFunc, list[Callable[..., pl.DataFrame]]] = {
# #         AggFunc.SUM.value: lambda df: _sum_agg(df, column_qualifier),
# #         AggFunc.AVG.value: lambda df: _avg_agg(df, column_qualifier),
# #         AggFunc.COUNT.value: lambda df: _sum_agg(df, column_qualifier),
# #         AggFunc.MAJOR.value: _major,
# #         AggFunc.PERCENTAGE.value: _percentage,
# #     }

# #     func = aggregation_func.get(agg_func)


# #     logging.info(f"======Start scaling up the data to h3 cells with resolution {resolution_target}======")
# #     result = (
# #         data
# #         .lazy()
# #         .with_columns(
# #             pl.col('hex_id')
# #             .h3.cells_parse()
# #             .h3.change_resolution(resolution_target)
# #             .alias('cell')
# #         )
# #         .pipe(func)
# #         .select(  # Convert the cell(unit64) to string
# #             pl.col('cell')
# #             .h3.cells_to_string().alias('hex_id'),
# #             pl.exclude('cell')
# #         )
# #         .collect(streaming=True)
# #     )

# #     return result