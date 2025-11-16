import polars as pl
import datetime as dt
def main():
    ex_1=read_and_process_excel("temp/西红柿.xlsx")


def read_and_process_excel(file_path: str) -> pl.DataFrame:
    df = pl.read_excel(file_path)
    result = df.to_dicts()
    return result

if __name__ == "__main__":
    main()







