%define hhvm_dir %{_var}/hhvm
%define hhvm_user hhvm

Name:           hhvm
Version:        2.2.0
Release:        1%{?dist}
Summary:        HipHop VM (HHVM) is a virtual machine for executing programs written in PHP

Group:          Development/Compiler
License:        PHP/Apache
URL:            http://hhvm.com
Source0:        https://github.com/facebook/hhvm/archive/HHVM-%{version}.tar.gz
Source1:	hhvm.initscript
Source2:	hhvm.hdf
Source3:	hhvm.sysconfig
Source4:	hhvm.bash_profile

BuildRequires:  gcc >= 4.6.3, cmake >= 2.8.5, libevent-devel >= 1.4 
BuildRequires:	libcurl-devel >= 7.29 
BuildRequires:	glog-devel >= 0.3.3, jemalloc-devel >= 3.0, tbb-devel >= 4.0
BuildRequires:	libmcrypt-devel >= 2.5.8, libdwarf-devel >= 20130729
BuildRequires:	mysql-devel libxml2-devel libicu-devel
BuildRequires:	oniguruma-devel readline-devel libc-client-devel pam-devel
BuildRequires:	libcap-devel libedit-devel pcre-devel gd-devel sqlite-devel
#BuildRequires:	inotify-tools-devel 
BuildRequires:	boost-devel >= 1.48, libmemcached-devel >= 0.39 
#BuildRequires:	boost-devel >= 1.48
Requires:       glog >= 0.3.3, jemalloc >= 3.0, tbb >= 4.0
Requires:		libmcrypt >= 2.5.8, libdwarf >= 20130729
Requires:		boost >= 1.48, libmemcached >= 0.39

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
%setup -q -n hhvm


%build
export HPHP_HOME=`pwd`
export CPLUS_INCLUDE_PATH=/usr/include/libdwarf
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr .
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Install initscript, sysconfig and hhvm configuration
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initddir}/%{name}
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/hhvm/%{name}
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/profile.d/hhvm.sh

# Create default directory
%{__mkdir} -p %{buildroot}%{_var}/run/%{name}
%{__mkdir} -p %{buildroot}%{_var}/log/%{name}

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
%dir %{_var}/run/%{name}
%dir %{_var}/log/%{name}

%defattr(-,root,root,-)
%dir %{_sysconfdir}/hhvm/%{name}
%config(noreplace) %{_sysconfdir}/hhvm/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/profile.d/hhvm.sh
%{_initddir}/%{name}
%{_bindir}/hhvm
%{_bindir}/hphpize

%doc CONTRIBUTING.md LICENSE.PHP LICENSE.ZEND README.md hphp/NEWS 


%changelog
* Sat Nov 23 2013 Teguh Dwicaksana <dheche@fedoraproject.org> - 2.2.0-1
- Initial built for el6
