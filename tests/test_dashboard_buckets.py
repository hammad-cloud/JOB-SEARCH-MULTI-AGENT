from datetime import date

from job_search.ui.components.charts import period_buckets


def test_week_is_last_seven_days_ending_today():
    buckets = period_buckets("Week", date(2026, 10, 19))
    assert len(buckets) == 7
    assert buckets[0][1] == date(2026, 10, 13)
    assert buckets[-1] == ("Mon", date(2026, 10, 19), date(2026, 10, 19))


def test_month_is_four_contiguous_weeks():
    buckets = period_buckets("Month", date(2026, 10, 19))
    assert [b[1] for b in buckets] == [
        date(2026, 9, 22), date(2026, 9, 29), date(2026, 10, 6), date(2026, 10, 13)
    ]
    assert buckets[-1][2] == date(2026, 10, 19)


def test_year_spans_twelve_months_across_year_boundary():
    buckets = period_buckets("Year", date(2026, 2, 10))
    assert len(buckets) == 12
    assert buckets[0][1:] == (date(2025, 3, 1), date(2025, 3, 31))
    assert buckets[-2][1:] == (date(2026, 1, 1), date(2026, 1, 31))
    assert buckets[-1][1:] == (date(2026, 2, 1), date(2026, 2, 28))
