import time

from rssched.data.access import PkgDataAccess
from rssched.io.reader import import_response
from rssched.visualization.depot_loads import plot_depot_vehicle_loads
from rssched.visualization.plot import generate_plots


def test_generate_plots():
    response = import_response(PkgDataAccess.locate_response())
    figs = generate_plots(response, "test_instance")
    assert len(figs) == 6


def test_plot_depot_vehicle_loads():
    response = import_response(PkgDataAccess.locate_response())
    fig = plot_depot_vehicle_loads(response, "test_instance", "depot_ZH")
    fig.show()
    time.sleep(5)
