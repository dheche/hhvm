# HHVM RPM Repository for CentOS 6.x
## Notes
* version: 2.3.0-dev
* FastCGI is disabled
* Support memcache session 
* Arch: x86_64

## How to Install
* Install epel and hhvm repository configuration

    ```
    [dheche@fountain ~]$ sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    [dheche@fountain ~]$ sudo rpm -Uvh http://dheche.fedorapeople.org/hhvm/el6/RPMS/x86_64/hhvm-release-6-1.noarch.rpm
    ```

* Install hhvm

    ```
    [dheche@fountain ~]$ sudo yum install hhvm
    ```

## How to Build
### Build Using Files from git
* yum install rpmdevtools
* rpmdev-setuptree
* git clone https://github.com/dheche/hhvm.git
* Copy all spec files to rpmbuild/SPECS
* Copy remaining files to rpmbuild/SOURCES
* Download original source (tarball) for each package to rpmbuild/SOURCES (take alook at spec file, where you can find it)
* Build all package, rpmbuild -ba SPECS/*package_name.spec*

### Build Using Source RPM
* yum install yum-utils
* yumdownloader --source hhvm
* rpmbuild --rebuild hhvm-2.3.0-0.2.el6.src.rpm

## How to Create Local Repository
* yum install createrepo
* mkdir -p hhvm-repo/{RPMS,SRPMS}
* copy all rpm to hhvm-repo/RPMS
* copy all src.rpm to hhvm-repo/SRPMS
* cd hhvm-repo/RPMS
* createrepo .
* cd ../hhvm-repo/SRPMS
* createrepo .
* create repo configuration

