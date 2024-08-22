import os

import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Polygon

from .indicator import (envelope_of_expected_error, pearsonr_scipy, r2_score,
                        root_mean_square_error)

font_config = {
    "Default": {},
    "Times New Roman": {
        "family": "serif",
        "serif": ["Times New Roman"],
        "weight": "normal",
    },
}

style_config = {
    "single_normal": {
        "figsize": (3.538, 3.538),
        "fontsize": 10.5,
        "tick_fontsize": 9,
        "text_fontsize": 9,
        "label_fontsize": 9,
        "legend_fontsize": 9,
    },
    "single_bold": {
        "figsize": (5, 4.5),
        "fontsize": 12,
        "tick_fontsize": 10.5,
        "text_fontsize": 10.5,
        "label_fontsize": 10.5,
        "legend_fontsize": 10.5,
    },
}

example_config = {
    "fontname": "Times New Roman",
    "fontsize": 10.5,
    "tick_fontsize": 9,
    "text_fontsize": 9,
    "label_fontsize": 9,
    "legend_fontsize": 9,
    "dpi": 300,
    "figsize": (3.5, 3.22),
    "xlabel": "Measured AOD",
    "ylabel": "Retrieved AOD",
    "title": None,
    "ee_line_width": 0.5,
    "ee_absolute_error": 0.05,
    "ee_relative_error": 0.15,
    "text_indicators": ["EE", "RMSE", "R", "N"],
    "kernel_normalize": True,
    "text_bbox": dict(boxstyle="round", facecolor="white", alpha=0.7, linewidth=0.2),
}


