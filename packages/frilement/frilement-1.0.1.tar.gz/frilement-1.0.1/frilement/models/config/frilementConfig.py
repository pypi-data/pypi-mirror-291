from pathlib import Path


class FrilementConfig:
    """
    Class that contains all parameters to execute frilement's task
    """
    __output_path: Path
    __data_chunk_size: int
    __max_result_file_size: int
    __clustering_enabled: bool
    __max_file_amount_cluster: int
    __file_analyzer_chunk_size: int

    def __init__(self, output_path: str, data_chunk_size: int = 250e6, max_result_file_size: int = 250_000,
                clustering_enabled: bool = True, max_file_amount_cluster: int = 20, file_analyzer_chunk_size: int = 8192) -> None:
        self.__output_path = Path(output_path)
        self.__data_chunk_size = data_chunk_size
        self.__max_result_file_size = max_result_file_size
        self.__clustering_enabled = clustering_enabled
        self.__max_file_amount_cluster = max_file_amount_cluster
        self.__file_analyzer_chunk_size = file_analyzer_chunk_size

    @property
    def output_path(self) -> Path:
        """
        Path to the output folder
        """
        return self.__output_path
    
    @property
    def data_chunk_size(self) -> int:
        """
        Max amount of datas loaded in memory at a time
        """
        return self.__data_chunk_size
    
    @property
    def max_result_file_size(self) -> int:
        """
        Max size of a result file
        
        NB : Each file will have a size smaller or equals to that amount
        """
        return self.__max_result_file_size
    
    @property
    def clustering_enabled(self) -> bool:
        """
        Determins if file clustering is enabled
        """
        return self.__clustering_enabled
    
    @property
    def max_file_amount_cluster(self) -> int:
        """
        Max amount of file by cluster

        NB : Will only work if clustering is enabled
        """
        return self.__max_file_amount_cluster
    
    @property
    def file_analyzer_chunk_size(self) -> int:
        """
        Size of datas loaded for CSV delimiter analyzer
        """
        return self.__file_analyzer_chunk_size
