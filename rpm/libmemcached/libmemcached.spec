# Regression tests take a long time, you can skip 'em with this
%{!?runselftest: %{expand: %%global runselftest 1}}
%global with_sasl        1

Name:      libmemcached
Summary:   Client library and command line tools for memcached server
Version:   1.0.16
Release:   1%{?dist}
License:   BSD
Group:     System Environment/Libraries
URL:       http://libmemcached.org/
# Original sources:
#   http://launchpad.net/libmemcached/1.0/%{version}/+download/libmemcached-%{version}.tar.gz
# The source tarball must be repackaged to remove the Hsieh hash
# code, since the license is non-free.  When upgrading, download the new
# source tarball, and run "./strip-hsieh.sh <version>" to produce the
# "-exhsieh" tarball.
Source0:   libmemcached-%{version}-exhsieh.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{with_sasl}
BuildRequires: cyrus-sasl-devel
%endif
BuildRequires: flex
BuildRequires: bison
BuildRequires: python-sphinx
BuildRequires: memcached
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
BuildRequires: systemtap-sdt-devel
%endif
BuildRequires: libevent-devel


%description
libmemcached is a C/C++ client library and tools for the memcached server
(http://memcached.org/). It has been designed to be light on memory
usage, and provide full access to server side methods.

It also implements several command line tools:

memaslap    Load testing and benchmarking a server
memcapable  Checking a Memcached server capibilities and compatibility
memcat      Copy the value of a key to standard output
memcp       Copy data to a server
memdump     Dumping your server
memerror    Translate an error code to a string
memexist    Check for the existance of a key
memflush    Flush the contents of your servers
memparse    Parse an option string
memping     Test to see if a server is available.
memrm       Remove a key(s) from the server
memslap     Generate testing loads on a memcached cluster
memstat     Dump the stats of your servers to standard output
memtouch    Touches a key


%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
%if %{with_sasl}
Requires: cyrus-sasl-devel%{?_isa}
%endif

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.


%prep
%setup -q

mkdir examples
cp -p tests/*.{cc,h} examples/


%build
# option --with-memcached=false to disable server binary check (as we don't run test)
%configure \
%if %{runselftest}
   --with-memcached=%{_bindir}/memcached \
%else
   --with-memcached=false \
%endif
%if %{with_sasl}
   --enable-sasl \
%else
   --disable-sasl \
%endif
   --enable-libmemcachedprotocol \
   --enable-memaslap \
   --enable-dtrace \
   --disable-static

%if 0%{?fedora} < 14 && 0%{?rhel} < 7
# for warning: unknown option after '#pragma GCC diagnostic' kind
sed -e 's/-Werror//' -i Makefile
%endif

make %{_smp_mflags}


%install
rm -rf %{buildroot}
make install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""

# Hack: when sphinx-build too old (fedora < 14 and rhel < 7)
# install upstream provided man pages
if [ ! -d %{buildroot}%{_mandir}/man1 ]; then
   install -d %{buildroot}%{_mandir}/man1
   install -p -m 644 man/*1 %{buildroot}%{_mandir}/man1
   install -d %{buildroot}%{_mandir}/man3
   install -p -m 644 man/*3 %{buildroot}%{_mandir}/man3
fi


%check
%if %{runselftest}
make test 2>&1 | tee rpmtests.log
# Ignore test result for memaslap (XFAIL but PASS)
# https://bugs.launchpad.net/libmemcached/+bug/1115357
if grep "XPASS: clients/memaslap" rpmtests.log && grep "1 of 21" rpmtests.log
then
  exit 0
else
  exit 1
fi
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig
 

%files
%defattr (-,root,root,-) 
%doc AUTHORS COPYING README THANKS TODO ChangeLog
%{_bindir}/mem*
%exclude %{_libdir}/lib*.la
%{_libdir}/libhashkit.so.2*
%{_libdir}/libmemcached.so.11*
%{_libdir}/libmemcachedprotocol.so.0*
%{_libdir}/libmemcachedutil.so.2*
%{_mandir}/man1/mem*


%files devel
%defattr (-,root,root,-) 
%doc examples
%{_includedir}/libmemcached
%{_includedir}/libmemcached-1.0
%{_includedir}/libhashkit
%{_includedir}/libhashkit-1.0
%{_includedir}/libmemcachedprotocol-0.0
%{_includedir}/libmemcachedutil-1.0
%{_libdir}/libhashkit.so
%{_libdir}/libmemcached.so
%{_libdir}/libmemcachedprotocol.so
%{_libdir}/libmemcachedutil.so
%{_libdir}/pkgconfig/libmemcached.pc
%{_datadir}/aclocal/ax_libmemcached.m4
%{_mandir}/man3/libmemcached*
%{_mandir}/man3/libhashkit*
%{_mandir}/man3/memcached*
%{_mandir}/man3/hashkit*


%changelog
* Mon Feb  4 2013 Remi Collet <remi@fedoraproject.org> - 1.0.16-1
- update to 1.0.16
- ignore test result for memaslap (XFAIL but PASS)
  https://bugs.launchpad.net/libmemcached/+bug/1115357

* Sat Dec 29 2012 Remi Collet <remi@fedoraproject.org> - 1.0.15-1
- update to 1.0.15
- libmemcachedprotocol is back
- add memaslap command line tool
- report various issues to upstream
  https://bugs.launchpad.net/libmemcached/+bug/1094413 (libevent)
  https://bugs.launchpad.net/libmemcached/+bug/1094414 (c99 MODE)

* Sat Nov 17 2012 Remi Collet <remi@fedoraproject.org> - 1.0.14-1
- update to 1.0.14
- libmemcachedprotocol removed
- sasl support is back
- run test during build
- report various issues to upstream
  https://bugs.launchpad.net/libmemcached/+bug/1079994 (bigendian)
  https://bugs.launchpad.net/libmemcached/+bug/1079995 (config.h)
  https://bugs.launchpad.net/libmemcached/+bug/1079996 (dtrace)
  https://bugs.launchpad.net/libmemcached/+bug/1079997 (-ldl)
  https://bugs.launchpad.net/libmemcached/+bug/1080000 (touch)

* Sat Oct 20 2012 Remi Collet <remi@fedoraproject.org> - 1.0.13-1
- update to 1.0.13

* Fri Oct 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.12-2
- temporary hack: fix LIBMEMCACHED_VERSION_HEX value

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.0.12-1
- update to 1.0.12
- add aclocal/ax_lib_libmemcached.m4
- abi-compliance-checker verdict : Compatible
- uggly hack for man pages

* Tue Sep 25 2012 Karsten Hopp <karsten@redhat.com> 1.0.11-2
- fix defined but not used variable error on bigendian machines

* Sat Sep 22 2012 Remi Collet <remi@fedoraproject.org> - 1.0.11-1
- update to 1.0.11, soname bump to libmemcached.so.11
- drop broken SASL support
- don't generate parser (bison 2.6 not supported)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 27 2012 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- update to 1.0.8

* Sun Apr 22 2012 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- update to 1.0.7
- regenerate parser using flex/bison (#816766)

* Sun Apr 22 2012 Remi Collet <remi@fedoraproject.org> - 1.0.6-2
- workaround for SASL detection

* Sat Apr 21 2012 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- update to 1.0.6
- soname bump to libmemcached.so.10 and libhashkit.so.2

* Sat Mar 03 2012 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4
- soname bump to libmemcached.so.9
- update description

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 27 2011 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Sun Oct 16 2011 Remi Collet <remi@fedoraproject.org> - 0.53-1
- update to 0.53

* Sat Sep 17 2011 Remi Collet <remi@fedoraproject.org> - 0.52-1
- update to 0.52

* Sun Jul 31 2011 Remi Collet <remi@fedoraproject.org> - 0.51-1
- update to 0.51 (soname bump libmemcached.so.8)

* Thu Jun 02 2011 Remi Collet <Fedora@famillecollet.com> - 0.49-1
- update to 0.49
- add build option : --with tests

* Mon Feb 28 2011 Remi Collet <Fedora@famillecollet.com> - 0.47-1
- update to 0.47
- remove patch merged upstream

* Sun Feb 20 2011 Remi Collet <Fedora@famillecollet.com> - 0.46-2
- patch Makefile.in instead of include.am (to avoid autoconf)
- donc requires pkgconfig with arch

* Fri Feb 18 2011 Remi Collet <Fedora@famillecollet.com> - 0.46-1
- update to 0.46

* Sat Feb 12 2011 Remi Collet <Fedora@famillecollet.com> - 0.44-6
- arch specific requires

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Joe Orton <jorton@redhat.com> - 0.44-4
- repackage source tarball to remove non-free Hsieh hash code

* Sat Oct 02 2010 Remi Collet <Fedora@famillecollet.com> - 0.44-3
- improves SASL patch

* Sat Oct 02 2010 Remi Collet <Fedora@famillecollet.com> - 0.44-2
- enable SASL support

* Fri Oct 01 2010 Remi Collet <Fedora@famillecollet.com> - 0.44-1
- update to 0.44
- add soname version in %%file to detect change

* Fri Jul 30 2010 Remi Collet <Fedora@famillecollet.com> - 0.43-1
- update to 0.43

* Wed Jul 07 2010 Remi Collet <Fedora@famillecollet.com> - 0.42-1
- update to 0.42

* Tue May 04 2010 Remi Collet <Fedora@famillecollet.com> - 0.40-1
- update to 0.40 (new soname for libmemcached.so.5)
- new URI (site + source)

* Sat Mar 13 2010 Remi Collet <Fedora@famillecollet.com> - 0.38-1
- update to 0.38

* Sat Feb 06 2010 Remi Collet <Fedora@famillecollet.com> - 0.37-1
- update to 0.37 (soname bump)
- new libhashkit (should be a separated project in the futur)

* Sun Sep 13 2009 Remi Collet <Fedora@famillecollet.com> - 0.31-1
- update to 0.31

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Remi Collet <Fedora@famillecollet.com> - 0.30-1
- update to 0.30

* Tue May 19 2009 Remi Collet <Fedora@famillecollet.com> - 0.29-1
- update to 0.29

* Fri May 01 2009 Remi Collet <Fedora@famillecollet.com> - 0.28-2
- add upstream patch to disable nonfree hsieh hash method

* Sat Apr 25 2009 Remi Collet <Fedora@famillecollet.com> - 0.28-1
- Initial RPM from Brian Aker spec
- create -devel subpackage
- add %%post %%postun %%check section

