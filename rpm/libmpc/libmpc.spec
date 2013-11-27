Summary: C library for multiple precision complex arithmetic
Name: libmpc
Version: 0.8.1
Release: 1%{?dist}
License: LGPLv2+
Group: Development/Tools
URL: http://www.multiprecision.org/
Source0: http://www.multiprecision.org/mpc/download/mpc-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gmp-devel mpfr-devel texinfo

%description

MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as Mpfr.

%package devel
Summary: Header and shared development libraries for MPC
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: mpfr-devel gmp-devel

%description devel
Header files and shared object symlinks for MPC is a C library.

%prep
%setup -q -n mpc-%{version}

%build
%configure
make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/libmpc.{l,}a
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/mpc.info.gz ]; then # for --excludedocs
   /sbin/install-info %{_infodir}/mpc.info.gz %{_infodir}/dir || :
fi

%preun devel
if [ $1 = 0 ]; then
   if [ -f %{_infodir}/mpc.info.gz ]; then # for --excludedocs
      /sbin/install-info --delete %{_infodir}/mpc.info.gz %{_infodir}/dir || :
   fi
fi

%files
%defattr(-,root,root,-)
%doc README NEWS COPYING.LIB
%{_libdir}/libmpc.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmpc.so
%{_includedir}/mpc.h
%{_infodir}/*.info*

%changelog
* Mon Nov 25 2013 Teguh Dwicaksana <dheche@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1

* Fri Nov 13 2009 Petr Machata <pmachata@redhat.com> - 0.8-3
- Require mpfr-devel, gmp-devel in -devel subpackage
- Don't pass --entry to install-info

* Thu Nov 12 2009 Petr Machata <pmachata@redhat.com> - 0.8-2
- Rename the package to libmpc, it's a better choice of name
- %%preun should uninstall mpc's info page, not make's
- Move info page to -devel
- BR on -devel packages
- Drop postscript documentation

* Thu Nov 12 2009 Petr Machata <pmachata@redhat.com> - 0.8-1
- Initial package.
