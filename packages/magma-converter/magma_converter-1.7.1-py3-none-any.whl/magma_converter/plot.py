import seaborn as sns
import os
import numpy as np

from matplotlib import pyplot as plt
from PIL import Image
from .sds import SDS
from obspy import Trace, Stream
from typing import List, Self
sns.set_style("whitegrid")


class Plot:
    types: List[str] = ['normal', 'dayplot', 'relative', 'section']

    def __init__(self,
                 sds: SDS,
                 plot_type: str = 'dayplot'):
        """Plot daily seismogram

        Args:
            sds: SDS object
            plot_type: Plot type must be between 'normal', 'dayplot', 'relative', 'section'.
        """
        assert type not in self.types, f"Plot type must be between 'normal', 'dayplot', 'relative', 'section'."

        self.sds: SDS = sds
        self.completeness = sds.results['completeness']
        self.trace: Trace = sds.trace
        self.sampling_rate = sds.results['sampling_rate']
        self.date = sds.results['date']
        self.filename: str = f"{sds.filename}.jpg"
        self.plot_type = plot_type
        self.plot_gaps: bool = False

        output_dir: str = os.path.dirname(sds.path).replace('SDS', 'Seismogram')
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir: str = output_dir

        thumbnail_dir: str = os.path.join(output_dir, 'thumbnail')
        os.makedirs(thumbnail_dir, exist_ok=True)
        self.thumbnail_dir: str = thumbnail_dir

    def plot_with_gaps(self, plot_gaps: bool = False) -> Self:
        """Plot with gaps.

        Args:
            plot_gaps: Plot gaps between traces.

        Returns:
            Self: Plot with gaps.
        """
        self.plot_gaps = plot_gaps
        return self

    @property
    def title(self):
        """Plot title

        Returns:
            title (str)
        """
        return (f"{self.date} | {self.trace.id} | {self.sampling_rate} Hz | "
                f"{self.trace.stats.npts} samples ({self.completeness:.2f})%")

    def thumbnail(self, seismogram: str) -> str:
        """Generate thumbnail of seismogram.

        Args:
            seismogram (str): Seismogram image path
        """
        outfile = os.path.join(self.thumbnail_dir, self.filename)

        image = Image.open(seismogram)

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image.thumbnail((320, 180))
        image.save(outfile)

        return outfile

    def replace_zeros_with_gaps(self, trace: Trace) -> Stream | Trace:
        """Replace zeros with gaps.

        Args:
            trace (Trace): Trace to replace zeros with gaps.

        Returns:
            Stream | Trace: Stream or trace with zeros replaced with gaps.
        """
        if self.plot_gaps is True:
            trace.data = np.ma.masked_where(trace.data == 0, trace.data)
            stream: Stream = trace.split()
            return stream

        return trace

    def save(self) -> tuple[str, str]:
        """Save plot to file.

        Returns:
            seismogram_image_path (str), thumbnail_image_path (str)
        """
        seismogram = os.path.join(self.output_dir, self.filename)

        stream = self.replace_zeros_with_gaps(self.trace.copy())

        stream.plot(
            type='dayplot',
            interval=60,
            one_tick_per_line=True,
            color=['k'],
            outfile=seismogram,
            number_of_ticks=13,
            size=(1600, 900),
            title=self.title
        )

        plt.close('all')

        thumbnail = self.thumbnail(seismogram)

        print(f"🏞️ {self.date} :: Seismogram saved to : {seismogram}")

        return seismogram, thumbnail
