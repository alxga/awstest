import os
import shutil
import csv
import unittest
from common import utils, Settings
from gtfsstatic import gtfsparsers


class TestGtfsStaticCsvParsersMBTA1(unittest.TestCase):
  """Class to test the DataMgr class

  Class Attributes:
    TestsRootDir: Path to test input and expected output files
    TempDir: Path to temporary input and test output files
  """

  TestsRootDir = os.path.join(Settings.ProjPath, "tests", "mbta1")
  TempDir = os.path.join(Settings.ProjPath, "Temp")

  @classmethod
  def setUpClass(cls):
    """Creates a temporary folder shared by all tests"""
    if os.path.isdir(cls.TempDir):
      shutil.rmtree(cls.TempDir)
    os.makedirs(cls.TempDir)

    gtfsStaticPath = os.path.join(cls.TempDir, "gtfs_static")
    shutil.copytree(cls.TestsRootDir, gtfsStaticPath)

    cls.GTFSStaticPath = gtfsStaticPath

  @classmethod
  def tearDownClass(cls):
    """Removes the temporary folder shared by all tests"""
    shutil.rmtree(cls.TempDir, True)


  def read_calendar_to_dict(self):
    ret = {}
    with utils.open_csv_r(os.path.join(self.__class__.GTFSStaticPath,
                                       "calendar.csv")) as f:
      reader = csv.reader(f)
      parser = gtfsparsers.CalendarCsv(next(reader))
      for row in reader:
        service = parser.parse_row(row)
        ret[service.id] = service
    return ret

  def read_calendar_dates(self, serviceDict):
    with utils.open_csv_r(os.path.join(self.__class__.GTFSStaticPath,
                                       "calendar_dates.csv")) as f:
      reader = csv.reader(f)
      parser = gtfsparsers.CalendarDatesCsv(next(reader), serviceDict)
      for row in reader:
        parser.parse_row(row)

  def read_stops_to_dict(self):
    ret = {}
    with utils.open_csv_r(os.path.join(self.__class__.GTFSStaticPath,
                                       "stops.csv")) as f:
      reader = csv.reader(f)
      parser = gtfsparsers.StopsCsv(next(reader))
      for row in reader:
        stop = parser.parse_row(row)
        ret[stop.id] = stop
    parser.resolve_forward_refs(ret)
    return ret

  def read_routes_to_dict(self):
    ret = {}
    with utils.open_csv_r(os.path.join(self.__class__.GTFSStaticPath,
                                       "routes.csv")) as f:
      reader = csv.reader(f)
      parser = gtfsparsers.RoutesCsv(next(reader))
      for row in reader:
        route = parser.parse_row(row)
        ret[route.id] = route
    return ret


  def test_calendar_csv_parser(self):
    serviceDict = self.read_calendar_to_dict()
    self.assertEqual(len(serviceDict), 92)

  def test_calendar_dates_csv_parser(self):
    serviceDict = self.read_calendar_to_dict()
    self.read_calendar_dates(serviceDict)

  def test_stops_csv_parser(self):
    stopDict = self.read_stops_to_dict()
    self.assertEqual(len(stopDict), 9861)

  def test_route_csv_parser(self):
    routeDict = self.read_routes_to_dict()
    self.assertEqual(len(routeDict), 236)


if __name__ == '__main__':
  unittest.main()
