import ratelimit
import matplotlib.pyplot as plt
import pathlib
from xml.etree import ElementTree
import gzip
import urllib.request
import tempfile
from bfastor import maps


@ratelimit.limits(calls=30, period=60)
def _get_validation_report(emdb_number, local_file):
    url = (
        f"https://ftp.ebi.ac.uk/pub/databases/emdb/validation_reports/EMD-{emdb_number}/"
        f"emd_{emdb_number}_validation.xml.gz"
    )
    print(f"Downloading validation report for EMD-{emdb_number}...")
    urllib.request.urlretrieve(url, filename=local_file)


def fetch_validation_report(emdb_number):
    tempdir = pathlib.Path(tempfile.gettempdir())
    local_file = tempdir / f"emd_{emdb_number}_validation.xml.gz"

    if not local_file.is_file():
        _get_validation_report(emdb_number, local_file)

    return local_file


def fetch_resolution_from_emdb(emdb_number):
    local_file = fetch_validation_report(emdb_number)

    # parse the xml file and find the resolution
    with gzip.open(local_file, "r") as f:
        etree = ElementTree.parse(f)
        resolution = etree.find("Entry").attrib["EMDB-resolution"]

    return float(resolution)


def plot_and_save_line(data, output_folder, title="plot", xlabel=None, ylabel=None):
    plt.plot(data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(output_folder / f"{title}.png")
    plt.close()


def plot_and_save_bfactors(initial_bfactors, refined_bfactors, output_dir):
    max_val = max(initial_bfactors.max(), refined_bfactors.max())
    fig, ax = plt.subplots()
    plot1 = ax.plot(initial_bfactors, label="Initial Bfactors")
    ax.set_ylim(0, max_val)
    plot2 = ax.plot(refined_bfactors, label="Refined Bfactors", color="tab:orange")
    ax.set(ylabel="B-factor values", xlabel="Atom number")
    plotted_data = plot1 + plot2
    labels = [i.get_label() for i in plotted_data]
    ax.legend(plotted_data, labels)
    plt.savefig(output_dir / "refined-bfactors.png")
    plt.close()


def ccc(map_1: maps.Map, map_2: maps.Map):
    return (maps.normalise(map_1).data * maps.normalise(map_2).data).mean()
