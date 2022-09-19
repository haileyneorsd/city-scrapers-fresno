from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.san_joaquin_river_conservancy import SanJoaquinRiverConservancySpider

test_response = file_response(
    join(dirname(__file__), "files", "san_joaquin_river_conservancy.html"),
    url="http://sjrc.ca.gov/Board/",
)
spider = SanJoaquinRiverConservancySpider()

freezer = freeze_time("2022-09-18")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()

def test_title():
    assert parsed_items[0]["title"] == "February 2- Board Meeting "
    assert parsed_items[1]["title"] == "April 6- Board Meeting"
    assert parsed_items[2]["title"] == "May 4- Board Meeting"
    assert parsed_items[3]["title"] == "August 3- Board Meeting"
    assert parsed_items[4]["title"] == "September 7 – Board Meeting"
    assert parsed_items[5]["title"] == "November 2- Board Meeting"

@pytest.mark.parametrize("item", parsed_items)
def test_description(item):
    assert item["description"] == ""

def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 2, 2, 10, 30)
    assert parsed_items[1]["start"] == datetime(2022, 4, 6, 10, 00)
    assert parsed_items[2]["start"] == datetime(2022, 5, 4, 10, 00)
    assert parsed_items[3]["start"] == datetime(2022, 8, 3, 10, 00)
    assert parsed_items[4]["start"] == datetime(2022, 9, 7, 10, 00)
    assert parsed_items[5]["start"] == datetime(2022, 11, 2, 10, 30)


def test_end():
    assert parsed_items[0]["end"] == None

@pytest.mark.parametrize("item", parsed_items)
def test_time_notes(item):
    time_notes_str = ("Scheduled meetings are subject to change. "
                      "Refer to Agenda if available. For more information "
                      "email info@sjrc.ca.gov or call (559) 253-7324.")
    assert item["time_notes"] == time_notes_str

# def test_id():
#     assert parsed_items[0]["id"] == "EXPECTED ID"


def test_status():
    assert parsed_items[0]["status"] == "passed"
    assert parsed_items[1]["status"] == "passed"
    assert parsed_items[2]["status"] == "passed"
    assert parsed_items[3]["status"] == "passed"
    assert parsed_items[4]["status"] == "passed"
    assert parsed_items[5]["status"] == "tentative"


def test_location():
    location_dict = { "address": "5469 E. Olive Ave., Fresno, CA 93727",
            "name": "Fresno Metropolitan Flood Control District Board Room" }

    assert parsed_items[0]["location"] == location_dict

@pytest.mark.parametrize("item", parsed_items)
def test_source(item):
    assert item["source"] == "http://sjrc.ca.gov/Board/"

def test_links():
    link_dict = {'http://sjrc.ca.gov/wp-content/uploads/2022/01/2021-December-SJRC-Draft-Minutes.pdf': '2021-December-SJRC-Draft-Minutes',
           'http://sjrc.ca.gov/wp-content/uploads/2022/01/2022-Feb-SJRC-Revised-Agenda.pdf': '2022-Feb-SJRC-Revised-Agenda',
           'http://sjrc.ca.gov/wp-content/uploads/2022/01/2022-February-SJRC-Board-Packet.pdf': '2022-February-SJRC-Board-Packet',
           'http://sjrc.ca.gov/wp-content/uploads/2022/02/BALL-RANCH.pdf': 'BALL-RANCH',
           'http://sjrc.ca.gov/wp-content/uploads/2022/02/Staff-Presentation-for-Feb-2022.pdf': 'Staff-Presentation-for-Feb-2022'}
    assert parsed_items[0]["links"] == link_dict

@pytest.mark.parametrize("item", parsed_items)
def test_classification(item):
    assert item["classification"] == BOARD


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
