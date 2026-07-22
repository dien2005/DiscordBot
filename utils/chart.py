import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io


def create_exchange_chart(
    history: list[dict],
    base: str,
    target: str
) -> io.BytesIO:
    """Vẽ biểu đồ lịch sử tỷ giá, trả về ảnh dạng bytes."""

    times = [row["thoi_gian"] for row in history]
    rates = [float(row["rate"]) for row in history]

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#2b2d31")  
    ax.set_facecolor("#383a40")

    # Vẽ đường
    ax.plot(times, rates, color="#5865f2", linewidth=2, marker="o", markersize=4)
    ax.fill_between(range(len(rates)), rates, alpha=0.2, color="#5865f2")

    # Style
    ax.set_title(
        f"Tỷ giá {base}/{target}",
        color="white", fontsize=14, fontweight="bold", pad=15
    )
    ax.set_ylabel(target, color="white")
    ax.tick_params(colors="white", labelsize=8)
    ax.spines[:].set_color("#4e5058")

    # Format trục x 
    step = max(1, len(times) // 6)
    ax.set_xticks(range(0, len(times), step))
    ax.set_xticklabels(
        [times[i] for i in range(0, len(times), step)],
        rotation=30, ha="right", color="white"
    )

    # Min/Max annotation
    min_val = min(rates)
    max_val = max(rates)
    min_idx = rates.index(min_val)
    max_idx = rates.index(max_val)

    ax.annotate(
        f"Min: {min_val:,.2f}",
        xy=(min_idx, min_val),
        xytext=(min_idx, min_val * 0.998),
        color="#ed4245", fontsize=8, fontweight="bold"
    )
    ax.annotate(
        f"Max: {max_val:,.2f}",
        xy=(max_idx, max_val),
        xytext=(max_idx, max_val * 1.001),
        color="#57f287", fontsize=8, fontweight="bold"
    )

    ax.grid(color="#4e5058", linestyle="--", alpha=0.5)
    plt.tight_layout()

    # Xuất ra bytes
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=120, facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


def create_weather_chart(
    history: list[dict],
    city: str
) -> io.BytesIO:
    """Vẽ biểu đồ nhiệt độ & độ ẩm theo thời gian."""

    times = [row["thoi_gian"] for row in history]
    temps = [float(row["temperature"]) for row in history]
    humids = [float(row["humidity"]) for row in history]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.patch.set_facecolor("#2b2d31")

    # -- Nhiệt độ --
    ax1.set_facecolor("#383a40")
    ax1.plot(temps, color="#fee75c", linewidth=2, marker="o", markersize=4)
    ax1.fill_between(range(len(temps)), temps, alpha=0.2, color="#fee75c")
    ax1.set_title(
        f"Thời tiết {city}",
        color="white", fontsize=14, fontweight="bold", pad=15
    )
    ax1.set_ylabel("Nhiệt độ (°C)", color="white")
    ax1.tick_params(colors="white", labelsize=8)
    ax1.spines[:].set_color("#4e5058")
    ax1.grid(color="#4e5058", linestyle="--", alpha=0.5)

    # -- Độ ẩm --
    ax2.set_facecolor("#383a40")
    ax2.plot(humids, color="#5865f2", linewidth=2, marker="o", markersize=4)
    ax2.fill_between(range(len(humids)), humids, alpha=0.2, color="#5865f2")
    ax2.set_ylabel("Độ ẩm (%)", color="white")
    ax2.tick_params(colors="white", labelsize=8)
    ax2.spines[:].set_color("#4e5058")
    ax2.grid(color="#4e5058", linestyle="--", alpha=0.5)

    # Trục x chung
    step = max(1, len(times) // 6)
    ax2.set_xticks(range(0, len(times), step))
    ax2.set_xticklabels(
        [times[i] for i in range(0, len(times), step)],
        rotation=30, ha="right", color="white"
    )

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=120, facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf