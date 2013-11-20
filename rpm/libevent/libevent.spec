Name:           libevent
Version:        1.4.13
Release:        4%{?dist}
Summary:        Abstract asynchronous event notification library

Group:          System Environment/Libraries
License:        BSD
URL:            http://monkey.org/~provos/libevent/
Source0:        http://monkey.org/~provos/libevent-%{version}-stable.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: doxygen

Patch00: libevent-1.4.13-stable-configure.patch

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-headers = %{version}-%{release}
Requires: %{name}-doc = %{version}-%{release}

%description devel
This package contains the static libraries documentation for %{name}. 
If you like to develop programs using %{name}, you will need 
to install %{name}-devel.

%package doc
Summary: Development documentation for %{name}
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
BuildArch: noarch

%description doc
This package contains the development documentation for %{name}. 
If you like to develop programs using %{name}-devel, you will 
need to install %{name}-doc.

%package headers
Summary: Header file for development  for %{name}
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
BuildArch: noarch

%description headers
This package contains the header files for %{name}. If you like to 
develop programs using %{name}, you will need to install %{name}-devel.

%prep
%setup -q -n libevent-%{version}-stable

# 477685 -  libevent-devel multilib conflict
%patch00 -p1

%build
%configure \
    --disable-dependency-tracking
make %{?_smp_mflags}

# Create the docs
make doxygen

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/html
(cd doxygen/html; \
	install *.* $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/html)

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/latex
(cd doxygen/latex; \
	install *.* $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/latex)

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/man/man3
(cd doxygen/man/man3; \
	install *.3 $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/man/man3)

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/sample
(cd sample; \
	install *.c Makefile* $RPM_BUILD_ROOT/%{_docdir}/%{name}-devel-%{version}/sample)

%check
make verify

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc README
%{_libdir}/libevent-*.so.*
%{_libdir}/libevent_core-*.so.*
%{_libdir}/libevent_extra-*.so.*

%files devel
%defattr(-,root,root,0755)
%{_libdir}/libevent.so
%{_libdir}/libevent.a
%{_libdir}/libevent_core.so
%{_libdir}/libevent_core.a
%{_libdir}/libevent_extra.so
%{_libdir}/libevent_extra.a

%{_bindir}/event_rpcgen.*

%{_mandir}/man3/*

%files doc
%defattr(-,root,root,0644)
%{_docdir}/%{name}-devel-%{version}/html/*
%{_docdir}/%{name}-devel-%{version}/latex/*
%{_docdir}/%{name}-devel-%{version}/man/man3/*
%{_docdir}/%{name}-devel-%{version}/sample/*

%files headers
%{_includedir}/event.h
%{_includedir}/evdns.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/event-config.h
%{_includedir}/evutil.h
%defattr(-,root,root,0644)

%changelog
* Mon Apr 23 2012 Steve Dickson <steved@redhat.com> 1.4.13-4
- Moved header files into there own rpm (bz 658051)
- Added event-config.h to the new headers rpm.

* Wed Apr  4 2012 Steve Dickson <steved@redhat.com> 1.4.13-3
- Removed the event-config.h file (bz 658051)

* Tue Mar  6 2012 Steve Dickson <steved@redhat.com> 1.4.13-2
- Moved documentation into its own rpm (bz 658051)

* Tue Dec 15 2009 Steve Dickson <steved@redhat.com> 1.4.13-1
- Updated to latest stable upstream version: 1.4.13

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.4.12-1.1
- Rebuilt for RHEL 6

* Tue Aug 18 2009 Steve Dickson <steved@redhat.com> 1.4.12-1
- Updated to latest stable upstream version: 1.4.12
- API documentation is now installed (bz 487977)
- libevent-devel multilib conflict (bz 477685)
- epoll backend allocates too much memory (bz 517918)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 20 2009 Steve Dickson <steved@redhat.com> 1.4.10-1
- Updated to latest stable upstream version: 1.4.10

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul  1 2008 Steve Dickson <steved@redhat.com> 1.4.5-1
- Updated to latest stable upstream version 1.4.5-stable

* Mon Jun  2 2008 Steve Dickson <steved@redhat.com> 1.4.4-1
- Updated to latest stable upstream version 1.4.4-stable

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3e-2
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Steve Dickson <steved@redhat.com> 1.3e-1
- Updated to latest stable upstream version 1.3e

* Fri Mar  9 2007 Steve Dickson <steved@redhat.com> 1.3b-1
- Updated to latest upstream version 1.3b
- Incorporated Merge Review comments (bz 226002)
- Increased the polling timeout (bz 204990)

* Tue Feb 20 2007 Steve Dickson <steved@redhat.com> 1.2a-1
- Updated to latest upstream version 1.2a

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1a-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1a-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 24 2006 Warren Togami <wtogami@redhat.com> - 1.1a-3
- rebuild (#177697)

* Mon Jul 04 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1a-2
- Removed unnecessary -r from rm

* Fri Jun 17 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1a-1
- Upstream update

* Wed Jun 08 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1-2
- Added some docs
- Moved "make verify" into %%check

* Mon Jun 06 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1-1
- Initial build for Fedora Extras, based on the package
  by Dag Wieers
