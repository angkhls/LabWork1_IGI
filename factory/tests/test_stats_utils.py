from factory.stats_utils import descriptive_stats


def test_descriptive_stats_basic():
    result = descriptive_stats([10, 20, 20, 40])
    assert result['count'] == 4
    assert result['mean'] == 22.5
    assert result['median'] == 20
    assert result['mode'] == 20


def test_descriptive_stats_empty():
    result = descriptive_stats([])
    assert result['count'] == 0
    assert result['mean'] == 0
    assert result['median'] == 0
