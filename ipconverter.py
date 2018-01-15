#!/usr/bin/python
import os
import sys
import re
import struct
import datetime
from socket import inet_aton

#define list where to add ip addresses.
listIP=[]
#identify a unique per day file. not great but no waste of time
today=datetime.datetime.today()
finalFile=str(today.date())+"-ipfile-sanitised.txt"

#Validation for correct IP evaluation
def validateIP(ip):
    ValidIpAddressRegex = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
    if ValidIpAddressRegex.search(ip):
        return True
    else:
        print "[ERROR] - During the processing we found that the current %s, was in incorrect format. Please review." % (ip)
        return False

#If , or space or - in line remove and set IP on newline
def evaluateBadStrings(line):
    if "-" or ","  in line:
        stripper=re.split(r"-|,| ",line)
        for elem in stripper:
            return stripper
    else:
        return line

#Sort ip address from 1.1.1.1 to 255.255.255.255
def sort_ip_list(ip_list):
    return sorted(ip_list, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])

#Main Function to read from file and print
if __name__ == "__main__":
    # give user option to decide what separator to use to write the list:
    try :
        userInput = raw_input("what is the separator you would like to add to list? (Eg: comma \",\" newline \"\\n\": ")
        if userInput.lower() == "coma":
            userInput = ","
            print "Your selection is: ", userInput.lower()
        elif userInput.lower() == "newline":
            userInput = "\n"
            print "Your selection is: ", userInput.lower()
        else:
            userInput = userInput.lower()
            print "Your selection is: ", userInput.lower()

        # If error will be user forgot to specify arg 1 as file
        try :
            if os.path.isfile(sys.argv[1]):
                readFile=open(sys.argv[1],"r").readlines()
                for elem in readFile:
                    # Remove blank line
                    if elem.strip() :
                        # Evaluate - , " " in line passed
                        for ip in evaluateBadStrings(elem.rstrip()):
                            # If the IP matches regex
                            if validateIP(ip):
                                # Put in a list
                                listIP.append(ip)
            else:
                print "Provide a file with a list of ip in it. Eg: python %s ipfile.txt" % sys.argv[0]

        except Exception, e:
            print "Provide a file with a list of ip in it. Eg: python %s ipfile.txt" % sys.argv[0]

        # Always remove if same file. We don't care.
        if os.path.isfile(finalFile):
            os.remove(finalFile)
        # Write list of IPs
        writeFinal=open(finalFile,"a")
        for ipsort in sort_ip_list(set(listIP)):
            writeFinal.write(ipsort+userInput)
        writeFinal.close()
        #Print some fancy stats
        print "The list has %d number of ip addresses." % len(listIP)
        print "The list has been cleared from duplicates and the current amount is: %d" % len(sort_ip_list(set(listIP)))
        print "The sanitised list of ip address has been written to:", finalFile
    #IF we press CTRL+C at any time we exit, byebye.
    except KeyboardInterrupt,e:
        print "\nYou pressed CTRL+C, exiting."
