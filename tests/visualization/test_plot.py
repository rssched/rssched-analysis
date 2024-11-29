import time

from rssched.data.access import PkgDataAccess
from rssched.io.reader import import_request, import_response
from rssched.visualization.depot_loads import plot_depot_vehicle_loads
from rssched.visualization.plot import generate_plots


def test_generate_plots():
    response = import_response(PkgDataAccess.locate_response())
    figs = generate_plots(response, "test_instance")
    assert len(figs) == 8


def test_plot_depot_vehicle_loads():
    request = import_request(PkgDataAccess.locate_request())
    response = import_response(PkgDataAccess.locate_response())
    fig = plot_depot_vehicle_loads(request, response, "test_instance", "depot_ZH")
    assert fig is not None
