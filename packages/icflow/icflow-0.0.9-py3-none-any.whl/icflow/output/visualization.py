import random
from pathlib import Path

from torchvision import transforms as tfs
from matplotlib import pyplot as plt
import numpy as np

ZEROS = [0.0, 0.0, 0.0]
ONES = [1.0, 1.0, 1.0]


class MultiFigureLinePlot:
    def __init__(self, data: dict, figures: dict, xlabel: str) -> None:
        self.data = data
        self.figures = figures
        self.size: tuple = (10, 5)
        self.xlabel = xlabel

    def _plot_line(self, metric: str, label: str):
        plt.plot(self.data[metric], label=label)

    def _decorate(self, ylabel: str, title: str):
        plt.title(title)
        plt.xlabel(self.xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

    def plot(self):

        for figure_info in self.figures:
            plt.figure(figsize=self.size)

            for data_key, label in zip(figure_info["keys"], figure_info["labels"]):
                self._plot_line(data_key, label)

            title = figure_info["title"]
            ylabel = figure_info["ylabel"]

            self._decorate(ylabel, title)


class DatasetGridPlotter:
    def __init__(
        self, title: str, stride: int = 4, size: tuple = (25, 20), transform=None
    ) -> None:
        self.title = title
        self.stride = stride
        self.size = size
        self.transform = transform

    def tensor_to_numpy(self, t):
        if len(t) == 3:  # rgb
            return (
                (self.transform.inverse(t) * self.transform.scale())
                .detach()
                .cpu()
                .permute(1, 2, 0)
                .numpy()
                .astype(np.uint8)
            )
        return (t * self.transform.scale()).detach().cpu().numpy().astype(np.uint8)

    def _plot_grid_element(self, rows: int, cols: int, count: int, image):
        plt.subplot(rows, cols, count)
        plt.imshow(self.tensor_to_numpy(image.squeeze(0).float()))
        plt.axis("off")
        plt.title(self.title)
        return count + 1

    def plot_samples(self, data, num_samples: int):
        plt.figure(figsize=self.size)
        rows = num_samples // self.stride
        cols = num_samples // rows
        count = 1
        indices = [random.randint(0, len(data) - 1) for _ in range(num_samples)]

        for index in indices:
            if count == num_samples + 1:
                break
            x, y = data[index]

            count = self._plot_grid_element(rows, cols, count, x)
            count = self._plot_grid_element(rows, cols, count, y)


class Plot:
    """
    Class for plotting training and validation metrics over epochs
    """

    def __init__(self, result=None, is_multigpu: bool = False):
        self.result = result
        self.is_multigpu = is_multigpu

        if self.result:
            self.visualize_graphs(
                metric1="tr_iou",
                metric2="val_iou",
                label1="Train IoU",
                label2="Validation IoU",
                title="Mean Intersection Over Union Learning Curve",
                ylabel="mIoU Score",
            )

            self.visualize_graphs(
                metric1="tr_pa",
                metric2="val_pa",
                label1="Train PA",
                label2="Validation PA",
                title="Pixel Accuracy Learning Curve",
                ylabel="PA Score",
            )

            self.visualize_graphs(
                metric1="tr_loss",
                metric2="val_loss",
                label1="Train Loss",
                label2="Validation Loss",
                title="Loss Learning Curve",
                ylabel="Loss Value",
            )

    def save(self, path: Path):
        plt.savefig(path)

    def plot_graphs(self, metric, label):
        if self.is_multigpu:
            metric_data = [t.cpu().numpy() for t in self.result[metric]]
        else:
            metric_data = self.result[metric]
        plt.plot(metric_data, label=label)

    def decorate(self, ylabel, title):
        """
        Helper method to decorate the plot with titles, labels, and legends
        """

        plt.title(title)
        plt.xlabel("Epochs")
        plt.ylabel(ylabel)
        plt.legend()

    def visualize_graphs(self, metric1, metric2, label1, label2, title, ylabel):
        """
        Method to visualize the comparison of train and validation metrics
        """

        plt.figure(figsize=(10, 5))
        self.plot_graphs(metric1, label1)
        self.plot_graphs(metric2, label2)
        self.decorate(ylabel, title)
        plt.savefig(ylabel)

    def tn_2_np(self, t):
        """
        Reverse the normalization and convert a PyTorch tensor to NumPy
        """

        inv_trans = tfs.Compose(
            [
                tfs.Normalize(
                    mean=[0.0, 0.0, 0.0], std=[1 / 0.229, 1 / 0.224, 1 / 0.225]
                ),
                tfs.Normalize(mean=[-0.485, -0.456, -0.406], std=[1.0, 1.0, 1.0]),
            ]
        )

        rgb = len(t) == 3
        return (
            (inv_trans(t) * 255)
            .detach()
            .cpu()
            .permute(1, 2, 0)
            .numpy()
            .astype(np.uint8)
            if rgb
            else (t * 255).detach().cpu().numpy().astype(np.uint8)
        )

    def plot(self, rows, cols, count, im, gt=None, title="Original Image"):
        """
        Create a subplot in a grid and display an image
        """

        plt.subplot(rows, cols, count)
        (
            plt.imshow(self.tn_2_np(im.squeeze(0).float()))
            if gt
            else plt.imshow(self.tn_2_np(im.squeeze(0)))
        )
        plt.axis("off")
        plt.title(title)

        return count + 1

    def visualize(self, ds, n_ims):
        """
        Visualize a random set of images and their ground truths from a dataset
        """

        plt.figure(figsize=(12, 10))
        rows = n_ims // 4
        cols = n_ims // rows
        count = 1
        indices = [random.randint(0, len(ds) - 1) for _ in range(n_ims)]

        for _, index in enumerate(indices):

            if count == n_ims + 1:
                break  # Stop if we've plotted all requested images
            im, gt = ds[index]

            # First Plot
            count = self.plot(rows, cols, count, im=im)

            # Second Plot
            count = self.plot(rows, cols, count, im=gt, gt=True)
