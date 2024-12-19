import json

import pytest

from helper.work_json import json_converter_to_lofl, compare_json

JSON_1 = """
{"data": {
    "pages": {
        "current": 1, "objects_per_page": 
        4294967295, "total": 1
    }, 
    "stations": {
        "regular": [{
            "id": "f65c2cb2-44e0-11ef-b069-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f65c2cb2", 
            "os": 0, 
            "os_name": "unknown"}], 
        "scanning_server": [{
            "id": "f67acb45-44e0-11ef-9660-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f67acb45", 
            "os": 0, 
            "os_name": "unknown"}], 
        "virtual_agent": [{
            "id": "f6703f68-44e0-11ef-a125-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f6703f68", 
            "os": 0, 
            "os_name": "unknown"}]
    }}, 
"head": {
    "api": {
        "version": 40302, 
        "versionString": "4.3.2"}, 
    "server": {
        "name": "192.168.21.9", 
        "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", 
        "version": "13.00.1.202406060"}, 
    "status": true, 
    "timestamp": 1721291847}}
"""

JSON_2 = """
{
"head": {
    "status": true, 
    "api": {
        "version": 40302, 
        "versionString": "4.3.2"}, 
    "server": {
        "name": "192.168.21.9", 
        "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", 
        "version": "13.00.1.202406060"}, 
    "timestamp": 1721291847},
"data": {
    "pages": {
        "current": 1, "objects_per_page": 
        4294967295, "total": 1
    }, 
    "stations": {
        "regular": [{
            "name": "f65c2cb2",         
            "last_seen_time": 0, 
            "os": 0, 
            "os_name": "unknown",
            "id": "f65c2cb2-44e0-11ef-b069-3c7c3fbc6d25"             
            }], 
        "scanning_server": [{
            "id": "f67acb45-44e0-11ef-9660-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "os": 0,             
            "name": "f67acb45", 
            "os_name": "unknown"}], 
        "virtual_agent": [{
            "os_name": "unknown",
            "id": "f6703f68-44e0-11ef-a125-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f6703f68", 
            "os": 0 
            }]
    }}
}
"""

# Немного изменённый JSON_1
JSON_DAMAGED_1 = """
{"data": {
    "pages": {
        "current": 1, "objects_per_page": 
        4294967295, "total": 2
    }, 
    "stations": {
        "regular": [{
            "id": "f65c2cb2-44e0-11ef-b069-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f65c2cb2", 
            "os": 0, 
            "os_name": "unknown"}], 
        "scanning_server": [{
            "id": "f67acb45-44e0-11ef-9660-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f67acb45", 
            "os": 0, 
            "os_name": "unknown"}], 
        "virtual_agent": [{
            "id": "f6703f68-44e0-11ef-a125-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f6703f68", 
            "os": 0, 
            "os_name": "unknown"}]
    }}, 
"head": {
    "api": {
        "version": 40302, 
        "versionString": "4.3.2"}, 
    "server": {
        "name": "192.168.21.9", 
        "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", 
        "version": "13.00.1.202406060"}, 
    "status": true, 
    "timestamp": 1721291847}}
"""

# Немного изменённый JSON_2
JSON_DAMAGED_2 = """
{"data": {
    "pages": {
        "current": 1, "objects_per_page": 
        4294967295, "total": 1
    }, 
    "stations": {
        "regular": [{
            "id": "f65c2cb2-44e0-11ef-b069-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f65c2cb2", 
            "os": 0, 
            "os_name": "unknown"}], 
        "scanning_server": [{
            "id": "f67acb45-44e0-11ef-9660-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f67acb45", 
            "os": 0, 
            "os_name": "unknown"}], 
        "virtual_agent": [{
            "id": "f6703f68-44e0-11ef-a125-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f6703f68", 
            "os": 0, 
            "os_name": "unknown"}]
    }}, 
"head": {
    "api": {
        "version": 40302, 
        "versionString": "4.3.2"}, 
    "server": {
        "name": "192.168.21.9", 
        "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", 
        "version": "13.00.1.202406060"}, 
    "status": true, 
    "timestamp": 1721291848}}
"""

