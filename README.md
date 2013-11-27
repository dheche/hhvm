# HHVM RPM Repository for CentOS 6.x
## Notes
* version: 2.3.0-dev
* FastCGI is disabled
* Arch: x86_64

## How to Install
* URL Repository: TBD

    ```
    [dheche@fountain ~]$ sudo yum-config-manager --enable hhvm
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
* Build all package, rpmbuild -ba SPECS/<package.spec>

### Build Using Source RPM
* URL Repository: TBD
* yumdownloader --source hhvm
* rpmbuild --rebuild package.src.rpm

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

