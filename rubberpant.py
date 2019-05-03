import requests
import json
import sys
from progress.bar import Bar
import os, platform
from argparse import ArgumentParser
from colorama import Fore, Back, Style
import threading

verbose = False
check = False


os_env = platform.platform()

def clear_screen(os_env):
    if 'Windows' in os_env:
        os.system('cls')
    else:
        os.system('clear')



def _start():
    banner = '''

 ______      _     _              ______           _   
| ___ \    | |   | |             | ___ \         | |  
| |_/ _   _| |__ | |__   ___ _ __| |_/ __ _ _ __ | |_ 
|    | | | | '_ \| '_ \ / _ | '__|  __/ _` | '_ \| __|
| |\ | |_| | |_) | |_) |  __| |  | | | (_| | | | | |_ 
\_| \_\__,_|_.__/|_.__/ \___|_|  \_|  \__,_|_| |_|\__|
                                                      
               '''+Fore.RED+'''Version: 1.0
               Author: @mztique et. @eeyitemi
               Github: @dipman467
                    
'''+Style.RESET_ALL
    print(banner)
    
def get_args():
    parser = ArgumentParser()
    parser.add_argument('-c','--check', help='Only check if your IP is exposed or not', required=False, action='store_true')
    parser.add_argument('-ip','--ip', help='Work on a single IP Address', required=False)
    parser.add_argument('-p','--port', help='port to check [default:9200]', required=False)
    parser.add_argument('-n','--cidr', help='Work on a CIDR Notation of /24', required=False)
    parser.add_argument('-f','--file', help='Work on a list of IP address', required=False)
    parser.add_argument('-r','--range', help='Work on an IP range',required=False)
    #parser.add_argument('-t','--thread', help='Number of threads to use [only use with -c or --check]',required=False)
    parser.add_argument('-v','--verbose', help='Read output to terminal',required=False, action='store_true')
    return parser.parse_args()

  
def ip_range(ip,port):
    start, stop = ip.split("-")

    _start = start.split(".")
    _stop = stop.split(".")
    
    #Check same subnet
    if _start[2] == _stop[2]:
        start_host_index = int(_start[3])
        stop_host_index = int(_stop[3])
        counter = start_host_index
        while stop_host_index != counter-1:
            ip_address = _start[0]+"."+_start[1]+"."+_start[2]+"."+str(counter)
            host = ip_address+":"+port
            print(Fore.GREEN+"Checking ===>  {}".format(host)+Style.RESET_ALL)
            elastic_rubber(host)
            counter = counter + 1
    
def cidr(ip,port):
    #TODO calculate cidr notation
    ip,cidr = ip.split("/")
    if cidr == "24":
        start = ip.split(".")
        for i in range(255):
            ip_address = start[0]+"."+start[1]+"."+start[2]+"."+str(i)
            host = ip_address+":"+port
            print(Fore.GREEN+"Checking ===>  {}".format(host)+Style.RESET_ALL)
            elastic_rubber(host) 
    else:
        print("Sorry only /24 notation supported")
        
            
def ipfile(infile):
    try:
        with open(infile,'r+') as file:
            for ip in file.readlines():
                host = ip.strip("\n")+":"+port
                print(Fore.GREEN+"Checking ===>  {}".format(host)+Style.RESET_ALL)
                elastic_rubber(host)
    except Exception as e:
        print("Error occured in ".format(e))
        
def elastic_rubber(host):
    try:
        #Check host
        elastic = requests.get("http://"+host)
        if elastic.status_code == 200:
            if "cluster_name" in elastic.text:
                if check:
                    print(Fore.GREEN+host+"\tEXPOSED"+Style.RESET_ALL)
                    return 
                elastic_host = json.loads(elastic.text)
                
                print(json.dumps(elastic_host, indent=4))
                
                
                index_cmd = "/_cat/indices/?v&pretty"
                indices = requests.get("http://"+host+index_cmd)
                print(indices.text)
        
                if "index" in indices.text:
                    index = input("What index do you wish to explore? ")
                    explore_index(host,index)
                else:
                    print("Sorry! Index not found. Ensure the name is written correctly")
                
            else:
                if check:
                    print(Fore.RED+host+"\tNOT EXPOSED"+Style.RESET_ALL)
                else:
                    print("{}: Cluster name not found. Ensure it's an Elasticsearch instance".format(host))
    except Exception as ex:
        print("Error Occured! {}, please check and try again".format(ex))

def explore_index(host,index):
    
    _size = input("How many data set to explore? ")
    _from = input("Where to start downloading?[default:0] ")
    if not _from:
        _from = '0'
    print()
    explore_cmd = "/_search/?q=*&size="+_size+"&from="+_from

    re = requests.get("http://"+host+"/"+index+explore_cmd)
    data = json.loads(re.text)
    if int(data["hits"]["total"]) > 0:
        hits = data["hits"]["hits"]
        #_host = host.replace(".","_")
        _host = host.replace(":","-")
        filename = _host+'_'+index+'.txt'
        
        f = open(filename, 'a+')
        bar = Bar('Downloading', max=len(hits))
        for i in hits:
            source = dict(i)
            _source = source["_source"]
            f.writelines(json.dumps(_source, indent=4))
            if verbose:
                #Color the lines if possible
                print(json.dumps(_source, indent=4))
            else:
                bar.next()
        if not verbose: bar.finish()
        print("Results saved to: {}".format(filename))
        
    else:
        print("Nothing found, see below\n{}".format(data))

def runThreads(threads):
    thread_list = []
    
    for i in threads:
        tr = threading.Thread(target=self.generate_listings, args=(url,page_no))                            
        thread_list.append(tr)
        thread_list[page_index].start()
        page_no+= 120
        page_index+= 1
    
    for t in thread_list:
        t.join()              


if __name__ == '__main__':
    clear_screen(os_env)
    _start()
    args = get_args()
    port = args.port if args.port else "9200"
    #Assign all args
    check = args.check
    ip = args.ip
    cidr = args.cidr
    infile = args.file
    verbose = args.verbose
    
    if check:
        check = True
    if verbose:
        verbose = True
    if infile:
        ipfile(infile)
    elif ip:
        host = str(ip) + ":" + str(port)
        elastic_rubber(host)
    elif cidr:
        cidr(cidr,port)
    elif iprange:
        ip_range(ip,port)
    else:
        print("You need to specify one method of IP addressing. Type -h or --help for usage help")
