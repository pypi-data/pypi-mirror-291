"""
This module supports output handling
"""

from pathlib import Path
import logging

from icflow.data import SplitDataset

from .output_handler import OutputHandler
from .visualization import Plot

logger = logging.getLogger(__name__)


class PlottingOutputHandler(OutputHandler):
    def __init__(
        self, result_dir: Path = Path(), is_multigpu: bool = False, num_images: int = 20
    ):
        super().__init__(result_dir)

        self.is_multigpu = is_multigpu
        self.num_images = num_images
        self.pre_epoch_image_path = "train_sample"

    def on_before_epochs(self, num_epochs: int, dataset: SplitDataset):
        logger.info("Plotting dataset sample")
        plot = Plot(is_multigpu=self.is_multigpu)
        plot.visualize(dataset.get_data("train"), n_ims=self.num_images)
        plot.save(self.result_dir / "train_sample")

    def on_after_infer(self, stage, predictions, metrics):
        super().on_after_infer(stage, predictions, metrics)

        Plot(metrics, self.is_multigpu)
