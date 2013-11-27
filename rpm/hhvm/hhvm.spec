%define hhvm_dir %{_var}/hhvm
%define hhvm_user hhvm
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           hhvm
Version:        2.3.0
Release:        0.1%{?dist}
Summary:        HipHop VM (HHVM) is a virtual machine for executing programs written in PHP

Group:          Development/Compiler
License:        PHP/Zend
URL:            http://hhvm.com
Source0:        https://github.com/facebook/hhvm/archive/HHVM-%{version}.tar.gz
Source1:	hhvm.initscript
Source2:	hhvm.hdf
Source3:	hhvm.sysconfig
Patch0:		hhvm-disable_fastcgi.patch
BuildRequires:  gcc >= 4.7.2, cmake >= 2.8.7, libevent-devel >= 1.4 
BuildRequires:	libcurl-devel >= 7.29 
BuildRequires:	glog-devel >= 0.3.3, jemalloc-devel >= 3.0, tbb-devel >= 4.0
BuildRequires:	libmcrypt-devel >= 2.5.8, libdwarf-devel >= 20130729
BuildRequires:	mysql-devel libxml2-devel libicu-devel
BuildRequires:	oniguruma-devel readline-devel libc-client-devel pam-devel
BuildRequires:	libcap-devel libedit-devel pcre-devel gd-devel sqlite-devel
BuildRequires:	inotify-tools-devel 
BuildRequires:	boost-devel >= 1.48, libmemcached-devel >= 0.39 
Requires:       glog >= 0.3.3, jemalloc >= 3.0, tbb >= 4.0
Requires:	libmcrypt >= 2.5.8, libdwarf >= 20130729
Requires:	boost >= 1.48, libmemcached >= 0.39

%description
HipHop VM (HHVM) is a new open-source virtual machine designed for executing 
programs written in PHP. 
HHVM uses a just-in-time compilation approach to achieve superior performance 
while maintaining the flexibility that PHP developers are accustomed to. 
HipHop VM (and before it HPHPc) has realized > 5x increase in throughput for 
Facebook compared with Zend PHP 5.2.

HipHop is most commonly run as a standalone server, replacing both Apache and 
modphp.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
export HPHP_HOME=`pwd`
export CPLUS_INCLUDE_PATH=/usr/include/libdwarf
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr \
	-DLIBINOTIFY_LIBRARY=/usr/lib64/libinotifytools.so.0 .
make %{?_smp_mflags}


%install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
%{__install} -p -D -m 0755 hphp/hhvm/hhvm %{buildroot}%{_bindir}/hhvm
%{__install} -p -D -m 0755 hphp/tools/hphpize/hphpize %{buildroot}%{_bindir}/hphpize


# Install initscript, sysconfig and hhvm configuration
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initddir}/%{name}
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/hhvm/hhvm.hdf
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Create default directory
%{__mkdir} -p %{buildroot}%{_var}/run/%{name}
%{__mkdir} -p %{buildroot}%{_var}/log/%{name}
%{__mkdir} -p %{buildroot}%{_var}/hhvm

# Cleanup
%{__rm} -f %{buildroot}%{_includedir}/zip.h
%{__rm} -f %{buildroot}%{_includedir}/zipconf.h
%{__rm} -f %{buildroot}/usr/lib/libzip.a
%{__rm} -f %{buildroot}/usr/lib/libzip.so


%clean
rm -rf $RPM_BUILD_ROOT


%pre
%{_sbindir}/useradd -d %{hhvm_dir} -m -c "HHVM" -r %{hhvm_user} 2>/dev/null
exit 0


%post
if [ $1 == 1 ]; then
    /sbin/chkconfig --add %{name}
fi


%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi


%files
%defattr(-,hhvm,hhvm,-)
%dir %{_var}/hhvm
%dir %{_var}/run/%{name}
%dir %{_var}/log/%{name}

%defattr(-,root,root,-)
%dir %{_sysconfdir}/hhvm
%config(noreplace) %{_sysconfdir}/hhvm/hhvm.hdf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initddir}/%{name}
%{_bindir}/hhvm
%{_bindir}/hphpize

%doc CONTRIBUTING.md LICENSE.PHP LICENSE.ZEND README.md hphp/NEWS 


%changelog
* Tue Nov 26 2013 Teguh Dwicaksana <dheche@fedoraproject.org> - 2.3.0-0.1
- Initial built for el6
