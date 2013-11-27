%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Create deltas between rpms
Name: deltarpm
Version: 3.5
Release: 0.5.20090913git%{?dist}
License: BSD
Group: System Environment/Base
URL: http://gitorious.org/deltarpm/deltarpm
# Generate source by doing:
# git clone git://gitorious.org/deltarpm/deltarpm
# cd deltarpm
# git archive --format=tar --prefix="deltarpm-git-20090913" f716bb7 | \
# bzip2 > deltarpm-git-20090831.1.tar.bz2
Source: %{name}-git-20090913.tar.bz2
# Build with system zlib
Patch0: deltarpm-system-zlib.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, xz-devel, rpm-devel, popt-devel
BuildRequires: zlib-devel
BuildRequires: python-devel

%description
A deltarpm contains the difference between an old
and a new version of a rpm, which makes it possible
to recreate the new rpm from the deltarpm and the old
one. You don't have to have a copy of the old rpm,
deltarpms can also work with installed rpms.

%package -n drpmsync
Summary: Sync a file tree with deltarpms
Requires: deltarpm = %{version}-%{release}

%description -n drpmsync
This package contains a tool to sync a file tree with
deltarpms.

%package -n deltaiso
Summary: Create deltas between isos containing rpms
Requires: deltarpm = %{version}-%{release}

%description -n deltaiso
This package contains tools for creating and using deltasisos,
a difference between an old and a new iso containing rpms.

%package -n python-deltarpm
Summary: Python bindings for deltarpm
Requires: deltarpm = %{version}-%{release}

%description -n python-deltarpm
This package contains python bindings for deltarpm.

%prep
%setup -q -n %{name}-git-20090913
# Build with system zlib
%patch0 -p1 -b .zlib

