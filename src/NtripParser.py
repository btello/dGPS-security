# A program to parse through the list of casters posted on
# ntrip-rtcm.org and gather statistics about Ntrip sources
# out in the wild.  It scans the list of casters, and downloads
# the source table from each one.  For each source table retrieved,
# the records corresponding to Ntrip sources are parsed and
# gathered for some simple statistical processing.
#
# Links to further casters/networks are not followed so the data 
# returned from this program likely only represents a small sample
# of the overall Ntrip source population.
#
# @author Brady Tello
import string;
import urllib;

# These casters didn't seem to work. We'll just ignore them.
badCasterList = ["132.239.152.74","167.131.0.205","190.12.71.75",
"193.2.110.246", "200.145.185.200", "203.159.29.16", "203.166.119.228",
"207.34.120.72", "211.79.140.230", "217.12.213.134", "62.25.98.134",
"74.223.26.163","81.255.128.233", "81.255.128.234", "89.97.35.19",
"igs-au.net", "ntrip.omnistar.net.au", "ntrip.rtklink.net",
"sydnet.lands.nsw.gov.au", "vrs.ngii.go.kr", "www.gpsnet.fr",
"www.vrs.dyndns.org"];

numBasicAuth = 0;
numDigestAuth = 0;
numFee = 0;
numNoFee = 0;

ignoredCasters = 0;

listOfDevices = {};

# Open a connection to the main caster and download the source table
mainCaster = urllib.urlopen("http://rtcm-ntrip.org");
for casterLine in mainCaster:
    casterSplitLine = string.split(casterLine,";");
    if casterSplitLine[0] != "CAS":
        continue;
    if casterSplitLine[1] in badCasterList:
        continue;
    if casterSplitLine[1] == "87.253.133.135" and casterSplitLine[2] == "80":
        continue;

    nextURL = "http://" + casterSplitLine[1] + ":" + casterSplitLine[2];
    print "Opening ", nextURL;
    f = urllib.urlopen(nextURL);

    for line in f:
        splitLine = string.split(line,";");
        if splitLine[0] == "CAS":
            ignoredCasters += 1;
        if splitLine[0] == "STR":
            if splitLine[13].upper().replace(" ","") not in listOfDevices:
                listOfDevices[splitLine[13].upper().replace(" ","")] = 1;
            else:
                listOfDevices[splitLine[13].upper().replace(" ","")] += 1;
            if splitLine[15] == "N" or splitLine[15] == "B":
                numBasicAuth += 1;
            elif splitLine[15] == "D":
                numDigestAuth += 1;
            if splitLine[16] == "Y":
                numFee += 1;
            elif splitLine[16] == "N":
                numNoFee += 1;
    f.close();
        
print "# of streams using basic authentication: ", numBasicAuth;
print "# of streams using digest authentication: ", numDigestAuth;
print "# of streams charging a fee: ", numFee;
print "# of streams charging no fee: ", numNoFee;
print "Devices: "

for k,v in sorted(listOfDevices.iteritems()):
    print k,v;

print "# of caster links that were not followed: ", ignoredCasters;
