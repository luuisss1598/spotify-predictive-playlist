import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
from dotenv import find_dotenv, load_dotenv
import os
import time


def csv_to_parquet(csv_file_path: str, parquet_file_path: str) -> str:
    start_time = time.time()
    df = pd.read_csv(csv_file_path)
    end_time = time.time()

    total_time = end_time - start_time

    # parquet_file_name = '_products.parquet'
    parquet_file_name = "/products.parquet"
    full_parquet_file_path: str = parquet_file_path + parquet_file_name
    table = pa.Table.from_pandas(df)
    pq.write_table(table, full_parquet_file_path)

    print(f"Total time taken to load data: {total_time}")

    print(df.head(n=100))

    return full_parquet_file_path


def load_parquet_to_s3_bucket(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    parquet_file_path: str,
    file_name: str,
) -> None:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1",
    )
    # region = s3.meta.region_name
    bucket_name = "products-details-summary"

    response = s3.upload_file(
        Filename=parquet_file_path, Bucket=bucket_name, Key=file_name
    )

    print(response)


def read_parquet_from_s3_bucket(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    s3_bucket_name: str,
    s3_parquet_file_path: str,
    file_name: str,
) -> pd.DataFrame:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1",
    )

    s3.download_file(
        Bucket=s3_bucket_name, Key=s3_parquet_file_path, Filename=file_name
    )

    df = pd.read_parquet(file_name)

    return df


def create_s3_bucket(aws_access_key_id: str, aws_secret_access_key: str) -> None:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1",
    )
    # region = s3.meta.region_name
    bucket_name = "products-details-summary"

    response = s3.create_bucket(Bucket=bucket_name)

    print(response)


def main() -> None:
    find_env_file_path = find_dotenv()
    load_dotenv(find_env_file_path)

    aws_access_key_id = os.getenv("aws_access_key_id")
    aws_secret_access_key = os.getenv("aws_secret_access_key")

    csv_file_path = "./data/raw_data/products.csv"
    parquet_file_path = "./data/raw_parquet"

    create_s3_bucket(
        aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key
    )
    full_parquet_file_path = csv_to_parquet(
        csv_file_path=csv_file_path, parquet_file_path=parquet_file_path
    )

    load_parquet_to_s3_bucket(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        parquet_file_path=full_parquet_file_path,
        file_name="products.parquet",
    )

    s3_parquet_file_path = "products.parquet"
    s3_bucket_name = "products-details-summary"
    to_local_file_name = "./data/raw_parquet/from_s3_products.parquet"
    df = read_parquet_from_s3_bucket(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        s3_bucket_name=s3_bucket_name,
        s3_parquet_file_path=s3_parquet_file_path,
        file_name=to_local_file_name,
    )

    print(df.head(n=100))

    print("\n")

    bytes_to_mb = 1024 * 1024
    products_csv_size: float = os.path.getsize(filename=csv_file_path) / bytes_to_mb
    products_parquet_size: float = (
        os.path.getsize(filename=f"{parquet_file_path}/products.parquet") / bytes_to_mb
    )
    products_parquet_size: float = (
        os.path.getsize(filename=to_local_file_name) / bytes_to_mb
    )

    print(f"Total size of local Products CSV file: {products_csv_size}")
    print(f"Total size of local Products Parquet file: {products_parquet_size}")
    print(f"Total size of s3 Products Parquet file: {products_parquet_size}")


if __name__ == "__main__":
    main()
