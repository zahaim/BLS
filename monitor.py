#!/usr/bin/python

# jan.szczyra@gmail.com
# 2016-03-31
# simple python to:
# - check website availability
# - find a string on this website
# - measure and log stats
# as requested by BLS people

# importing what is necessary
import sys, getopt, requests, re, time, datetime

# defining main function
def main(argv):
    # default values set
    inputfile = 'sites.csv'
    outputfile = 'monitor.log'
    sleepy = 1
    try:
        opts, args = getopt.getopt(argv,"hi:o:t:",["ifile=","ofile=","sleep="])
    except getopt.GetoptError:
        print 'monitor.py -i <inputfile> -o <outputfile> -t <time between checks in sec>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'monitor.py -i <inputfile> -o <outputfile> -t <time between checks in sec>'
            print "FYI: By default program uses the following defaults -i %s -o %s -t %s" % (inputfile, outputfile, sleepy)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-t", "--sleep"):
            sleepy = float(arg)
            
    # setting a value for infinite loop
    daemon = 'true'

    # and the loop in person!
    while daemon == 'true' :
        # reading from conf file
        with open(inputfile) as f:
            for line in f:
                # splitting comma separated values
                temp_split = line.split(",")
                url, pattern_temp = temp_split
                
                # method to check http
                try:
                    r = requests.get(url, timeout=0.2)
                    if r.status_code is 200:
                        code = "OK (%s)" % r.status_code
                    else:
                        code = "KO (%s)" % r.status_code
                    # checking if pattern can be found on the website
                    content = r.text
                    pattern = pattern_temp.rstrip()
                    if re.search(pattern, content) is None:
                        patt = "pattern %s not found!" % pattern
                    else:
                        patt = "pattern %s found" % pattern
                    secs = r.elapsed.total_seconds()
                except requests.exceptions.Timeout:
                    code = "KO Timeout!"
                    patt = ''
                    secs = ''
                except requests.exceptions.MissingSchema:
                    code = "Invalid URL!"
                    patt = ''
                    secs = ''
                # we will be appending to logfile
                l = open(outputfile, 'a')
                time_is = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
                # putting it all together
                check_result = "%s \t %s \t %s \t %s \t %s \n" % (time_is,url,code,patt,secs)
                # writing to log
                l.write(check_result)
        
        # just to be nice - closing the file and waiting for -t <seconds>
        f.closed
        time.sleep(sleepy)
        
# main function
if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print 'Thanks and Bye!'
        sys.exit(0)