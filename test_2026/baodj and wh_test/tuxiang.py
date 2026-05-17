import polars as pl
import matplotlib.pyplot as plt

def draw_chart():
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False

    df = pl.read_excel("temp/full_data.xlsx")
    df = df.with_columns(pl.col("月份").str.to_date("%Y-%m"))

    plt.figure(figsize=(12, 5))
    plt.plot(df["月份"], df["2"], marker="o", color="#127FCD", linewidth=2.5, label="插值完整月度数据")
    plt.title("月度数据插值完整趋势图", fontsize=15)
    plt.xlabel("月份")
    plt.ylabel("数值")
    plt.grid(alpha=0.3, linestyle="--")
    plt.legend()
    plt.tight_layout()

    plt.savefig("temp/chart.png", dpi=300)
    plt.close()
    print("✅ 成员B：折线图已生成 temp/chart.png")