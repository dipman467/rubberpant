## RuberPant


RubberPant is an interactive data explorer for open elasticsearch instance. 
It is capable of searching a single IP, IP Range, CIDR Notation of /24, File input or parsing Shodan queries. It can donwnload a range of data just for viewing

In its simplicity, you can use the tool to check if any of your elasticsearch infrastructure is exposed to the internet.

Install the dependencies.

```sh
$ git clone https://github.com/dipman467/rubberpant.git
$ cd rubberpant
$ pip install -r requirements.txt
```

Then after installation, you can start exploring;

```sh
$ python rubberpant.py --help

Usage: rubberpant.py [-h] [-c] [-ip IP] [-p PORT] [-n CIDR] [-f FILE] [-r RANGE] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -c, --check           Only check if your IP is exposed or not
  -ip IP, --ip IP       Work on a single IP Address
  -p PORT, --port PORT  port to check [default:9200]
  -n CIDR, --cidr CIDR  Work on a CIDR Notation of /24
  -f FILE, --file FILE  Work on a list of IP address
  -r RANGE, --range RANGE  Work on an IP range
  -v, --verbose         Read output to terminal
```