from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import CITY_COUNCIL
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.fre_kingsburg_city_council import (
    FreKingsburgCityCouncilSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "fre_kingsburg_city_council.html"),
    url="https://www.cityofkingsburg-ca.gov/agendacenter",
)
spider = FreKingsburgCityCouncilSpider()

freezer = freeze_time("2022-08-21")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()

"""
def test_tests():
    print("Please write some tests for this spider or at least disable this one.")
    assert False

Uncomment below
"""


def test_title():
    assert parsed_items[0]["title"] == "City Council Regular Meeting "


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2022, 8, 17, 14, 0)


# def test_end():
#     assert parsed_items[0]["end"] == datetime(2019, 1, 1, 0, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "fre_kingsburg_city_council/202208171400/x/city_council_regular_meeting"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Council Chamber",
        "address": "1401 Draper Street, Kingsburg, CA 93631",
    }


def test_source():
    assert (
        parsed_items[0]["source"] == "https://www.cityofkingsburg-ca.gov/agendacenter"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": "https://www.cityofkingsburg-ca.gov/AgendaCenter/ViewFile/Agenda/_08172022-724",  # noqa
            "title": "Meeting Agenda",
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
