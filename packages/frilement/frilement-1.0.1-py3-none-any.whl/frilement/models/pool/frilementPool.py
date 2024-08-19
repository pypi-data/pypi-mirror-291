from pandas import DataFrame
from streamingpool import FIFOPool
from io import BufferedWriter
from os import makedirs
from os.path import getsize
from typing import Callable

from ...models.config.frilementConfig import FrilementConfig
from ...enums.fileFormat import FileFormat


class FrilementPool(FIFOPool[DataFrame]):
    """
    Async pool that will fragment DataFrames on multiple files
    """
    __result_file_base_name: str
    __result_file_format: FileFormat
    __config: FrilementConfig

    __current_cluster_number: int
    __current_file_number: int
    __result_writer: BufferedWriter | None
    __result_file_size: int
    __export_method: Callable

    def __init__(self, result_file_base_name: str, result_file_format: FileFormat, config: FrilementConfig) -> None:
        super().__init__()
        self.__result_file_base_name = result_file_base_name
        self.__result_file_format = result_file_format
        self.__config = config

        self.__current_cluster_number = 0
        self.__current_file_number = 0
        self.__result_writer = None  
        self.__export_method = FrilementPool.__get_df_export_method(result_file_format)

        if self.__export_method is None:
            raise Exception(f"Unsupporter file format '{result_file_format}'...")

    @staticmethod
    def __get_df_export_method(file_format: FileFormat) -> Callable | None:
        if file_format == FileFormat.CSV:
            return DataFrame.to_csv
        
        return None

    def __reset_writer(self):
        """
        Reset informations about result writer
        """
        if self.__result_writer is not None:
            self.__result_writer.close()
            self.__result_writer = None
            self.__current_file_number = 0

    def process_segment(self, segment: DataFrame) -> None:
        if self.__result_writer is None:
            path = self.__config.output_path / self.__result_file_base_name / (f"{self.__result_file_base_name}_{self.__current_cluster_number}" if self.__config.clustering_enabled else "")
            
            makedirs(path, exist_ok=True)

            file_path = path / (self.__result_file_base_name + (f"_{self.__current_cluster_number}" if self.__config.clustering_enabled else "") + f"_{self.__current_file_number}.{self.__result_file_format}")

            self.__export_method(
                DataFrame(columns=segment.columns),
                file_path,
                index = False,
                encoding = "utf-8"
            )

            self.__result_writer = open(file_path, "ab")
            self.__result_file_size = getsize(file_path)

            if self.__result_file_size > self.__config.max_result_file_size:
                self.clear_buffer()
                self.stop()
                raise Exception(f"The header of the file exceed the max result file size, please adjust config...")
        
        for index, row in segment.iterrows():
            row_bin = self.__export_method(row.to_frame().T, index=False, header=False).encode("utf-8")

            bin_len = len(row_bin)

            if self.__result_file_size + bin_len > self.__config.max_result_file_size:
                self.__reset_writer()
                self.__current_file_number += 1

                if self.__config.clustering_enabled and self.__current_file_number >= self.__config.max_file_amount_cluster:
                    self.__current_file_number = 0
                    self.__current_cluster_number += 1

                self.enqueue_segment(segment.iloc[index:])
            else:
                self.__result_writer.write(row_bin)
                self.__result_file_size += bin_len

    def dispose(self) -> None:
        self.__reset_writer()
        self.__current_cluster_number = 0
            