# Немного изменённый JSON_1
JSON_DAMAGED_3 = """
{"data": {
    "pages": {
        "current": 1, "objects_per_page": 
        4294967295, "total": 1
    }, 
    "stations": {
        "regular": [{
            "id": "f65c2cb2-44e0-11ef-b069-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f65c2cb2", 
            "os": 0, 
            "os_name": "unknown"}], 
        "scanning_server": [{
            "id": "f67acb45-44e0-11ef-9660-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f67acb45", 
            "os": 0, 
            "os_name": "unknown"}], 
        "virtual_agent": [{
            "id": "f6703f68-44e0-11ef-a125-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f6703f68", 
            "os": 0, 
            "os_name": "unknown"}]
    }}, 
"head": {
    "api": {
        "version": 40302, 
        "versionString": "4.3.2"}, 
    "server": {
        "name": "192.168.21.9", 
        "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", 
        "version": "13.00.1.202406060"}, 
    "status": true, 
    "timestam": 1721291847}}
"""

# Немного изменённый JSON_1
JSON_DAMAGED_4 = """
{"data": {
    "pages": {
        "current": 1, "objects_per_page": 
        4294967295, "total": 1
    }, 
    "stations": {
        "regular": [{
            "id": "f65c2cb2-44e0-11ef-b069-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f65c2cb2", 
            "os": 0, 
            "os_name": "unknown"}], 
        "scanning_server": [{
            "id": "f67acb45-44e0-11ef-9660-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f67acb45", 
            "os_name": "unknown"}], 
        "virtual_agent": [{
            "id": "f6703f68-44e0-11ef-a125-3c7c3fbc6d25", 
            "last_seen_time": 0, 
            "name": "f6703f68", 
            "os": 0, 
            "os_name": "unknown"}]
    }}, 
"head": {
    "api": {
        "version": 40302, 
        "versionString": "4.3.2"}, 
    "server": {
        "name": "192.168.21.9", 
        "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", 
        "version": "13.00.1.202406060"}, 
    "status": true, 
    "timestamp": 1721291847}}
"""


JSON_STR_THREE_1 = """{"data": {"pages": {"current": 1, "objects_per_page": 4294967295, "total": 1}, 
    "stations": {
        "regular": [{"id": "f65c2cb2-44e0-11ef-b069-3c7c3fbc6d25", "last_seen_time": 0, "name": "f65c2cb2", "os": 0, "os_name": "unknown"}], 
        "scanning_server": [{"id": "f67acb45-44e0-11ef-9660-3c7c3fbc6d25", "last_seen_time": 0, "name": "f67acb45", "os": 0, "os_name": "unknown"}], 
        "virtual_agent": [{"id": "f6703f68-44e0-11ef-a125-3c7c3fbc6d25", "last_seen_time": 0, "name": "f6703f68", "os": 0, "os_name": "unknown"}]
    }}, "head": {"api": {"version": 40302, "versionString": "4.3.2"}, "server": {"name": "192.168.21.9", "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", "version": "13.00.1.202406060"}, "status": true, "timestamp": 1721291847}}"""

JSON_STR_THREE_2 = """{"data": {"pages": {"current": 1, "objects_per_page": 4294967295, "total": 1}, 
    "stations": {
        "scanning_server": [{"id": "f67acb45-44e0-11ef-9660-3c7c3fbc6d25", "last_seen_time": 0, "name": "f67acb45", "os": 0, "os_name": "unknown"}], 
        "regular": [{"id": "f65c2cb2-44e0-11ef-b069-3c7c3fbc6d25", "last_seen_time": 0, "name": "f65c2cb2", "os": 0, "os_name": "unknown"}], 
        "virtual_agent": [{"id": "f6703f68-44e0-11ef-a125-3c7c3fbc6d25", "last_seen_time": 0, "name": "f6703f68", "os": 0, "os_name": "unknown"}]
    }}, "head": {"api": {"version": 40302, "versionString": "4.3.2"}, "server": {"name": "192.168.21.9", "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", "version": "13.00.1.202406060"}, "status": true, "timestamp": 1721291847}}"""

JSON_STR_TWO_1 = """{"data": {"pages": {"current": 1, "objects_per_page": 4294967295, "total": 1}, 
    "stations": {
        "regular": [{"id": "f65c2cb2-44e0-11ef-b069-3c7c3fbc6d25", "last_seen_time": 0, "name": "f65c2cb2", "os": 0, "os_name": "unknown"}], 
        "virtual_agent": [{"id": "f6703f68-44e0-11ef-a125-3c7c3fbc6d25", "last_seen_time": 0, "name": "f6703f68", "os": 0, "os_name": "unknown"}]
    }}, "head": {"api": {"version": 40302, "versionString": "4.3.2"}, "server": {"name": "192.168.21.9", "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", "version": "13.00.1.202406060"}, "status": true, "timestamp": 1721291847}}"""

