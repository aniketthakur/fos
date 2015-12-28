import os, sys, copy
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
from models import *
from datetime import date, datetime, timedelta


def application_status1():
    app1 = EsthenosOrgStatsApplication()
    app1.cb_passed = 1
    app1.cf_passed = 1
    app1.kyc_passed = 1
    app1.loan_amount = 100
    app1.loan_applied = 1
    return app1

def application_status2():
    app2 = EsthenosOrgStatsApplication()
    app2.cb_passed = 1
    app2.cf_passed = 1
    app2.kyc_failed = 1
    app2.loan_amount = 150
    app2.loan_applied = 1
    return app2

def application_status3():
    app3 = EsthenosOrgStatsApplication()
    app3.cb_passed = 2
    app3.cf_passed = 2
    app3.kyc_passed = 1
    app3.kyc_failed = 1
    app3.loan_amount = 250
    app3.loan_applied = 2
    return app3

def application_status4():
    app1 = EsthenosOrgStatsApplication()
    app1.cb_passed = 2
    app1.cf_passed = 2
    app1.kyc_passed = 2
    app1.loan_amount = 200
    app1.loan_applied = 2
    return app1

class TestApplicationStats(unittest.TestCase):

    def test_application_stat_empty(self):
        app1 = EsthenosOrgStatsApplication()
        app2 = EsthenosOrgStatsApplication()
        self.assertEqual(app1, app2)

    def test_application_stat_addition_empty(self):
        app1 = EsthenosOrgStatsApplication()
        app2 = EsthenosOrgStatsApplication()
        self.assertEqual(app1 + app2, app2)

    def test_application_stat_addition_empty(self):
        app1 = application_status1()
        app4 = application_status4()
        self.assertEqual(app1 + app1, app4)
        self.assertEqual(app1 + app1, app4)
        self.assertEqual(app1 + app1, app4)

    def test_application_stat_addition_values1(self):
        app1 = application_status1()
        app2 = application_status2()
        app3 = application_status3()
        self.assertEqual(app1 + app2, app3)

    def test_application_stat_addition_values2(self):
        app1 = application_status1()
        app2 = application_status2()
        app3 = application_status3()
        self.assertEqual(app1 + app2, app3)
        self.assertEqual(app1 + app2, app3)
        self.assertEqual(app1 + app2, app3)

        self.assertEqual(app2 + app1, app3)
        self.assertEqual(app2 + app1, app3)
        self.assertEqual(app2 + app1, app3)

        self.assertEqual(app1 + app2, app3)
        self.assertEqual(app1 + app2, app3)
        self.assertEqual(app1 + app2, app3)

class TestEsthenosStatsDay(unittest.TestCase):

     def test_day_stats_equal(self):
        stats1 = EsthenosOrgStatsDay()
        stats2 = EsthenosOrgStatsDay()
        self.assertEqual(stats1, stats2)

     def test_day_stats_equal_not1(self):
        stats1 = EsthenosOrgStatsDay(key="123")
        stats2 = EsthenosOrgStatsDay(key="124")
        self.assertNotEqual(stats1, stats2)

     def test_day_stats_equal_not2(self):
        stats1 = EsthenosOrgStatsDay(key="123", loans_applied=1)
        stats2 = EsthenosOrgStatsDay(key="123", loans_disbursed=3)
        self.assertNotEqual(stats1, stats2)

     def test_day_stats_add_empty(self):
        stats1 = EsthenosOrgStatsDay()
        stats2 = EsthenosOrgStatsDay()
        self.assertEqual(stats1 + stats2 + stats1, stats2)

     def test_day_stats_add_values1(self):
        stats1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2)
        stats2 = EsthenosOrgStatsDay()
        self.assertEqual(stats1 + stats2, stats1)
        self.assertEqual(stats2 + stats1, stats1)
        self.assertEqual(stats1 + stats2, stats1)

     def test_day_stats_add_values2(self):
        stats1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12)
        self.assertEqual(stats1 + stats1, stats1 + stats1)

     def test_day_stats_add_values3(self):
        stats1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12)
        stats2 = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15)
        self.assertEqual(stats2 + stats1, stats1 + stats2)

     def test_day_stats_sub_values(self):
        stats1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12)
        stats2 = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15)
        stats3 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=1, loans_applied=3)
        self.assertEqual(stats2 - stats1, stats3)


