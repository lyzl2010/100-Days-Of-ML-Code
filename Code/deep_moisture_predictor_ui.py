"""Static mock-up for the deep learning moisture prediction interface."""

from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from typing import Iterable

APP_BG = "#08141f"
PANEL_BG = "#102538"
SECTION_BG = "#132c42"
ACCENT = "#2eccff"
TEXT_PRIMARY = "#f3f8ff"
TEXT_SECONDARY = "#89a9c6"
CARD_BORDER = "#1f3a50"


@dataclass
class Metric:
    label: str
    value: str
    unit: str | None = None

    def render(self, parent: tk.Widget) -> None:
        row = tk.Frame(parent, bg=SECTION_BG)
        row.pack(fill="x", padx=12, pady=4)
        tk.Label(
            row,
            text=self.label,
            font=("Microsoft YaHei", 11),
            fg=TEXT_SECONDARY,
            bg=SECTION_BG,
        ).pack(side="left")
        value_text = self.value if self.unit is None else f"{self.value} {self.unit}"
        tk.Label(
            row,
            text=value_text,
            font=("Microsoft YaHei", 13, "bold"),
            fg=TEXT_PRIMARY,
            bg=SECTION_BG,
        ).pack(side="right")


def _header(parent: tk.Widget) -> None:
    header = tk.Frame(parent, bg=APP_BG)
    header.grid(row=0, column=0, sticky="ew", padx=28, pady=(20, 16))

    tk.Label(
        header,
        text="总控室  烘丝监控  模型训练数据  数据管理",
        font=("Microsoft YaHei", 12),
        fg=TEXT_SECONDARY,
        bg=APP_BG,
    ).pack(anchor="w")

    tk.Label(
        header,
        text="模型训练：指标 蒸发10%回收温度 模型 DBN",
        font=("Microsoft YaHei", 22, "bold"),
        fg=TEXT_PRIMARY,
        bg=APP_BG,
    ).pack(anchor="w", pady=(8, 0))


def _section_title(parent: tk.Widget, text: str) -> None:
    tk.Label(
        parent,
        text=text,
        font=("Microsoft YaHei", 14, "bold"),
        fg=TEXT_PRIMARY,
        bg=SECTION_BG,
    ).pack(anchor="w", padx=16, pady=(16, 6))


def _render_layers(parent: tk.Widget) -> None:
    container = tk.Frame(parent, bg=SECTION_BG, bd=1, relief="flat")
    container.pack(fill="x", padx=24, pady=(8, 18))

    _section_title(container, "模型结构")

    layers = [
        ("输入", "传感器特征", "128 节点"),
        ("隐藏层 1", "ReLU", "64 节点"),
        ("隐藏层 2", "ReLU", "32 节点"),
        ("输出", "Sigmoid", "水分预测"),
    ]

    for name, activation, detail in layers:
        frame = tk.Frame(container, bg=SECTION_BG, highlightbackground=CARD_BORDER)
        frame.pack(fill="x", padx=16, pady=6)
        tk.Label(
            frame,
            text=name,
            font=("Microsoft YaHei", 12, "bold"),
            fg=ACCENT,
            bg=SECTION_BG,
        ).pack(anchor="w")
        tk.Label(
            frame,
            text=f"激活函数: {activation}    描述: {detail}",
            font=("Microsoft YaHei", 11),
            fg=TEXT_SECONDARY,
            bg=SECTION_BG,
        ).pack(anchor="w", pady=(4, 0))


def _render_metrics(parent: tk.Widget) -> None:
    container = tk.Frame(parent, bg=SECTION_BG)
    container.pack(fill="x", padx=24, pady=(0, 18))

    _section_title(container, "训练指标")

    metrics: Iterable[Metric] = (
        Metric("RMSE", "5.2302"),
        Metric("R²", "0.982"),
        Metric("MAPE", "1.23", "%"),
        Metric("Loss", "0.0068"),
    )

    for metric in metrics:
        metric.render(container)


def _render_logs(parent: tk.Widget) -> None:
    container = tk.Frame(parent, bg=SECTION_BG)
    container.pack(fill="both", expand=True, padx=24, pady=(0, 20))

    _section_title(container, "训练日志")

    log = tk.Text(
        container,
        bg="#0d2335",
        fg=TEXT_SECONDARY,
        bd=0,
        highlightthickness=0,
        height=10,
        font=("Consolas", 10),
    )
    log.pack(fill="both", expand=True, padx=16, pady=(0, 16))
    log.insert(
        "end",
        "[12:01] 加载训练数据集完成\n"
        "[12:02] 开始第 1200 轮训练\n"
        "[12:07] 验证集 RMSE 改善 0.12\n"
        "[12:10] 模型已保存到 '/models/dryer_dnb_best.h5'\n"
    )
    log.configure(state="disabled")


def _create_placeholder_chart(parent: tk.Widget, title: str) -> None:
    card = tk.Frame(parent, bg=SECTION_BG)
    card.pack(fill="both", expand=True, padx=20, pady=10)

    tk.Label(
        card,
        text=title,
        font=("Microsoft YaHei", 12, "bold"),
        fg=TEXT_PRIMARY,
        bg=SECTION_BG,
    ).pack(anchor="w", padx=16, pady=(16, 6))

    canvas = tk.Canvas(card, height=180, bg="#0d2335", highlightthickness=0)
    canvas.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    width = 560
    height = 160
    canvas.create_line(20, height, width, 20, fill=ACCENT, width=2, smooth=True)
    for x in range(40, width, 100):
        canvas.create_line(x, height, x, height - 12, fill="#1f3a50")
    for y in range(height, 20, -40):
        canvas.create_line(20, y, width, y, fill="#1f3a50")


def _render_controls(parent: tk.Widget) -> None:
    bar = tk.Frame(parent, bg=PANEL_BG)
    bar.pack(fill="x", padx=24, pady=(4, 20))

    for label in ("开始训练", "暂停", "导出报告"):
        tk.Button(
            bar,
            text=label,
            font=("Microsoft YaHei", 11),
            bg="#1d6ea7",
            fg=TEXT_PRIMARY,
            activebackground="#289bd6",
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=18,
            pady=6,
        ).pack(side="left", padx=12)


def _left_panel(parent: tk.Widget) -> None:
    left = tk.Frame(parent, bg=PANEL_BG)
    left.grid(row=0, column=0, sticky="nsew")
    left.grid_rowconfigure(2, weight=1)

    _render_layers(left)
    _render_metrics(left)
    _render_logs(left)


def _right_panel(parent: tk.Widget) -> None:
    right = tk.Frame(parent, bg=PANEL_BG)
    right.grid(row=0, column=1, sticky="nsew", padx=(6, 28))
    right.grid_rowconfigure(0, weight=1)
    right.grid_rowconfigure(1, weight=1)

    _create_placeholder_chart(right, "蒸发温度回溯")
    _create_placeholder_chart(right, "水分波动监测")

    _render_controls(right)


def launch_app() -> None:
    root = tk.Tk()
    root.title("烘丝机水分质量预测软件")
    root.configure(bg=APP_BG)
    root.geometry("1320x780")
    root.minsize(1180, 700)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    _header(root)

    content = tk.Frame(root, bg=APP_BG)
    content.grid(row=1, column=0, sticky="nsew")
    content.grid_columnconfigure(0, weight=1, minsize=380)
    content.grid_columnconfigure(1, weight=2)
    content.grid_rowconfigure(0, weight=1)

    _left_panel(content)
    _right_panel(content)

    root.mainloop()


if __name__ == "__main__":
    launch_app()
