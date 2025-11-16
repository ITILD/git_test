import polars as pl
import datetime as dt
def main():
    df = pl.read_excel("temp/西红柿.xlsx")
    print(df)
if __name__ == "__main__":
    main()
