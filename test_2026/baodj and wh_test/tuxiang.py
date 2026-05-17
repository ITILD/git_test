import polars as pl
import matplotlib.pyplot as plt

# 假数据（list格式）
def get_fake_data():
    date_list = [
        "2024-01-01", "2024-02-01", "2024-04-01",
        "2024-05-01", "2024-07-01", "2024-08-01",
        "2024-10-01", "2024-11-01"
    ]
    value_list = [120, 132, 154, 161, 180, 190, 210, 225]
    return date_list, value_list

# 生成假数据Excel到 temp
def save_fake_data():
    date_list, value_list = get_fake_data()
    df = pl.DataFrame({
        "日期": date_list,
        "数值": value_list
    })
    df.write_excel("temp/fake_data.xlsx")
    print(" 假数据已保存到 temp/fake_data.xlsx")

# 绘制折线图 + 美化
def draw_chart():
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False

    df = pl.read_excel("temp/fake_data.xlsx")
    df = df.with_columns(pl.col("日期").cast(pl.Date))

    plt.figure(figsize=(12, 5), dpi=120)
    plt.plot(df["日期"], df["数值"], marker="o", color="#0099ff", linewidth=2.5, label="月度数据")
    
    plt.title("月度数据趋势图", fontsize=15)
    plt.xlabel("月份")
    plt.ylabel("数值")
    plt.grid(alpha=0.3, linestyle="--")
    plt.legend()
    plt.tight_layout()

    plt.savefig("temp/chart.png", dpi=300)
    plt.close()
    print(" 折线图已生成到 temp/chart.png")