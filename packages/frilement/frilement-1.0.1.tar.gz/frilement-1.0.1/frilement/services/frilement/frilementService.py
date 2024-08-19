from ..IO.fileService import FileService
from ...models.pool.frilementPool import FrilementPool
from ...models.config.frilementConfig import FrilementConfig
from ...enums.fileFormat import FileFormat


class FrilementService:
    def frilement(file_path: str, config: FrilementConfig, output_file_format: FileFormat | None = None) -> None:
        """
        Fragment specified file

        Args:
            files_path (str | list[str]): The file to fragment
            config (FrilementConfig): The app config
        """
        iterator, file_format = FileService.create_reader(file_path, config)

        with FrilementPool("d", file_format if output_file_format is None else output_file_format, config) as p:
            for segment in iterator:
                pd_df = segment.compute()
                p.enqueue_segment(pd_df)

    def frilements(files_path: list[str], config: FrilementConfig, output_file_format: FileFormat) -> None:
        """
        Fragment specified files

        Args:
            files_path (str | list[str]): The files to fragment
            config (FrilementConfig): The app config
        """
        pool = None
        
        with FrilementPool("d", output_file_format, config) as p:
            for file_path in files_path:
                iterator, _ = FileService.create_reader(file_path, config)

                for segment in iterator:
                    p.enqueue_segment(segment.compute())