import pytest

from two.my_converts import json_converter_to_lofo

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


@pytest.mark.parametrize('json_str1, json_str2, result',[
    [JSON_1, JSON_2, True],
    [JSON_1, JSON_DAMAGED_1, False],
    [JSON_1, JSON_DAMAGED_2, False],
    [JSON_1, JSON_DAMAGED_3, False],
    [JSON_1, JSON_DAMAGED_4, False],
], ids='1 2 3 4 5'.split())
def test_json_converter_to_lofo(json_str1, json_str2, result):
    result1 = json_converter_to_lofo(json_str1)
    hash1 = hash(repr(result1))
    result2 = json_converter_to_lofo(json_str2)
    hash2 = hash(repr(result2))
    print("")
    print(f"result_1: {hash1}, {result1}")
    print(f"result_2: {hash2}, {result2}")
    assert (hash1 == hash2) == result
