from cisco_config_parser import ConfigParser

file = "/Users/ahmad/running_config.txt"

parser = ConfigParser(content=file, method="file")

obj = parser.ios_get_switchport(mode="trunk")

for i in obj:
    print(i.get_trunk)