JSON_STR_TWO_2 = """{"data": {"pages": {"current": 1, "objects_per_page": 4294967295, "total": 1}, 
    "stations": {
        "scanning_server": [{"id": "f67acb45-44e0-11ef-9660-3c7c3fbc6d25", "last_seen_time": 0, "name": "f67acb45", "os": 0, "os_name": "unknown"}], 
        "virtual_agent": [{"id": "f6703f68-44e0-11ef-a125-3c7c3fbc6d25", "last_seen_time": 0, "name": "f6703f68", "os": 0, "os_name": "unknown"}]
    }}, "head": {"api": {"version": 40302, "versionString": "4.3.2"}, "server": {"name": "192.168.21.9", "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", "version": "13.00.1.202406060"}, "status": true, "timestamp": 1721291847}}"""

JSON_STR_TWO_3 = """{"data": {"pages": {"current": 1, "objects_per_page": 4294967295, "total": 1}, 
    "stations": {
        "regular": [{"id": "f65c2cb2-44e0-11ef-b069-3c7c3fbc6d25", "last_seen_time": 0, "name": "f65c2cb2", "os": 0, "os_name": "unknown"}], 
        "scanning_server": [{"id": "f67acb45-44e0-11ef-9660-3c7c3fbc6d25", "last_seen_time": 0, "name": "f67acb45", "os": 0, "os_name": "unknown"}]
    }}, "head": {"api": {"version": 40302, "versionString": "4.3.2"}, "server": {"name": "192.168.21.9", "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", "version": "13.00.1.202406060"}, "status": true, "timestamp": 1721291847}}"""

JSON_STR_ONE_1 = """{"data": {"pages": {"current": 1, "objects_per_page": 100, "total": 1}, 
    "stations": {
        "regular": [{"id": "f65c2cb2-44e0-11ef-b069-3c7c3fbc6d25", "last_seen_time": 0, "name": "f65c2cb2", "os": 0, "os_name": "unknown"}]
    }}, "head": {"api": {"version": 40302, "versionString": "4.3.2"}, "server": {"name": "192.168.21.9", "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", "version": "13.00.1.202406060"}, "status": true, "timestamp": 1721291847}}"""

JSON_STR_ONE_2 = """{"data": {"pages": {"current": 1, "objects_per_page": 100, "total": 1}, 
    "stations": {
        "virtual_agent": [{"id": "f6703f68-44e0-11ef-a125-3c7c3fbc6d25", "last_seen_time": 0, "name": "f6703f68", "os": 0, "os_name": "unknown"}]
    }}, "head": {"api": {"version": 40302, "versionString": "4.3.2"}, "server": {"name": "192.168.21.9", "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", "version": "13.00.1.202406060"}, "status": true, "timestamp": 1721291847}}"""

JSON_STR_ONE_3 = """{"data": {"pages": {"current": 1, "objects_per_page": 100, "total": 1},
    "stations": {
        "scanning_server": [{"id": "f67acb45-44e0-11ef-9660-3c7c3fbc6d25", "last_seen_time": 0, "name": "f67acb45", "os": 0, "os_name": "unknown"}]
    }}, "head": {"api": {"version": 40302, "versionString": "4.3.2"}, "server": {"name": "192.168.21.9", "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", "version": "13.00.1.202406060"}, "status": true, "timestamp": 1721291847}}"""