%build
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags=''
%{__make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags='' \
    python

%install
%{__rm} -rf %{buildroot}
%makeinstall

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/applydeltarpm*
%doc %{_mandir}/man8/makedeltarpm*
%doc %{_mandir}/man8/combinedeltarpm*
%{_bindir}/applydeltarpm
%{_bindir}/combinedeltarpm
%{_bindir}/makedeltarpm
%{_bindir}/rpmdumpheader

%files -n deltaiso
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/applydeltaiso*
%doc %{_mandir}/man8/makedeltaiso*
%{_bindir}/applydeltaiso
%{_bindir}/fragiso
%{_bindir}/makedeltaiso

%files -n drpmsync
%defattr(-, root, root, 0755)
%doc LICENSE.BSD README
%doc %{_mandir}/man8/drpmsync*
%{_bindir}/drpmsync

%files -n python-deltarpm
%defattr(-, root, root, 0755)
%doc LICENSE.BSD
%{python_sitearch}/*

%changelog
* Mon Jan 11 2010 Panu Matilainen <pmatilai@redhat.com> 3.5-0.5.20090913git
- rebuild for rpm 4.8.0
- use %%global instead of %%define

* Wed Sep 30 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.5-0.4.20090913git
- Update patch to properly detect when an rpm is built with an rsync-friendly
  zlib and bail out.

* Wed Sep 30 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.5-0.3.20090913git
- Make building with system zlib selectable at build time.
- Fix cfile_detect_rsync() to detect rsync even if we don't have a zlib capable
  of making rsync-friendly compressed files.

* Wed Sep 30 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.5-0.2.20090913git
- Correct prerelease rlease numbering.
- Build against the system zlib, not the bundled library.  This remedies the
  fact that the included zlib is affected by CAN-2005-1849.

* Sun Sep 13 2009 Jonathan Dieter <jdieter@lesbg.com> - 3.5-0.git.20090913
- Merge python error patch upstream

* Thu Sep 10 2009 Bill Nottingham <notting@redhat.com> - 3.5-0.git.20090831.1.4
- fix python bindings to not require kernel >= 2.6.27

* Wed Sep  9 2009 Bill Nottingham <notting@redhat.com> - 3.5-0.git.20090831.1.3
- fix python bindings to:
  - call _exit(), not exit()
  - properly pythonize errors
  - not leak file descriptors

* Mon Aug 31 2009 Jonathan Dieter <jdieter@lesbg.com> - 3.5-0.git.20090831.1
- Add python bindings sub-package
- Fix build error

* Mon Aug 17 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090729.1
- Explain where we get the source from
- Split *deltaiso commands into deltaiso subpackage (#501953)

* Wed Jul 29 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090729
- Fix bug in writing Fedora's xz-compressed rpms (surely that's the last one)

* Mon Jul 27 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090727.1
- Fix bug in reading Fedora's xz-compressed rpms

* Mon Jul 27 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090727
- Update to current upstream git repository
- Add upstream xz compression support
- Drop all patches (they're now in upstream)
- Fix spelling mistakes (#505713)
- Fix url error (#506179)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Jonathan Dieter <jdieter@gmail.com> - 3.4-16
- Split drpmsync into a separate subpackage (#489231)

* Thu Mar 26 2009 Jonathan Dieter <jdieter@gmail.com> - 3.4-15
- Fix bug when checking sequence with new sha256 file digests

* Tue Mar 24 2009 Jonathan Dieter <jdieter@gmail.com> - 3.4-14
- Add support for rpms with sha256 file digests

* Fri Mar 06 2009 Jesse Keating <jkeating@redhat.com> - 3.4-13
- Rebuild for new rpm libs

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jul 13 2008 Jonathan Dieter <jdieter@gmail.com> - 3.4-11
- Rebuild for rpm 4.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.4-10
- Autorebuild for GCC 4.3

* Mon Jan  7 2008 Jonathan Dieter <jdieter@gmail.com> - 3.4-9
- Add patch that allows deltarpm to rebuild rpms from deltarpms that have
  had the rpm signature added after their creation.  The code came from
  upstream.
- Drop nodoc patch added in 3.4-4 as most packages in repository have been
  updated since April-May 2007 and this patch was supposed to be temporary.

* Wed Aug 29 2007 Jonathan Dieter <jdieter@gmail.com> - 3.4-6
- Bring in popt-devel in BuildRequires to fix build in x86_64

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.4-5
- Rebuild for selinux ppc32 issue.

* Wed Jul 11 2007 Jonathan Dieter <jdieter@gmail.com> - 3.4-4
- Fix prelink bug
- Ignore verify bits on doc files as they were set incorrectly in older
  versions of rpm.  Without this patch, deltarpm will not delta doc files
  in rpm created before April-May 2007

* Tue Jun  5 2007 Jeremy Katz <katzj@redhat.com> - 3.4-3
- include colored binaries from non-multilib-dirs so that deltas can work 
  on multilib platforms

* Wed May 09 2007 Adam Jackson <ajax@redhat.com> 3.4-2
- Add -a flag to work around multilib ignorance. (#238964)

* Tue Mar 06 2007 Adam Jackson <ajax@redhat.com> 3.4-1
- Update to 3.4 (#231154)

* Mon Feb 12 2007 Adam Jackson <ajax@redhat.com> 3.3-7
- Add RPM_OPT_FLAGS to make line. (#227380)

* Mon Feb 05 2007 Adam Jackson <ajax@redhat.com> 3.3-6
- Fix rpm db corruption in rpmdumpheader.  (#227326)

* Mon Sep 11 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-5
- Rebuilding for new toolset

* Thu Aug 17 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-4
- Removing BuildRequires: gcc

* Tue Aug 15 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-3
- Fedora packaging guidelines build

* Tue Aug  8 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-2
- Added BuildRequires: rpm-devel, gcc

* Sat Dec 03 2005 Dries Verachtert <dries@ulyssis.org> - 3.3-1 - 3768/dries
- Initial package.