class DensityChart:
    @staticmethod
    def set_matplotlib_params(**kwargs):
        # 设置字体
        mpl.rc("font", **font_config[kwargs.get("fontname", "Times New Roman")])
        mpl.rcParams["font.size"] = kwargs.get("fontsize", 9)
        mpl.rcParams["mathtext.fontset"] = "stix"

        # 设置布局
        mpl.rcParams["figure.constrained_layout.use"] = True

        # Set x axis
        mpl.rcParams["xtick.direction"] = "in"
        mpl.rcParams["xtick.major.size"] = 3
        mpl.rcParams["xtick.major.width"] = 0.5
        mpl.rcParams["xtick.minor.size"] = 1.5
        mpl.rcParams["xtick.minor.width"] = 0.5
        mpl.rcParams["xtick.minor.visible"] = True
        mpl.rcParams["xtick.top"] = True

        # Set y axis
        mpl.rcParams["ytick.direction"] = "in"
        mpl.rcParams["ytick.major.size"] = 3
        mpl.rcParams["ytick.major.width"] = 0.5
        mpl.rcParams["ytick.minor.size"] = 1.5
        mpl.rcParams["ytick.minor.width"] = 0.5
        mpl.rcParams["ytick.minor.visible"] = True
        mpl.rcParams["ytick.right"] = True

        # 设置分辨率
        mpl.rcParams["figure.dpi"] = kwargs.get("dpi", 300)  # plt.show显示分辨率
        mpl.rcParams["savefig.dpi"] = kwargs.get("dpi", 300)  # plt.savefig保存分辨率

    @staticmethod
    def update_style_config_with_default_kwargs(style: str, config):
        if style:
            if style in style_config:
                _config = style_config[style]
                _config.update(config)
            else:
                raise ValueError(f"没有{style}对应的风格")
        else:
            _config = config.copy()

        # 设置字体, 默认使用Times New Roman, 如果系统中没有该字体, 则使用Matplotlib默认字体
        fontname = _config.get("fontname", "Times New Roman")
        matplotlib_fontnames = [i.name for i in mpl.font_manager.fontManager.ttflist]
        if (fontname not in ["Default"]) and (fontname not in matplotlib_fontnames):
            print(f"Warning: 系统中没有找到{fontname}字体, 请安装该字体, 本次将使用默认字体")
            fontname = "Default"
        _config["fontname"] = fontname

        # 设置字体大小, 小四号字体为12pt, 五号字体为10.5pt, 小五号字体为9pt
        _config["fontsize"] = _config.get("fontsize", 10.5)
        _config["tick_fontsize"] = _config.get("tick_fontsize", _config["fontsize"])
        _config["text_fontsize"] = _config.get("text_fontsize", _config["fontsize"])
        _config["label_fontsize"] = _config.get("label_fontsize", _config["fontsize"])
        _config["legend_fontsize"] = _config.get("legend_fontsize", _config["fontsize"])

        # 设置分辨率, 默认300dpi
        _config["dpi"] = _config.get("dpi", 300)
        _config["figsize"] = _config.get("figsize", (4, 4))
        _config["xlabel"] = _config.get("xlabel", "Measured AOD")
        _config["ylabel"] = _config.get("ylabel", "Retrieved AOD")
        _config["title"] = _config.get("title", None)

        # 设置其它参数
        _config["ee_line_width"] = _config.get("ee_line_width", 0.5)
        _config["ee_absolute_error"] = _config.get("ee_absolute_error", 0.05)
        _config["ee_relative_error"] = _config.get("ee_relative_error", 0.15)
        _config["text_indicators"] = _config.get("text_indicators", ["EE", "RMSE", "R", "N"])
        _config["kernel_normalize"] = _config.get("kernel_normalize", False)
        # text_box: dict(boxstyle="round", facecolor="white", alpha=0.7, linewidth=0.2)
        _config["text_bbox"] = _config.get("text_bbox", None)
        return _config

    @staticmethod
    def add_envelope_layer(ax: Axes, absolute_error=0.05, relative_error=0.15, linewidth=0.5, label="EE envelopes"):
        # 生成包络线图层, default EE envelopes: ±(0.05+15%)
        ax.axline((0, 0), slope=1, linestyle="-", color="black", linewidth=linewidth)
        slope_positive = 1 + relative_error
        point_positive = (0, absolute_error)
        slope_negative = 1 - relative_error
        point_negative = (0, -absolute_error)
        ax.axline(point_positive, slope=slope_positive, linestyle="--", color="black", linewidth=linewidth, label=label)
        ax.axline(point_negative, slope=slope_negative, linestyle="--", color="black", linewidth=linewidth)

    @staticmethod
    def add_kernel_density_layer(ax: Axes, x, y, point_size, cmap="jet", label=None, Normalize=False):
        # 计算数据的高斯核密度分布
        from scipy.stats import gaussian_kde

        xy = np.vstack([x, y])
        z = gaussian_kde(xy)(xy)

        # 归一化
        if Normalize:
            z = z / z.max()

        # 生成散点图图层
        p = ax.scatter(x, y, marker="o", c=z, s=point_size, cmap=cmap, vmin=0, label=label)
        return p

    @staticmethod
    def add_indicator_text_layer(
        ax: Axes, x, y, absolute_error=0.05, relative_error=0.15, fontsize=9, bbox=None, indicators=None
    ):
        # 计算指标
        text_list = []
        for indicator in indicators:
            if indicator not in ["EE", "RMSE", "R2", "R", "N"]:
                raise ValueError(f"指标{indicator}不在支持的指标列表中")
            if indicator == "EE":
                above_percent, below_percent, within_percent = envelope_of_expected_error(
                    x, y, absolute_error=absolute_error, relative_error=relative_error
                )
                text_list += [
                    f"$EE$ envelopes: ±({absolute_error}+{int(relative_error*100)}%)",
                    f"     {format(within_percent, '.1f')}% within $EE$",
                    f"     {format(above_percent, '.1f')}% above $EE$",
                    f"     {format(below_percent, '.1f')}% below $EE$",
                ]
            if indicator == "RMSE":
                rmse = root_mean_square_error(x, y)
                text_list.append(f"$RMSE$ = {format(rmse, '.3f')}")
            if indicator == "R2":
                r2 = r2_score(x, y)
                text_list.append(f"$R^2$ = {format(r2, '.3f')}")
            if indicator == "R":
                r = pearsonr_scipy(x, y) if len(x) > 1 else 0
                text_list.append(f"$R$ = {format(r, '.3f')}")
            if indicator == "N":
                text_list.append(f"$N$ = {len(x)}")
        _text = "\n".join(text_list)

        edge_distance = 0.03
        x, y = edge_distance, 1 - edge_distance
        p = ax.text(
            x, y, _text, fontsize=fontsize, verticalalignment="top", color="black", bbox=bbox, transform=ax.transAxes
        )
        return p

    @staticmethod
    def add_legend(ax: Axes, fontsize=9):
        lg = ax.legend(
            loc=4,
            alignment="right",
            fontsize=fontsize,
            labelspacing=0.2,
            borderpad=0.2,
            handletextpad=0.2,
            handlelength=1,
        )
        lg.get_frame().set(linewidth=0.2, edgecolor="k", alpha=0.5)


