from medtools.tools.ascvd import ascvd


def test_ascvd():
    data = {
        "sex": 1,
        "age": 40,
        "region": 1,
        "area": 1,
        "waist": 75,
        "tc_unit": 1,
        "tc": 198,
        "hdlc_unit": 1,
        "hdlc": 76,
        "sbp": 130,
        "dbp": 80,
        "drug": 0,
        "dm": 0,
        "csmoke": 0,
        "fh_ascvd": 0,
    }
    result = ascvd.run({"data": data})
    assert result.type == "json"
    assert len(list(result.data)) == 3
    # {
    # '您的心脑血管病10年发病风险为': '1.2%',
    # '理想危险因素状态下您的心脑血管病10年发病风险应小于': '1.1%',
    # '您的心脑血管病终生发病风险为': '18.9%',
    # '理想危险因素状态下您的心脑血管病终生发病风险应小于': '20.7%'
    # }
