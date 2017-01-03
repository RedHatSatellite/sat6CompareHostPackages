# sat6CompareHostPackages
Given two hosts, show the package differences between them.


## Usage

~~~
↪ ./sat6CompareHostPackages.py -l admin \
       -s satellite.example.com \
       --source-host auth01.example.com \
       --target-host auth02.example.com
admin's password:
There are 9 packages that differ from auth01.example.com -> auth02.example.com
	cyrus-sasl-plain-2.1.26-20.el7_2.x86_64
	openscap-1.2.10-2.el7.x86_64
	openscap-scanner-1.2.10-2.el7.x86_64
	openssh-6.6.1p1-23.el7_2.x86_64
	openssh-clients-6.6.1p1-23.el7_2.x86_64
	openssh-server-6.6.1p1-23.el7_2.x86_64
	subscription-manager-migration-1.17.15-1.el7.x86_64
	subscription-manager-migration-data-2.0.31-1.el7.noarch
	yajl-2.0.4-4.el7.x86_64

There are 3 packages that differ from auth02.example.com -> auth01.example.com
	openssh-6.6.1p1-31.el7.x86_64
	openssh-clients-6.6.1p1-31.el7.x86_64
	openssh-server-6.6.1p1-31.el7.x86_64
~~~
