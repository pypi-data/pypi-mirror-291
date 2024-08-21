from .summarizer import BedrockSummarizer
from .structredExtraction import BedrockstructredExtraction
from .data_masking import BedrockDataMasking
from .nl2sql import BedrockNL2SQL
import os
from loguru import logger


# _instance = None


def get_instance(aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
    # global _instance
    # if _instance is None:
    _instance = BedrockSummarizer(aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)
    return _instance


def get_instance_extraction(aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
    # global _instance
    # if _instance is None:
    _instance = BedrockstructredExtraction(aws_access_key_id=aws_access_key_id,
                                           aws_secret_access_key=aws_secret_access_key,
                                           region_name=region_name)
    return _instance


def get_instance_Data_mask(aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
    # global _instance
    # if _instance is None:
    _instance = BedrockDataMasking(aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   region_name=region_name)
    return _instance


def get_instance_nl2sql(aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
    # global _instance
    # if _instance is None:
    _instance = BedrockNL2SQL(aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=region_name)
    return _instance


def nl2sql(nl_query, db_type, username, password, host,
           port, dbname, db_path=None, user_prompt=None,
           model_name=None, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
    """
       Converts a natural language query into an SQL query, executes it against the specified database,
       and returns the results in a user-friendly manner.

       Parameters:
       - nl_query (str): The natural language query provided by the user.
       - db_type (str): The type of the database (e.g., 'postgresql', 'mysql', 'sqlite').
       - username (str): The username used to authenticate with the database.
       - password (str): The password used to authenticate with the database.
       - host (str): The host address of the database.
       - port (int or str): The port number of the database.
       - dbname (str): The name of the database.
       - db_path (str, optional): The file path for SQLite database (optional, required if db_type is 'sqlite').
       - user_prompt (str, optional): The custom prompt to guide the NL2SQL conversion (optional).
       - model_name (str, optional): The name of the model to be used for NL2SQL conversion (optional).
       - aws_access_key_id (str, optional): AWS access key ID for accessing cloud-based resources (optional).
       - aws_secret_access_key (str, optional): AWS secret access key for accessing cloud-based resources (optional).
       - region_name (str, optional): AWS region name for accessing cloud-based resources (optional).

       Returns:
       - str or None: The answer to the user's natural language query as a string. If an error occurs, returns None.

    """
    instance = get_instance_nl2sql(aws_access_key_id, aws_secret_access_key, region_name)
    try:
        return instance.get_answer_from_db(db_type, nl_query, username, password, host,
                                           port, dbname, db_path, model_name, user_prompt)
    except Exception as e:
        user_friendly_error = instance._get_user_friendly_error(e)
        logger.error(user_friendly_error)
        return None


def summarize(input_content, user_prompt=None, model_name=None, aws_access_key_id=None,
              aws_secret_access_key=None, region_name=None):
    """
    Summarizes the given input content. The input can be text, a local file path, or an S3 file path.

    Parameters:
    input_content (str): The content to be summarized. This can be a text string, a local file path, or an S3 file path.
    user_prompt (str, optional): A custom prompt to be used for the summarization. If not provided, a default prompt will be used.
    model_name (str, optional): The name of the model to be used. If not provided, the default model will be used.
    aws_access_key_id (str, optional): AWS Access Key ID.
    aws_secret_access_key (str, optional): AWS Secret Access Key.
    region_name (str, optional): AWS region name for accessing cloud-based resources (optional).

    Returns:
    tuple: A tuple containing the summary text, input token count, output token count, and the cost of the operation.
    """
    instance = get_instance(aws_access_key_id, aws_secret_access_key, region_name)
    try:
        if os.path.exists(input_content):  # Check if input is a local file path
            return instance.summarize_file(input_content, user_prompt, model_name)
        elif input_content.startswith('s3://'):  # Check if input is an S3 file path
            return instance.summarize_s3_file(input_content, user_prompt, model_name)
        else:  # Assume input is text
            return instance.summarize_text(input_content, user_prompt, model_name)
    except Exception as e:
        user_friendly_error = instance._get_user_friendly_error(e)
        logger.error(user_friendly_error)
        return None, 0, 0, 0.0


def structredExtraction(input_content, user_prompt=None, model_name=None, aws_access_key_id=None,
                        aws_secret_access_key=None, region_name=None):
    """
    Extract the given input content. The input can be text, a local file path, or an S3 file path.

    Parameters:
    input_content (str): The content to be used for extraction. This can be a text string, a local file path, or an S3 file path.
    user_prompt (str, optional): A custom prompt to be used for the Extraction. If not provided, a default prompt will be used.
    model_name (str, optional): The name of the model to be used. If not provided, the default model will be used.
    aws_access_key_id (str, optional): AWS Access Key ID.
    aws_secret_access_key (str, optional): AWS Secret Access Key.
    region_name (str, optional): AWS region name for accessing cloud-based resources (optional).

    Returns:
    tuple: A tuple containing the Extracted entity, input token count, output token count, and the cost of the operation.
    """
    instance = get_instance_extraction(aws_access_key_id, aws_secret_access_key, region_name)
    try:
        if os.path.exists(input_content):  # Check if input is a local file path
            return instance.extract_file(input_content, user_prompt, model_name)
        elif input_content.startswith('s3://'):  # Check if input is an S3 file path
            return instance.extract_s3_file(input_content, user_prompt, model_name)
        else:  # Assume input is text
            return instance.extract_text(input_content, user_prompt, model_name)
    except Exception as e:
        user_friendly_error = instance._get_user_friendly_error(e)
        logger.error(user_friendly_error)
        return None, 0, 0, 0.0


def DataMasking(input_content, user_prompt=None, model_name=None, aws_access_key_id=None,
                aws_secret_access_key=None, region_name=None):
    """
    Extract the given input content. The input can be text, a local file path, or an S3 file path.

    Parameters:
    input_content (str): The content to be used for extraction. This can be a text string, a local file path, or an S3 file path.
    user_prompt (str, optional): A custom prompt to be used for the Extraction. If not provided, a default prompt will be used.
    model_name (str, optional): The name of the model to be used. If not provided, the default model will be used.
    aws_access_key_id (str, optional): AWS Access Key ID.
    aws_secret_access_key (str, optional): AWS Secret Access Key.
    region_name (str, optional): AWS region name for accessing cloud-based resources (optional).

    Returns:
    tuple: A tuple containing the Extracted entity, input token count, output token count, and the cost of the operation.
    """
    instance = get_instance_Data_mask(aws_access_key_id, aws_secret_access_key, region_name)
    try:
        if os.path.exists(input_content):  # Check if input is a local file path
            return instance.mask_file(input_content, user_prompt, model_name)
        elif input_content.startswith('s3://'):  # Check if input is an S3 file path
            return instance.mask_s3_file(input_content, user_prompt, model_name)
        else:  # Assume input is text
            return instance.mask_text(input_content, user_prompt, model_name)
    except Exception as e:
        user_friendly_error = instance._get_user_friendly_error(e)
        logger.error(user_friendly_error)
        return None, 0, 0, 0.0