class TestEsthenosStatsMonth(unittest.TestCase):

    def test_month_stats_equal1(self):
        m1 = EsthenosOrgStatsMonth()
        m2 = EsthenosOrgStatsMonth()
        self.assertEqual(m1, m2)

    def test_month_stats_equal2(self):
        m1 = EsthenosOrgStatsMonth()
        m2 = EsthenosOrgStatsMonth()
        self.assertEqual(m1 + m2, m2)

    def test_month_stats_equal3(self):
        m1 = EsthenosOrgStatsMonth()
        m2 = EsthenosOrgStatsMonth()
        self.assertEqual(m2 + m1, m1)

    def test_month_stats_equal4(self):
        m1 = EsthenosOrgStatsMonth()
        m1.stats_total["1"] = EsthenosOrgStatsDay()
        m1.stats_total["2"] = EsthenosOrgStatsDay()

        m2 = EsthenosOrgStatsMonth()
        m2.stats_total["1"] = EsthenosOrgStatsDay()
        m2.stats_total["2"] = EsthenosOrgStatsDay()
        self.assertEqual(m2 + m1, m1)

    def test_month_stats_equal_not1(self):
        m1 = EsthenosOrgStatsMonth(key="123")
        m2 = EsthenosOrgStatsMonth(key="124")
        self.assertNotEqual(m1, m2)

    def test_month_stats_equal_not2(self):
        m1 = EsthenosOrgStatsMonth(key="123")
        m1.stats_total["1"] = EsthenosOrgStatsDay()

        m2 = EsthenosOrgStatsMonth(key="124")
        m2.stats_total["1"] = EsthenosOrgStatsDay()
        self.assertNotEqual(m1, m2)

    def test_month_stats_equal_not3(self):
        m1 = EsthenosOrgStatsMonth(key="123")
        m2 = EsthenosOrgStatsMonth(key="123")
        m2.stats_daily["1"] = EsthenosOrgStatsDay()
        m2.stats_daily["2"] = EsthenosOrgStatsDay()
        m2.stats_total["1"] = EsthenosOrgStatsDay()
        m2.stats_total["2"] = EsthenosOrgStatsDay()
        self.assertNotEqual(m1, m2)

    def test_month_stats_equal_not4(self):
        m1 = EsthenosOrgStatsMonth(key="123")
        m1.stats_daily["1"] = EsthenosOrgStatsDay(key="123")
        m1.stats_total["1"] = EsthenosOrgStatsDay(key="123")

        m2 = EsthenosOrgStatsMonth(key="123")
        m2.stats_daily["1"] = EsthenosOrgStatsDay(key="1234")
        m2.stats_total["1"] = EsthenosOrgStatsDay(key="1234")
        self.assertNotEqual(m1, m2)

    def test_month_stats_equal_not5(self):
        m1 = EsthenosOrgStatsMonth(key="123")
        m1.stats_daily["1"] = EsthenosOrgStatsDay(key="123")
        m1.stats_total["1"] = EsthenosOrgStatsDay(key="123")

        m2 = EsthenosOrgStatsMonth(key="123")
        m2.stats_daily["2"] = EsthenosOrgStatsDay(key="123")
        m2.stats_total["2"] = EsthenosOrgStatsDay(key="123")

        self.assertNotEqual(m1, m2)
        self.assertEqual(m1.stats_daily["1"], m2.stats_daily["2"])
        self.assertEqual(m1.stats_total["1"], m2.stats_total["2"])

    def test_month_stats_add_empty(self):
        m1 = EsthenosOrgStatsMonth()
        m1.stats_total["1"] = EsthenosOrgStatsDay()

        m2 = EsthenosOrgStatsMonth()
        m2.stats_total["1"] = EsthenosOrgStatsDay()
        self.assertEqual(m2 + m1, m1)

    def test_month_stats_add_values1(self):
        m1 = EsthenosOrgStatsMonth()
        m1.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12)

        m2 = EsthenosOrgStatsMonth()
        m2.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15)

        m3 = EsthenosOrgStatsMonth()
        m3.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=3, count_disbursed_groups=5, loans_applied=27)
        self.assertEqual(m1 + m2, m3)
        self.assertEqual(m2 + m1, m3)

    def test_month_stats_add_values2(self):
        m1 = EsthenosOrgStatsMonth(key="123")
        m2 = EsthenosOrgStatsMonth(key="123")
        m2.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15, key="1")

        m3 = EsthenosOrgStatsMonth(key="123")
        m3.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15, key="1")

        self.assertEqual(m1 + m2, m3)
        self.assertEqual(m2 + m1, m3)

    def test_month_stats_add_values3(self):
        m1 = EsthenosOrgStatsMonth(key="123")
        m1.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key="1")

        m2 = EsthenosOrgStatsMonth(key="123")
        m2.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15, key="1")

        m3 = EsthenosOrgStatsMonth(key="123")
        m3.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=3, count_disbursed_groups=5, loans_applied=27, key="1")

        self.assertEqual(m1 + m2, m3)
        self.assertEqual(m2 + m1, m3)

    def test_month_stats_add_values4(self):
        m1 = EsthenosOrgStatsMonth(key="123")
        m1.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key="1")

        m2 = EsthenosOrgStatsMonth(key="123")
        m2.stats_total["2"] = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15, key="2")

        m3 = EsthenosOrgStatsMonth(key="123")
        m3.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key="1")
        m3.stats_total["2"] = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15, key="2")

        self.assertEqual(m1 + m2, m3)
        self.assertEqual(m2 + m1, m3)

    def test_month_stats_add_values5(self):
        m1 = EsthenosOrgStatsMonth(key="123")
        m1.stats_total["0"] = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key="0")
        m1.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key="1")

        m2 = EsthenosOrgStatsMonth(key="123")
        m2.stats_total["2"] = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15, key="2")

        m3 = EsthenosOrgStatsMonth(key="123")
        m3.stats_total["0"] = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key="0")
        m3.stats_total["1"] = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key="1")
        m3.stats_total["2"] = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15, key="2")

        self.assertEqual(m1 + m2, m3)
        self.assertEqual(m2 + m1, m3)

    def test_month_stats_add_update1(self):
        t1 = datetime(2015, 12, 10)
        key1 = t1.strftime("%Y-%m-%d")
        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)

        m1 = EsthenosOrgStatsMonth(key="123")
        m2 = EsthenosOrgStatsMonth(key="123")
        m2.stats_daily[key1] = d1
        m2.stats_total[key1] = d1

        # assert1
        m1.update(d1, t1)
        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(m1.stats_daily, m2.stats_daily)
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

        # assert2
        m1.update(d1, t1)
        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

        # assert3
        m1.update(d1, t1)
        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(m1.stats_daily, m2.stats_daily)
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

    def test_month_stats_add_update2(self):
        t1 = datetime(2015, 12, 10)
        key1 = t1.strftime("%Y-%m-%d")

        t2 = datetime(2015, 12, 11)
        key2 = t2.strftime("%Y-%m-%d")

        m1 = EsthenosOrgStatsMonth(key="123")
        m2 = EsthenosOrgStatsMonth(key="123")

        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)
        d2 = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15, key=key2)

        # assert1
        m1.update(d1, t1)
        m2.stats_daily[key1] = d1
        m2.stats_total[key1] = d1
        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(m1.stats_daily, m2.stats_daily)
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

        # assert2
        m1.update(d2, t2)
        m2.stats_daily[key2] = d2
        m2.stats_total[key2] = (d2 + d1)
        self.assertEqual(d1, m1.day(t1))
        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(d2 + d1, m1.day(t2))
        self.assertEqual(m1.day(t2), m2.day(t2))
        self.assertEqual(m1.stats_daily, m2.stats_daily)
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

        # assert3
        m1.update(d2, t2)
        self.assertEqual(d1, m1.day(t1))
        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(d2 + d1, m1.day(t2))
        self.assertEqual(m1.day(t2), m2.day(t2))
        self.assertEqual(m1.stats_daily, m2.stats_daily)
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

        # assert4
        m1.update(d2, t2)
        self.assertEqual(d1, m1.day(t1))
        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(d2 + d1, m1.day(t2))
        self.assertEqual(m1.day(t2), m2.day(t2))
        self.assertEqual(m1.stats_daily, m2.stats_daily)
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

    def test_month_stats_add_update3(self):

        t1 = datetime(2015, 12, 10)
        key1 = t1.strftime("%Y-%m-%d")

        t2 = datetime(2015, 12, 11)
        key2 = t2.strftime("%Y-%m-%d")

        t3 = datetime(2015, 12, 12)
        key3 = t3.strftime("%Y-%m-%d")

        t4 = datetime(2015, 12, 13)
        key4 = t4.strftime("%Y-%m-%d")

        t5 = datetime(2015, 12, 14)
        key5 = t5.strftime("%Y-%m-%d")

        m1 = EsthenosOrgStatsMonth(key="123")
        m2 = EsthenosOrgStatsMonth(key="123")

        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=3, key=key1)

        # assert1
        m1.update(d1, t1)
        d = d1 * 1
        d.key = key1
        m2.stats_daily[key1] = d
        m2.stats_total[key1] = d
        self.assertEqual(m1, m2)

        # assert2
        m1.update(d1, t2)
        d = d1 * 2
        d.key = key2
        m2.stats_daily[key2] = d1
        m2.stats_total[key2] = d
        self.assertEqual(m1, m2)

        # assert3
        m1.update(d1, t3)
        d = d1 * 3
        d.key = key3
        m2.stats_daily[key3] = d1
        m2.stats_total[key3] = d
        self.assertEqual(m1, m2)

        # assert4
        m1.update(d1, t4)
        d = d1 * 4
        d.key = key4
        m2.stats_daily[key4] = d1
        m2.stats_total[key4] = d
        self.assertEqual(m1, m2)

        # assert5
        m1.update(d1, t5)
        d = d1 * 5
        d.key = key5
        m2.stats_daily[key5] = d1
        m2.stats_total[key5] = d
        self.assertEqual(m1, m2)

    def test_month_stats_add_update4(self):
        t1 = datetime(2015, 12, 10)
        key1 = t1.strftime("%Y-%m-%d")

        t2 = datetime(2015, 12, 15)
        key2 = t2.strftime("%Y-%m-%d")

        m1 = EsthenosOrgStatsMonth(key="123")
        m2 = EsthenosOrgStatsMonth(key="123")

        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)
        d2 = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, loans_applied=15, key=key2)

        # assert1
        m1.update(d1, t1)
        m2.stats_daily[key1] = d1
        m2.stats_total[key1] = d1
        self.assertEqual(m1, m2)

        # assert2
        m1.update(d2, t2)
        m2.stats_daily[key2] = d2
        m2.stats_total[key2] = d2
        self.assertEqual(m1, m2)

    def test_month_stats_add_update5(self):
        t1 = datetime(2015, 12, 10)
        key1 = t1.strftime("%Y-%m-%d")

        t2 = datetime(2015, 12, 11)
        key2 = t2.strftime("%Y-%m-%d")

        t3 = datetime(2015, 12, 13)
        key3 = t3.strftime("%Y-%m-%d")

        t4 = datetime(2015, 12, 12)
        key4 = t4.strftime("%Y-%m-%d")

        m1 = EsthenosOrgStatsMonth(key="123")
        m2 = EsthenosOrgStatsMonth(key="123")

        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=5, key=key1)

        # assert1
        m1.update(d1, t1)
        m2.stats_daily[key1] = d1
        m2.stats_total[key1] = d1
        self.assertEqual(d1, m1.day(t1))
        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(m1.day(t2), m2.day(t2))
        self.assertEqual(m1.stats_daily, m2.stats_daily)
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

        # assert2
        d2 = copy.deepcopy(d1)
        d2.key = key2
        m1.update(d2, t2)
        m2.stats_daily[key2] = d2
        m2.stats_total[key2] = d2 + d1
        self.assertEqual(m1.day(t1), d1)
        self.assertEqual(m1.day(t2), d2 + d1)
        self.assertEqual(m2.day(t1), d1)
        self.assertEqual(m2.day(t2), d2 + d1)
        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(m1.day(t2), m2.day(t2))
        self.assertEqual(m1.stats_daily, m2.stats_daily)
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

        # assert3
        d3 = copy.deepcopy(d1)
        d3.key = key3
        m1.update(d3, t3)
        m2.stats_daily[key3] = d3
        m2.stats_total[key3] = d3
        self.assertEqual(m1.day(t1), d1)
        self.assertEqual(m1.day(t2), d2 + d1)
        self.assertEqual(m1.day(t3), d3)

        self.assertEqual(m2.day(t1), d1)
        self.assertEqual(m2.day(t2), d2 + d1)
        self.assertEqual(m2.day(t3), d3)

        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(m1.day(t2), m2.day(t2))
        self.assertEqual(m1.day(t3), m2.day(t3))
        self.assertEqual(m1.stats_daily, m2.stats_daily)
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

        # assert4
        d4 = copy.deepcopy(d1)
        d4.key = key4
        m1.update(d4, t4)
        m2.stats_daily[key4] = d4
        m2.stats_total[key4] = d4 + d2 + d1
        self.assertEqual(m1.day(t1), d1)
        self.assertEqual(m1.day(t2), d2 + d1)
        self.assertEqual(m1.day(t4), d4 + d2 + d1)
        self.assertEqual(m1.day(t3), d3)

        self.assertEqual(m2.day(t1), d1)
        self.assertEqual(m2.day(t2), d2 + d1)
        self.assertEqual(m2.day(t4), d4 + d2 + d1)
        self.assertEqual(m2.day(t3), d3)

        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(m1.day(t2), m2.day(t2))
        self.assertEqual(m1.day(t3), m2.day(t3))
        self.assertEqual(m1.day(t4), m2.day(t4))
        self.assertEqual(m1.stats_daily, m2.stats_daily)
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

        # assert5
        d3 = copy.deepcopy(d1)
        d3.key = key3
        m1.update(d3, t3)
        m2.stats_total[key3] = d3 + d4 + d2 + d1
        self.assertEqual(m1.day(t1), d1)
        self.assertEqual(m1.day(t2), d2 + d1)
        self.assertEqual(m1.day(t4), d4 + d2 + d1)
        self.assertEqual(m1.day(t3), d3 + d4 + d2 + d1)

        self.assertEqual(m2.day(t1), d1)
        self.assertEqual(m2.day(t2), d2 + d1)
        self.assertEqual(m2.day(t4), d4 + d2 + d1)
        self.assertEqual(m2.day(t3), d3 + d4 + d2 + d1)

        self.assertEqual(m1.day(t1), m2.day(t1))
        self.assertEqual(m1.day(t2), m2.day(t2))
        self.assertEqual(m1.day(t3), m2.day(t3))
        self.assertEqual(m1.day(t4), m2.day(t4))
        self.assertEqual(m1.stats_total, m2.stats_total)
        self.assertEqual(m1, m2)

        # assert6.
        self.assertEqual(d3, m1.only(t3))
        self.assertEqual(m1.only(t3), m2.only(t3))
        self.assertEqual(m1.only(t4), m2.only(t4))

    def test_month_stats_only(self):
        time = datetime(2015, 12, 10)
        delta = timedelta(days=1)
        key1 = time.strftime("%Y-%m-%d")

        m1 = EsthenosOrgStatsMonth(key="123")
        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)

        for i in range(10):
            t = time + timedelta(days=i)
            d = copy.deepcopy(d1)
            d.key = t.strftime("%Y-%m-%d")
            m1.update(d, t)
        self.assertEqual(10, len(m1.stats_total))

        d2 = copy.deepcopy(d1)
        t2 = time + delta
        d2.key = t2.strftime("%Y-%m-%d")
        self.assertEqual(d2, m1.only(t2))

        d3 = copy.deepcopy(d1)
        t3 = time + delta + delta
        d3.key = t3.strftime("%Y-%m-%d")
        self.assertEqual(d3, m1.only(t3))

        d4 = copy.deepcopy(d1)
        t4 = time + delta + delta + delta
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, m1.only(t4))

    def test_month_stats_today(self):
        time = datetime(2015, 12, 10)
        delta = timedelta(days=1)
        key1 = time.strftime("%Y-%m-%d")

        m1 = EsthenosOrgStatsMonth(key="123")
        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)

        [m1.update(d1, time + timedelta(days=i)) for i in range(1, 4)]
        self.assertEqual(3, len(m1.stats_total))

        t4 = time + delta + delta + delta
        d4 = d1 + d1 + d1
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, m1.day(t4))

    def test_month_stats_week1(self):
        time = datetime(2015, 12, 10)
        delta = timedelta(days=1)
        key1 = time.strftime("%Y-%m-%d")

        m1 = EsthenosOrgStatsMonth(key="123")
        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)

        [m1.update(d1, time + timedelta(days=i)) for i in range(1, 4)]
        self.assertEqual(3, len(m1.stats_total))

        t4 = time + delta + delta + delta
        d4 = d1 + d1 + d1
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, m1.week(t4))

    def test_month_stats_week2(self):
        time = datetime(2015, 12, 10)
        key1 = time.strftime("%Y-%m-%d")

        m1 = EsthenosOrgStatsMonth(key="123")
        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)

        [m1.update(d1, time + timedelta(days=i)) for i in range(1, 6)]
        self.assertEqual(5, len(m1.stats_total))

        t4 = time + timedelta(days=5)
        d4 = d1 * 2
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, m1.week(t4))

    def test_month_stats_week3(self):
        time = datetime(2015, 12, 10)
        key1 = time.strftime("%Y-%m-%d")

        m1 = EsthenosOrgStatsMonth(key="123")
        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)

        [m1.update(d1, time + timedelta(days=i)) for i in range(1, 9)]
        self.assertEqual(8, len(m1.stats_total))

        t4 = time + timedelta(days=7)
        d4 = d1 * 4
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, m1.week(t4))

    def test_month_stats_week4(self):
        time = datetime(2015, 12, 10)
        key1 = time.strftime("%Y-%m-%d")

        m1 = EsthenosOrgStatsMonth(key="123")
        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)

        [m1.update(d1, time + timedelta(days=i)) for i in range(1, 15)]
        self.assertEqual(14, len(m1.stats_total))

        t4 = time + timedelta(days=12)
        d4 = d1 * 2
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, m1.week(t4))

    def test_month_stats_week5(self):
        time = datetime(2015, 12, 10)
        key1 = time.strftime("%Y-%m-%d")

        m1 = EsthenosOrgStatsMonth(key="123")
        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)

        [m1.update(d1, time + timedelta(days=i)) for i in range(1, 25)]
        self.assertEqual(24, len(m1.stats_total))

        t4 = time + timedelta(days=10)
        d4 = d1 * 7
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, m1.week(t4))


