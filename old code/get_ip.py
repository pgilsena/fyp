from geoip import geolite2

match = geolite2.lookup('216.58.211.162')

print match is not None
print match.country
print match.continent
