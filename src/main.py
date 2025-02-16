from src.obfuscator import obfuscate_file
from src.utils import read_s3_file, write_s3_file, json_input_handler
from typing import Literal


def handle_file_obfuscation(
        json_string: str,
        if_output_different_format: bool = False,
        output_format: Literal['csv', 'json', 'parquet', None] = None,
        chunk_size: int = 5000,
        if_save_to_s3: bool = True):
    '''
    Process the file obfuscation

    Args:
        json_input (str): A json string contraining 2 pairs -
            "file_to_obfuscate" as a str and
            "pii_fields" as a list

        if_output_different_format (bool):
            If the output is in a different format as input,
            default to be False

        output_format (str): If if_output_different_format is True,
        which format to output, default to be None
        Currently support csv/ json/ parquet

        chunk_size (int): number of rows to process at a time, 5000 by default

        if_save_to_s3 (bool): If True, save the obfuscated file to S3.
                              Otherwise, return the byte-stream object
                              instead of saving to S3.
    '''
    try:
        s3_bucket, file_key, fields_list = json_input_handler(json_string)

        content_str, file_extension = read_s3_file(s3_bucket, file_key)

        if if_output_different_format:
            content_BytesIO = obfuscate_file(
                content_str, fields_list, file_extension,
                output_format, chunk_size)
        else:
            content_BytesIO = obfuscate_file(
                content_str, fields_list, file_extension,
                chunk_size=chunk_size)

        if if_save_to_s3:
            output_file_key = file_key.replace('new_data', 'processed_data')
            write_s3_file(s3_bucket, output_file_key, content_BytesIO)

            return ('Obfuscated file saved to s3://' +
                    f'{s3_bucket}/{output_file_key}')
        else:
            return content_BytesIO
    except Exception as e:
        raise Exception(str(e))