class TestEsthenosStatsGeo(unittest.TestCase):

    def test_month_stats_geo1(self):
        time = datetime(2015, 12, 03)
        key1 = time.strftime("%Y-%m-%d")

        g1 = EsthenosOrgStatsGeo()
        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)

        [g1.update(d1, time + timedelta(days=i)) for i in range(1, 25)]
        self.assertEqual(24, len(g1.month(time).stats_total))

        t4 = time + timedelta(days=24)
        d4 = d1 * 24
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, g1.month(t4).day(t4))

    def test_month_stats_geo2(self):
        time1 = datetime(2015, 12, 03)
        time2 = datetime(2016, 01, 01)
        key1 = time1.strftime("%Y-%m-%d")

        g1 = EsthenosOrgStatsGeo()
        d1 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=key1)

        [g1.update(d1, time1 + timedelta(days=i)) for i in range(1, 40)]
        self.assertEqual(28, len(g1.month(time1).stats_total))
        self.assertEqual(11, len(g1.month(time2).stats_total))

        t4 = datetime(2015, 12, 15)
        d4 = d1 * 12
        d4.key = t4.strftime("%Y-%m-%d")
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d4, s4)
        self.assertEqual(0 ,  s4.loans_disbursed)
        self.assertEqual(144, s4.loans_applied)

        t4 = datetime(2015, 12, 27)
        d4 = d1 * 24
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, g1.month(t4).day(t4))

        t4 = datetime(2016, 01, 7)
        d4 = d1 * 7
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, g1.month(t4).day(t4))

        t4 = datetime(2016, 01, 8)
        d4 = d1 * 8
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, g1.month(t4).day(t4))

        t4 = datetime(2016, 01, 9)
        d4 = d1 * 9
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, g1.month(t4).day(t4))

        t4 = datetime(2016, 01, 10)
        d4 = d1 * 7
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, g1.month(t4).week(t4))

        t4 = datetime(2016, 01, 10)
        d4 = d1 * 1
        d4.key = t4.strftime("%Y-%m-%d")
        self.assertEqual(d4, g1.month(t4).only(t4))

        t4 = datetime(2016, 01, 10)
        d4 = d1 * 10
        d4.key = t4.strftime("%Y-%m-%d")

        s1 = g1.month(t4).day(t4)
        self.assertEqual(d4, s1)

    def test_month_stats_geo3(self):
        g1 = EsthenosOrgStatsGeo()

        t4 = datetime(2015, 12, 03)
        d4 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, loans_applied=12, key=t4.strftime("%Y-%m-%d"))
        g1.update(d4, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d4, s4)
        self.assertEqual(0 , s4.loans_disbursed)
        self.assertEqual(12, s4.loans_applied)

        t4 = datetime(2015, 12, 04)
        d5 = EsthenosOrgStatsDay(disbursement_done=1, loans_disbursed=2, loans_applied=2, key=t4.strftime("%Y-%m-%d"))
        g1.update(d5, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d5 + d4, s4)
        self.assertEqual(14, s4.loans_applied)
        self.assertEqual(2 , s4.loans_disbursed)
        self.assertEqual(1 , s4.disbursement_done)

        t4 = datetime(2015, 12, 04)
        d5 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=2, disbursement_done=1, loans_disbursed=2, loans_applied=2, key=t4.strftime("%Y-%m-%d"))
        g1.update(d5, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d5 + d4, s4)
        self.assertEqual(14, s4.loans_applied)
        self.assertEqual(2 , s4.loans_disbursed)
        self.assertEqual(1 , s4.disbursement_done)

        t4 = datetime(2015, 12, 05)
        d6 = EsthenosOrgStatsDay(count_disbursed_centers=2, count_disbursed_groups=3, disbursement_done=3, loans_disbursed=4, loans_applied=5, key=t4.strftime("%Y-%m-%d"))
        g1.update(d6, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d6 + d5 + d4, s4)
        self.assertEqual(19, s4.loans_applied)
        self.assertEqual(6 , s4.loans_disbursed)
        self.assertEqual(4 , s4.disbursement_done)

        t4 = datetime(2015, 12, 05)
        d6 = EsthenosOrgStatsDay(count_disbursed_centers=1, count_disbursed_groups=1, disbursement_done=3, loans_disbursed=4, loans_applied=5, key=t4.strftime("%Y-%m-%d"))
        g1.update(d6, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d6 + d5 + d4, s4)
        self.assertEqual(19, s4.loans_applied)
        self.assertEqual(6 , s4.loans_disbursed)
        self.assertEqual(4 , s4.disbursement_done)

        t4 = datetime(2015, 12, 06)
        d7 = EsthenosOrgStatsDay(cgt1_ready=1, cgt2_ready=1, cb_passed=1, cf_passed=1, key=t4.strftime("%Y-%m-%d"))
        g1.update(d7, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d7 + d6 + d5 + d4, s4)
        self.assertEqual(1, s4.cgt1_ready)
        self.assertEqual(1, s4.cgt2_ready)
        self.assertEqual(1, s4.cb_passed)
        self.assertEqual(1, s4.cf_passed)
        self.assertEqual(19, s4.loans_applied)
        self.assertEqual(6 , s4.loans_disbursed)
        self.assertEqual(4 , s4.disbursement_done)

        t4 = datetime(2015, 12, 9)
        d10 = EsthenosOrgStatsDay(cgt1_ready=1, cgt2_ready=1, cb_passed=1, cf_passed=1, key=t4.strftime("%Y-%m-%d"))
        g1.update(d10, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d10, s4)
        self.assertEqual(1, s4.cgt1_ready)
        self.assertEqual(1, s4.cgt2_ready)
        self.assertEqual(1, s4.cb_passed)
        self.assertEqual(1, s4.cf_passed)
        self.assertEqual(0, s4.loans_applied)
        self.assertEqual(0, s4.loans_disbursed)
        self.assertEqual(0, s4.disbursement_done)

        t4 = datetime(2015, 12, 9)
        d10 = EsthenosOrgStatsDay(cgt1_ready=1, cgt2_ready=1, cb_passed=1, cf_passed=1, key=t4.strftime("%Y-%m-%d"))
        g1.update(d10, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d10, s4)
        self.assertEqual(1, s4.cgt1_ready)
        self.assertEqual(1, s4.cgt2_ready)
        self.assertEqual(1, s4.cb_passed)
        self.assertEqual(1, s4.cf_passed)
        self.assertEqual(0, s4.loans_applied)
        self.assertEqual(0, s4.loans_disbursed)
        self.assertEqual(0, s4.disbursement_done)

        t4 = datetime(2015, 12, 9)
        d10 = EsthenosOrgStatsDay(cgt1_ready=1, cgt2_ready=1, cb_passed=1, cf_passed=1, key=t4.strftime("%Y-%m-%d"))
        g1.update(d10, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d10, s4)
        self.assertEqual(1, s4.cgt1_ready)
        self.assertEqual(1, s4.cgt2_ready)
        self.assertEqual(1, s4.cb_passed)
        self.assertEqual(1, s4.cf_passed)
        self.assertEqual(0, s4.loans_applied)
        self.assertEqual(0, s4.loans_disbursed)
        self.assertEqual(0, s4.disbursement_done)

        t4 = datetime(2015, 12, 7)
        d8 = EsthenosOrgStatsDay(key=t4.strftime("%Y-%m-%d"))
        g1.update(d8, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d8 + d7 + d6 + d5 + d4, s4)
        self.assertEqual(1, s4.cgt1_ready)
        self.assertEqual(1, s4.cgt2_ready)
        self.assertEqual(1, s4.cb_passed)
        self.assertEqual(1, s4.cf_passed)
        self.assertEqual(19, s4.loans_applied)
        self.assertEqual(6 , s4.loans_disbursed)
        self.assertEqual(4 , s4.disbursement_done)

        t4 = datetime(2015, 12, 8)
        d9 = EsthenosOrgStatsDay(key=t4.strftime("%Y-%m-%d"))
        g1.update(d9, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d9 + d8 + d7 + d6 + d5 + d4, s4)
        self.assertEqual(1, s4.cgt1_ready)
        self.assertEqual(1, s4.cgt2_ready)
        self.assertEqual(1, s4.cb_passed)
        self.assertEqual(1, s4.cf_passed)
        self.assertEqual(19, s4.loans_applied)
        self.assertEqual(6 , s4.loans_disbursed)
        self.assertEqual(4 , s4.disbursement_done)

        t4 = datetime(2015, 12, 9)
        d10 = EsthenosOrgStatsDay(cgt1_ready=1, cgt2_ready=1, cb_passed=1, cf_passed=1, key=t4.strftime("%Y-%m-%d"))
        g1.update(d10, t4)
        s4 = g1.month(t4).day(t4)
        self.assertEqual(d10 + d9 + d8 + d7 + d6 + d5 + d4, s4)
        self.assertEqual(2, s4.cgt1_ready)
        self.assertEqual(2, s4.cgt2_ready)
        self.assertEqual(2, s4.cb_passed)
        self.assertEqual(2, s4.cf_passed)
        self.assertEqual(19, s4.loans_applied)
        self.assertEqual(6 , s4.loans_disbursed)
        self.assertEqual(4 , s4.disbursement_done)

if __name__ == '__main__':
    unittest.main()