def create_figure_and_plot_density_kernel_chart(x, y, xy_max_edge=2, save_path=None, **kwargs):
    # 设置风格, 先从kwargs中获取style参数, 如果没有则为空字典, 然后使用kwargs中的参数更新风格字典
    kwargs = DensityChart.update_style_config_with_default_kwargs(kwargs.get("style"), kwargs)

    with mpl.rc_context():
        # 设置matplotlib参数
        DensityChart.set_matplotlib_params(**kwargs)

        # 设置画布
        fig, axes = plt.subplots(1, 1, figsize=kwargs["figsize"])

        # 设置其它参数
        axes.set_title(kwargs.get("title", None))  # 设置标题
        # 设置坐标轴参数
        axes.set_xlabel(kwargs.get("xlabel", None), labelpad=2)
        axes.set_ylabel(kwargs.get("ylabel", None), labelpad=2)
        axes.set_xlim(-0.05, xy_max_edge + 0.05)
        axes.set_ylim(-0.05, xy_max_edge + 0.05)
        axes.set_aspect("equal")
        axes.grid(linestyle=":", color="r", alpha=0.1)
        # 设置刻度, 保证刻度不会超过xy_max_edge, 且刻度间隔为0.5
        xyticks = [i / 2 for i in range(int(xy_max_edge // 0.5) + 1)]
        xyticks = [i for i in xyticks if i <= xy_max_edge]
        xytickslables = [f"{format(i, '.1f')}" for i in xyticks]
        axes.set_xticks(xyticks)
        axes.set_yticks(xyticks)
        axes.set_xticklabels(xytickslables)
        axes.set_yticklabels(xytickslables)

        # 设置刻度字体大小
        axes.tick_params(labelsize=kwargs["tick_fontsize"])

        # 绘制包络线图层
        ee_params = {
            "absolute_error": kwargs["ee_absolute_error"],
            "relative_error": kwargs["ee_relative_error"],
        }

        DensityChart.add_envelope_layer(axes, linewidth=kwargs["ee_line_width"], label="EE envelopes", **ee_params)

        # 将数据转为numpy数组
        x, y = np.array(x).reshape(-1), np.array(y).reshape(-1)  # x means label, y means predict
        mask = (x <= xy_max_edge) & (y <= xy_max_edge)
        print(f"数据总数: {len(x)}, 有效数据总数: {mask.sum()}, 越界数据总数: {(~mask).sum()}")

        # 计算scatter散点的大小
        point_size = kwargs.get("dpi", 300) / 100
        # 生成散点图图层
        p = DensityChart.add_kernel_density_layer(
            axes, x, y, point_size, cmap="jet", Normalize=kwargs["kernel_normalize"]
        )

        # 生成文本图层
        text_bbox = kwargs.get("text_bbox", None)
        indicators = kwargs["text_indicators"]
        DensityChart.add_indicator_text_layer(
            axes, x, y, fontsize=kwargs["text_fontsize"], bbox=text_bbox, indicators=indicators, **ee_params
        )

        # 生成图例
        DensityChart.add_legend(axes, kwargs["legend_fontsize"])

        # 生成colorbar
        cb = fig.colorbar(p, ax=axes, pad=0.02, fraction=0.05)
        # cb.ax.set_ylabel("Density", fontsize=kwargs["tick_fontsize"])
        cb.ax.set_title(label="Density", fontdict={"size": kwargs["label_fontsize"]}, pad=7)
        cb.ax.tick_params(labelsize=kwargs["tick_fontsize"])

        # 画图
        if save_path is not None:
            # 检查保存路径父文件夹是否存在, 不存在则创建上级目录
            pic_dirpath = os.path.dirname(os.path.abspath(save_path))
            if not os.path.exists(pic_dirpath):
                os.makedirs(pic_dirpath)
            # 保存图片
            plt.savefig(save_path)
            plt.close(fig)
        else:
            # 显示图片
            plt.show()
