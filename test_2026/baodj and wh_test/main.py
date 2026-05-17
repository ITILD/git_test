from full_data import run_process
from tuxiang import draw_chart

if __name__ == "__main__":
    print("=== 项目开始运行 ===")
    try:
        run_process()
        draw_chart()
        print("=== 全部完成 ===")
    except Exception as e:
        print(f"❌ 运行出错: {e}")