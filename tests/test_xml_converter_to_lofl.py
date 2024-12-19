import pytest

from helper.work_xml import xml_converter_to_lofl, compare_xml

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

# SAMPLE_XML_1 с поменянными местами странами.
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

# SAMPLE_XML_1 немного изменённый
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

# SAMPLE_XML_1 немного изменённый
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

# SAMPLE_XML_1 немного изменённый
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

# SAMPLE_XML_1 немного изменённый
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

# Часть от SAMPLE_XML_1
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

# SAMPLE_XML_2 с поменянными местами элементами
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

# SAMPLE_XML_2 немного изменённый
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

# Часть от SAMPLE_XML_2
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

# Строка XML не отформатированная, в одну строку.
XML_STR = """<groups total="17"><group id="469b8c67-b874-11ef-9f46-3c7c3fbc6d25" name="469b8c67" child_groups="0" stations="0" type="0" /><group id="46a49010-b874-11ef-89f6-3c7c3fbc6d25" name="46a49010" child_groups="0" stations="0" type="0" /><group id="46ab6fb7-b874-11ef-9128-3c7c3fbc6d25" name="46ab6fb7" child_groups="2" stations="4" type="0" /><group id="068e436a-952e-49d9-9b7f-46e2761dfc6f" name="Active Directory" child_groups="3" stations="0" type="10" /><group id="c35f4732-b866-11ef-b82e-3c7c3fbc6d25" name="c35f4732" child_groups="0" stations="0" type="0" /><group id="c3656e57-b866-11ef-96c3-3c7c3fbc6d25" name="c3656e57" child_groups="0" stations="0" type="0" /><group id="c36c66e0-b866-11ef-bb0d-3c7c3fbc6d25" name="c36c66e0" child_groups="2" stations="4" type="0" /><group id="8c483456-0d15-4e41-b271-87197ac2adb6" name="Configured" child_groups="0" stations="0" type="10" /><group id="20e27d73-d21d-b211-a788-85419c46f0e6" name="Everyone" child_groups="0" stations="8" type="1" /><group id="aa6469d2-6621-46ce-8eed-fc35573c0b34" name="Neighbors" child_groups="6" stations="0" type="10" /><group id="f991915f-8a15-4cf7-817a-d81d156d2bbe" name="Operating system" child_groups="6" stations="0" type="10" /><group id="2abcd184-d8ba-4020-92fb-53148b61efaf" name="Policies" child_groups="0" stations="0" type="10" /><group id="640b34ee-2058-49d6-b24d-d7cb239cfa3d" name="Profiles" child_groups="0" stations="0" type="10" /><group id="54171821-08df-4146-860b-3f5e6eb4ef40" name="Proxies" child_groups="0" stations="0" type="13" /><group id="48afe720-953c-4075-856c-361f3ff06b6d" name="Status" child_groups="7" stations="8" type="10" /><group id="159e383d-f853-4bc5-9e18-c40144542aca" name="Transport" child_groups="3" stations="0" type="10" /><group id="411dac63-2a3e-4ce8-af4f-1fbeb94242ef" name="Ungrouped" child_groups="0" stations="0" type="10" /></groups>"""


@pytest.mark.parametrize('xml_str1, xml_str2, xml_tag', [
    [SUB_XML_1,  SAMPLE_XML_1, 'country'],
    [SUB_XML_2, SAMPLE_XML_2, 'stations'],
    [SAMPLE_XML_2, SAMPLE_XML_2_OTHER, None]
], ids=['one', 'two', 'three'])
def test_compare_xml(xml_str1, xml_str2, xml_tag):
    assert compare_xml(xml_str1, xml_str2, xml_tag)


def test_compare_xml_2():
    assert compare_xml(SAMPLE_XML_2, SAMPLE_XML_2_OTHER)


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
