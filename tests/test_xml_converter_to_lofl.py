import pytest

from one.temp_1 import my_compare_xml
from two.my_converts import xml_converter_to_lofl

SAMPLE_XML_1 = """<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
"""

SAMPLE_XML_1_OTHER = """<?xml version="1.0"?>
<data>
    <country name="Singapore">
        <year>2011</year>    
        <rank>4</rank>
        <neighbor name="Malaysia" direction="N"/>
        <gdppc>59900</gdppc>        
    </country>
    <country name="Panama">
        <year>2011</year>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>        
        <gdppc>13600</gdppc>
        <rank>68</rank>
    </country>    
    <country name="Liechtenstein">
        <neighbor name="Austria" direction="E"/>    
        <rank>1</rank>
        <gdppc>141100</gdppc>
        <year>2008</year>
        <neighbor name="Switzerland" direction="W"/>
    </country>
</data>
"""

SAMPLE_XML_1_DAMAGED_1 = """<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="K"/>
    </country>
</data>
"""

SAMPLE_XML_1_DAMAGED_2 = """<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>6</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
"""

SAMPLE_XML_1_DAMAGED_3 = """<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
"""

SAMPLE_XML_1_DAMAGED_4 = """<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rang>4</rang>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
"""

SUB_XML_1 = """
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
</data>
"""


SAMPLE_XML_2 = """<?xml version="1.0" encoding="UTF-8"?>
<drweb-es-api api_version="4.3.2" timestamp="1721134700" server="192.168.21.9" srv_version="13.00.1.202406060" status="true">
    <stations type = "regular" total = "1">
        <station id = "1326782f-4373-11ef-96b1-3c7c3fbc6d25" name = "1326782f" last_seen_addr = "" last_seen_time = "0" os = "0" os_name = "unknown"/>
    </stations>
    <stations type = "scanning_server" total = "1">
        <station id = "1379440e-4373-11ef-b09a-3c7c3fbc6d25" name = "1379440e" last_seen_addr = "" last_seen_time = "0" os = "0" os_name = "unknown"/>
    </stations>
    <stations type = "virtual_agent" total = "1">
        <station id = "135a2040-4373-11ef-9945-3c7c3fbc6d25" name = "135a2040" last_seen_addr = "" last_seen_time = "0" os = "0" os_name = "unknown"/>
    </stations>
    <pages total = "1" current = "1" objects-per-page = "4294967295"/>
</drweb-es-api>
"""

SAMPLE_XML_2_OTHER = """<?xml version="1.0" encoding="UTF-8"?>
<drweb-es-api api_version="4.3.2" timestamp="1721134700" server="192.168.21.9" srv_version="13.00.1.202406060" status="true">
    <stations type = "scanning_server" total = "1">
        <station name = "1379440e" last_seen_addr = "" id = "1379440e-4373-11ef-b09a-3c7c3fbc6d25" last_seen_time = "0" os = "0" os_name = "unknown"/>
    </stations>
    <stations type = "virtual_agent" total = "1">
        <station id = "135a2040-4373-11ef-9945-3c7c3fbc6d25" name = "135a2040" last_seen_addr = "" last_seen_time = "0" os = "0" os_name = "unknown"/>
    </stations>    
    <stations type = "regular" total = "1">
        <station os = "0" os_name = "unknown" id = "1326782f-4373-11ef-96b1-3c7c3fbc6d25" name = "1326782f" last_seen_addr = "" last_seen_time = "0"/>
    </stations>
    <pages total = "1" current = "1" objects-per-page = "4294967295"/>
</drweb-es-api>
"""

SAMPLE_XML_DAMAGED = """<?xml version="1.0" encoding="UTF-8"?>
<drweb-es-api api_version="4.3.2" timestamp="1721134700" server="192.168.21.9" srv_version="13.00.1.202406060" status="true">
    <stations type = "regular" total = "1">
        <station id = "1326782f-4373-11ef-96b1-3c7c3fbc6d25" name = "1326782f" last_seen_addr = "" last_seen_time = "0" os = "0" os_name = "unknown"/>
    </stations>
    <stations type = "scanning_server" total = "1">
        <station id = "1379440e-4373-11ef-b09a-3c7c3fbc6d25" name = "1379440e" last_seen_addr = "" last_seen_time = "0" os = "0" os_name = "unknown"/>
    </stations>
    <stations type = "virtual_agent" total = "1">
        <station id = "135a2040-4373-11ef-9945-3c7c3fbc6d25" name = "135a2040" last_seen_addr = "" last_seen_time = "0" os = "0" os_name = "unknown"/>
    </stations>
    <pages total = "1" current = "1" objects-per-page = "4294967296"/>
</drweb-es-api>
"""

SUB_XML_2 = """
<drweb-es-api api_version="4.3.2" timestamp="1721134700" server="192.168.21.9" srv_version="13.00.1.202406060" status="true">
    <stations type = "regular" total = "1">
        <station id = "1326782f-4373-11ef-96b1-3c7c3fbc6d25" name = "1326782f" last_seen_addr = "" last_seen_time = "0" os = "0" os_name = "unknown"/>
    </stations>
    <stations type = "virtual_agent" total = "1">
        <station id = "135a2040-4373-11ef-9945-3c7c3fbc6d25" name = "135a2040" last_seen_addr = "" last_seen_time = "0" os = "0" os_name = "unknown"/>
    </stations>
</drweb-es-api>
"""


@pytest.mark.parametrize('xml_str1, xml_str2, xml_tag', [
    [SUB_XML_1,  SAMPLE_XML_1, 'country'],
    [SUB_XML_2, SAMPLE_XML_2, 'stations'],
    [SAMPLE_XML_2, SAMPLE_XML_2_OTHER, None]
], ids=['one', 'two', 'three'])
def test_compare_xml(xml_str1, xml_str2, xml_tag):
    assert my_compare_xml(xml_str1, xml_str2, xml_tag)


def test_compare_xml_2():
    assert my_compare_xml(SAMPLE_XML_2, SAMPLE_XML_2_OTHER)


@pytest.mark.parametrize('xml_str1, xml_str2, result', [
[SAMPLE_XML_1, SAMPLE_XML_1_OTHER, True],
[SAMPLE_XML_1, SAMPLE_XML_1_DAMAGED_1, False],
[SAMPLE_XML_1, SAMPLE_XML_1_DAMAGED_2, False],
[SAMPLE_XML_1, SAMPLE_XML_1_DAMAGED_3, False],
[SAMPLE_XML_1, SAMPLE_XML_1_DAMAGED_4, False],
[SAMPLE_XML_2, SAMPLE_XML_2_OTHER, True],
[SAMPLE_XML_2, SAMPLE_XML_DAMAGED, False],

], ids='1 2 3 4 5 6 7'.split())
def test_xml_converter_to_lofl(xml_str1, xml_str2, result):
    result1 = xml_converter_to_lofl(xml_str1)
    hash1 = hash(repr(result1))
    result2 = xml_converter_to_lofl(xml_str2)
    hash2 = hash(repr(result2))
    print("")
    print(f"result_1: {hash1}, {result1}")
    print(f"result_2: {hash2}, {result2}")
    assert (hash1 == hash2) == result