# JSON в формате словаря.
JSON_DICT = {"data": {"groups": {"list": [{"child_groups": 3, "id": "068e436a-952e-49d9-9b7f-46e2761dfc6f", "name": "Active Directory", "stations": 0, "type": 10}, {"child_groups": 0, "id": "8c483456-0d15-4e41-b271-87197ac2adb6", "name": "Configured", "stations": 0, "type": 10}, {"child_groups": 0, "id": "20e27d73-d21d-b211-a788-85419c46f0e6", "name": "Everyone", "stations": 0, "type": 1}, {"child_groups": 6, "id": "aa6469d2-6621-46ce-8eed-fc35573c0b34", "name": "Neighbors", "stations": 0, "type": 10}, {"child_groups": 6, "id": "f991915f-8a15-4cf7-817a-d81d156d2bbe", "name": "Operating system", "stations": 0, "type": 10}, {"child_groups": 0, "id": "2abcd184-d8ba-4020-92fb-53148b61efaf", "name": "Policies", "stations": 0, "type": 10}, {"child_groups": 0, "id": "640b34ee-2058-49d6-b24d-d7cb239cfa3d", "name": "Profiles", "stations": 0, "type": 10}, {"child_groups": 0, "id": "54171821-08df-4146-860b-3f5e6eb4ef40", "name": "Proxies", "stations": 0, "type": 13}, {"child_groups": 7, "id": "48afe720-953c-4075-856c-361f3ff06b6d", "name": "Status", "stations": 0, "type": 10}, {"child_groups": 3, "id": "159e383d-f853-4bc5-9e18-c40144542aca", "name": "Transport", "stations": 0, "type": 10}, {"child_groups": 0, "id": "411dac63-2a3e-4ce8-af4f-1fbeb94242ef", "name": "Ungrouped", "stations": 0, "type": 10}], "total": 11}}, "head": {"api": {"version": 40302, "versionString": "4.3.2"}, "server": {"name": "192.168.21.9", "uuid": "1e6c43f8-bbb6-4030-b866-ff0b6ece70e2", "version": "13.00.1.202406060"}, "status": True, "timestamp": 1723015339}}
# JSON в формате списка.
JSON_LIST = [{"id": "c35f4732-b866-11ef-b82e-3c7c3fbc6d25", "name": "c35f4732", "child_groups": 0, "stations": 0, "type": 0}, {"id": "c3656e57-b866-11ef-96c3-3c7c3fbc6d25", "name": "c3656e57", "child_groups": 0, "stations": 0, "type": 0}, {"id": "c36c66e0-b866-11ef-bb0d-3c7c3fbc6d25", "name": "c36c66e0", "child_groups": 2, "stations": 4, "type": 0}]


params = [
    [JSON_STR_TWO_1, JSON_STR_THREE_1, True],
    [JSON_STR_TWO_1, JSON_STR_THREE_2, True],
    [JSON_STR_TWO_2, JSON_STR_THREE_1, True],
    [JSON_STR_TWO_2, JSON_STR_THREE_2, True],
    [JSON_STR_TWO_3, JSON_STR_THREE_1, True],
    [JSON_STR_TWO_3, JSON_STR_THREE_2, True],
    [JSON_STR_ONE_1, JSON_STR_THREE_1, True],
    [JSON_STR_ONE_1, JSON_STR_THREE_2, True],
    [JSON_STR_ONE_1, JSON_STR_TWO_1, True],
    [JSON_STR_ONE_1, JSON_STR_TWO_3, True],
    [JSON_STR_ONE_2, JSON_STR_THREE_1, True],
    [JSON_STR_ONE_2, JSON_STR_THREE_2, True],
    [JSON_STR_ONE_2, JSON_STR_TWO_1, True],
    [JSON_STR_ONE_2, JSON_STR_TWO_2, True],
    [JSON_STR_TWO_1, JSON_STR_TWO_2, False],
    [JSON_STR_ONE_1, JSON_STR_TWO_2, False],
    [JSON_STR_ONE_2, JSON_STR_TWO_3, False],
    [JSON_STR_ONE_3, JSON_STR_TWO_1, False],
    ]

params += list(map(lambda x: [json.loads(x[0]), json.loads(x[1]), x[2]], params))


@pytest.mark.parametrize('json_str1, json_str2, result', params,
                         ids=' '.join(map(str, range(1, len(params) + 1))).split())
def test_compare_json(json_str1, json_str2, result):
    assert compare_json(json_str1, json_str2, "$..stations") is result


def test_compare_json_2():
    assert compare_json(JSON_STR_THREE_2, JSON_STR_THREE_1)


@pytest.mark.parametrize('json_str1, json_str2, result',[
    [JSON_1, JSON_2, True],
    [JSON_1, JSON_DAMAGED_1, False],
    [JSON_1, JSON_DAMAGED_2, False],
    [JSON_1, JSON_DAMAGED_3, False],
    [JSON_1, JSON_DAMAGED_4, False],
], ids='1 2 3 4 5'.split())
def test_json_converter_to_lofo(json_str1, json_str2, result):
    result1 = json_converter_to_lofl(json_str1)
    hash1 = hash(repr(result1))
    result2 = json_converter_to_lofl(json_str2)
    hash2 = hash(repr(result2))
    print("")
    print(f"result_1: {hash1}, {result1}")
    print(f"result_2: {hash2}, {result2}")
    assert (hash1 == hash2) == result
