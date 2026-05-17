import polars as pl
import matplotlib.pyplot as plt
import os

def draw_chart():
    # 设置中文字体，增加后备字体
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "WenQuanYi Zen Hei", "Arial Unicode MS"]
    plt.rcParams["axes.unicode_minus"] = False

    input_path = "temp/full_data.xlsx"
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"找不到文件: {input_path}，请先运行 full_data.py")

    df = pl.read_excel(input_path)
    # 确保月份列是日期类型
    df = df.with_columns(pl.col("月份").str.to_date("%Y-%m"))

    plt.figure(figsize=(12, 5))
    plt.plot(df["月份"], df["2"], marker="o", color="#127FCD", linewidth=2.5, label="插值完整月度数据")
    plt.title("月度数据插值完整趋势图", fontsize=15)
    plt.xlabel("月份")
    plt.ylabel("数值")
    plt.grid(alpha=0.3, linestyle="--")
    plt.legend()
    plt.tight_layout()

    os.makedirs("temp", exist_ok=True)
    output_path = "temp/chart.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ 成员B：折线图已生成 {output_path}")

if __name__ == "__main__":
    draw_chart()