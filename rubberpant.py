import requests
import json
import sys
from progress.bar import Bar
import os, platform

def clear_screen(os_env):
    if 'Windows' in os_env:
        os.system('cls')
    else:
        os.system('clear')

def usage():
    print("Usage: {} [-ip IP_Address [-p port[default:9200]] | --shodan -t threads]".format(sys.argv[0]))


def _start():
    banner = '''

 ______      _     _              ______           _   
| ___ \    | |   | |             | ___ \         | |  
| |_/ _   _| |__ | |__   ___ _ __| |_/ __ _ _ __ | |_ 
|    | | | | '_ \| '_ \ / _ | '__|  __/ _` | '_ \| __|
| |\ | |_| | |_) | |_) |  __| |  | | | (_| | | | | |_ 
\_| \_\__,_|_.__/|_.__/ \___|_|  \_|  \__,_|_| |_|\__|
                                                      
                                                      
                                    coded by: @mztique
'''
    print(banner)
    try:
        if "-ip" in sys.argv:
           ip = sys.argv.index("-ip")
           ip_address = sys.argv[ip+1]

        if "-p" in sys.argv:
            p = sys.argv.index("-p")
            port = sys.argv[p+1]
        else:
            port = 9200

        if "--shodan" in sys.argv:
            print("Shodan search coming soon")
            exit(0)

        if "-t" in sys.argv:
            print("Threading coming soon")
            sys.exit(0)

        host = ip_address+":"+str(port)
        
        index_cmd = "/_cat/indices/?v&pretty"
        indices = requests.get("http://"+host+index_cmd)
        print(indices.text)

        if "index" in indices.text:
            index = input("What index do you wish to explore? ")
            explore_index(host,index)
        else:
            print("Sorry! Index not found. Ensure it's an Elasticsearch cluster/node")
            exit(0)
    except Exception as ex:
        print("Exception caught: {}".format(ex))
        usage()

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
        
        print(filename)
        f = open(filename, 'a+')
        bar = Bar('Downloading', max=len(hits))
        for i in hits:
            source = dict(i)
            _source = source["_source"]
            f.writelines(json.dumps(_source, indent=4))
            
            bar.next()
        bar.finish()
    else:
        print("Nothing found, see below\n{}".format(data))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
    else:
        _start()
