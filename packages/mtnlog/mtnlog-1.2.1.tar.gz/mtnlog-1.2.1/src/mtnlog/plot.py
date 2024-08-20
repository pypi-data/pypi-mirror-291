import logging
import os
import re

import matplotlib.pyplot as plt
import pandas as pd
from pandas.errors import EmptyDataError, ParserError
from tqdm import tqdm

cuda_devices = [0, 1, 2, 3]

network_interfaces = ['lo', 'enp195s0', 'bond0', 'hsn0', 'hsn1']

plot_col = [
    'cpu_percent (%)/mean',
    'memory_used (GiB)/mean',
    'memory_percent (%)/mean'
] + [
    f'cuda:{i} (gpu:{i})/{metric}/mean'
    for i in cuda_devices
    for metric in ['memory_used (MiB)', 'gpu_utilization (%)']
] + [
    f'network_{interface}/{direction} (Mbps)'
    for interface in network_interfaces
    for direction in ['sent', 'recv']
]

colors = plt.get_cmap("Paired").colors  # type: ignore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PerformancePlotter:
    """Performance plotter class."""

    def __init__(self, base_dir, log_node):
        self.log_node = log_node
        self.metric_dir = f"{base_dir}/metric"
        self.graph_dir = f"{base_dir}/graph"

        os.makedirs(self.graph_dir, exist_ok=True)

    def get_tag_colors(self, df):
        """Returns the tag colors."""

        tags = df['tag'].unique()

        return {tag: colors[i] for i, tag in enumerate(tags)}

    def graph(self, df, node_plot_dir):
        """Graphs the performance metrics."""

        os.makedirs(node_plot_dir, exist_ok=True)

        tag_colors = self.get_tag_colors(df)

        for col in tqdm(plot_col, desc=f"Plotting metrics for node-{self.log_node}: "):
            if col not in df.columns:
                logging.warning("Column %s not found in DataFrame, skipping.", col)
                continue

            _, ax = plt.subplots(figsize=(10, 6))

            for tag in df['tag'].unique():
                segment = df[df['tag'] == tag]
                if segment.empty:
                    continue  # Skip empty segments
                ax.plot(segment['duration (s)'], segment[col], label=tag, color=tag_colors[tag])

            if 'memory_used (MiB)' in col:
                gpu_memory_col = col.replace('memory_used (MiB)', 'memory_total (MiB)')
                if gpu_memory_col in df.columns:
                    # Ensure the column contains numeric data
                    df[gpu_memory_col] = pd.to_numeric(df[gpu_memory_col], errors='coerce')
                    max_y = df[gpu_memory_col].mean()
                    if not pd.isna(max_y):
                        ax.axhline(y=max_y, color='r', linestyle='--', label="Max Memory")

            ax.legend(title='Tag')

            name = re.sub(r"[ /]", "_", col)
            name = re.sub(r"_mean", "", name)
            name = re.sub(r"\(gpu:\d+\)", "", name)

            ax.set_xlabel('Duration (s)')
            ax.set_ylabel(name)

            plt.savefig(f"{node_plot_dir}/{name}.jpg", format='jpeg', dpi=100)
            plt.close()

    def plot(self):
        """Plots the performance metrics."""

        filepath = f"{self.metric_dir}/node-{self.log_node}.csv"

        try:
            df = pd.read_csv(filepath)

            if df.empty:
                logging.warning("File %s is empty, skipping.", filepath)

            df.sort_values(by=['duration (s)'], inplace=True)

            df = df[df['tag'].notna()]
            self.graph(df, f"{self.graph_dir}/node-{self.log_node}")
        except EmptyDataError:
            logging.warning("File %s is empty, skipping.", filepath)
        except ParserError:
            logging.error("File %s is improperly formatted, skipping.", filepath)
        except OSError as e:
            logging.error("Error reading file %s: %s", filepath, e)

        logging.info("Graphs saved in %s", self.graph_dir)
