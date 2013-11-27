%global DATE 20121109
%global SVNREV 193356
%global gcc_version 4.7.2
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 8
%global _unpackaged_files_terminate_build 0
%global multilib_64_archs sparc64 ppc64 s390x x86_64
%ifarch %{ix86} x86_64 ia64 ppc ppc64 alpha
%global build_ada 1
%else
%global build_ada 0
%endif
%global build_java 1
%ifarch %{ix86} x86_64 ppc ppc64 s390 s390x %{arm}
%global build_go 1
%else
%global build_go 0
%endif
%ifarch %{ix86} x86_64 ia64
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%if 0%{?rhel} >= 7
%global build_cloog 0
%else
%global build_cloog 1
%endif
%global build_libstdcxx_docs 0
# If you don't have already a usable gcc-java and libgcj for your arch,
# do on some arch which has it rpmbuild -bc --with java_tar gcc.spec
# which creates libjava-classes-%{version}-%{release}.tar.bz2
# With this then on the new arch do rpmbuild -ba -v --with java_bootstrap gcc.spec
%global bootstrap_java %{?_with_java_bootstrap:%{build_java}}%{!?_with_java_bootstrap:0}
%global build_java_tar %{?_with_java_tar:%{build_java}}%{!?_with_java_tar:0}
%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%global multilib_32_arch i686
%endif
Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-4_7-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
%global fastjar_ver 0.97
Source4: http://download.savannah.nongnu.org/releases/fastjar/fastjar-%{fastjar_ver}.tar.gz
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
BuildRequires: binutils >= 2.20.51.0.2-12
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils
BuildRequires: systemtap-sdt-devel >= 1.3
%if %{build_go}
BuildRequires: net-tools
%endif
# For VTA guality testing
BuildRequires: gdb
%if %{build_java}
BuildRequires: /usr/share/java/eclipse-ecj.jar, zip, unzip
%if %{bootstrap_java}
Source10: libjava-classes-%{version}-%{release}.tar.bz2
%else
BuildRequires: gcc-java, libgcj
%endif
%endif
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
%if %{build_cloog}
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
BuildRequires: ppl >= 0.11.2, ppl-devel >= 0.11.2
%else
BuildRequires: ppl >= 0.10, ppl-devel >= 0.10
%endif
BuildRequires: cloog-ppl >= 0.15, cloog-ppl-devel >= 0.15
%endif
%if %{build_libstdcxx_docs}
BuildRequires: doxygen >= 1.7.1
BuildRequires: graphviz
%endif
Requires: cpp = %{version}-%{release}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
# Need binutils that support %gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
Requires: binutils >= 2.20.51.0.2-12
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%ifarch %{arm}
Requires: glibc >= 2.16
%endif
%endif
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
Obsoletes: libgnat < %{version}-%{release}
%endif
%if %{build_cloog}
Requires: cloog-ppl >= 0.15
%endif
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
AutoReq: true
Provides: bundled(libiberty)

Patch0: gcc47-hack.patch
Patch1: gcc47-c++-builtin-redecl.patch
Patch2: gcc47-java-nomulti.patch
Patch3: gcc47-ppc32-retaddr.patch
Patch5: gcc47-rh330771.patch
Patch6: gcc47-i386-libgomp.patch
Patch7: gcc47-sparc-config-detection.patch
Patch8: gcc47-libgomp-omp_h-multilib.patch
Patch9: gcc47-libtool-no-rpath.patch
Patch10: gcc47-cloog-dl.patch
Patch11: gcc47-pr38757.patch
Patch12: gcc47-libstdc++-docs.patch
Patch13: gcc47-no-add-needed.patch
Patch14: gcc47-ppl-0.10.patch
Patch15: gcc47-libitm-fno-exceptions.patch
Patch16: gcc47-rh837630.patch
Patch17: gcc47-arm-hfp-ldso.patch
Patch18: gcc47-pr55137.patch
Patch19: gcc47-pr55236.patch

Patch1000: fastjar-0.97-segfault.patch
Patch1001: fastjar-0.97-len1.patch
Patch1002: fastjar-0.97-filename0.patch
Patch1003: fastjar-CVE-2010-0831.patch
Patch1004: fastjar-man.patch

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%global _gnu %{nil}
%endif
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparcv9 ppc
%global gcc_target_platform %{_target_platform}
%endif

%description
The gcc package contains the GNU Compiler Collection version 4.7.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 4.7 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Group: System Environment/Libraries
Autoreq: true
Requires: glibc >= 2.10.90-7

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++%{?_isa} = %{version}-%{release}
Autoreq: true

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++-static
Summary: Static libraries for the GNU standard C++ library
Group: Development/Libraries
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description -n libstdc++-static
Static libraries for the GNU standard C++ library. 

%package -n libstdc++-docs
Summary: Documentation for the GNU standard C++ library
Group: Development/Libraries
Autoreq: true

%description -n libstdc++-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Autoreq: true

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: gcc-c++ = %{version}-%{release}, gcc-objc = %{version}-%{release}
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%package gfortran
Summary: Fortran support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
Requires: libquadmath-devel = %{version}-%{release}
%endif
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Group: System Environment/Libraries
Autoreq: true
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
%endif

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgfortran-static
Summary: Static Fortran libraries
Group: Development/Libraries
Requires: libgfortran = %{version}-%{release}
Requires: gcc = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath-static = %{version}-%{release}
%endif

%description -n libgfortran-static
This package contains static Fortran libraries.

%package -n libgomp
Summary: GCC OpenMP v3.0 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v3.0 support.

%package -n libmudflap
Summary: GCC mudflap shared support library
Group: System Environment/Libraries

%description -n libmudflap
This package contains GCC shared support library which is needed
for mudflap support.

%package -n libmudflap-devel
Summary: GCC mudflap support
Group: Development/Libraries
Requires: libmudflap = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libmudflap-devel
This package contains headers for building mudflap-instrumented programs.

To instrument a non-threaded program, add -fmudflap
option to GCC and when linking add -lmudflap, for threaded programs
also add -fmudflapth and -lmudflapth.

%package -n libmudflap-static
Summary: Static libraries for mudflap support
Group: Development/Libraries
Requires: libmudflap-devel = %{version}-%{release}

%description -n libmudflap-static
This package contains static libraries for building mudflap-instrumented
programs.

%package -n libquadmath
Summary: GCC __float128 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n libquadmath-devel
Summary: GCC __float128 support
Group: Development/Libraries
Requires: libquadmath = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libquadmath-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libquadmath-static
Summary: Static libraries for __float128 support
Group: Development/Libraries
Requires: libquadmath-devel = %{version}-%{release}

%description -n libquadmath-static
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%package -n libitm
Summary: The GNU Transactional Memory library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libitm-devel
Summary: The GNU Transactional Memory support
Group: Development/Libraries
Requires: libitm = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libitm-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package -n libitm-static
Summary: The GNU Transactional Memory static library
Group: Development/Libraries
Requires: libitm-devel = %{version}-%{release}

%description -n libitm-static
This package contains GNU Transactional Memory static libraries.

%package java
Summary: Java support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgcj = %{version}-%{release}
Requires: libgcj-devel = %{version}-%{release}
Requires: /usr/share/java/eclipse-ecj.jar
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description java
This package adds support for compiling Java(tm) programs and
bytecode into native code.

%package -n libgcj
Summary: Java runtime library for gcc
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: zip >= 2.1
Requires: gtk2 >= 2.4.0
Requires: glib2 >= 2.4.0
Requires: libart_lgpl >= 2.1.0
%if %{build_java}
BuildRequires: gtk2-devel >= 2.4.0
BuildRequires: glib2-devel >= 2.4.0
BuildRequires: libart_lgpl-devel >= 2.1.0
BuildRequires: alsa-lib-devel
BuildRequires: libXtst-devel
BuildRequires: libXt-devel
%endif
Autoreq: true

%description -n libgcj
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%package -n libgcj-devel
Summary: Libraries for Java development using GCC
Group: Development/Languages
Requires: libgcj%{?_isa} = %{version}-%{release}
Requires: zlib-devel%{?_isa}
Requires: /bin/awk
Autoreq: false
Autoprov: false

%description -n libgcj-devel
The Java(tm) static libraries and C header files. You will need this
package to compile your Java programs using the GCC Java compiler (gcj).

%package -n libgcj-src
Summary: Java library sources from GCC4 preview
Group: System Environment/Libraries
Requires: libgcj = %{version}-%{release}
Autoreq: true

%description -n libgcj-src
The Java(tm) runtime library sources for use in Eclipse.

%package -n cpp
Summary: The C Preprocessor
Group: Development/Languages
Requires: filesystem >= 2.4.30
Provides: /lib/cpp
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description -n cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package gnat
Summary: Ada 95 support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgnat = %{version}-%{release}, libgnat-devel = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description gnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes development tools,
the documents and Ada 95 compiler.

%package -n libgnat
Summary: GNU Ada 95 runtime shared libraries
Group: System Environment/Libraries
Autoreq: true

%description -n libgnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared libraries,
which are required to run programs compiled with the GNAT.

%package -n libgnat-devel
Summary: GNU Ada 95 libraries
Group: Development/Languages
Autoreq: true

%description -n libgnat-devel
GNAT is a GNU Ada 95 front-end to GCC. This package includes libraries,
which are required to compile with the GNAT.

%package -n libgnat-static
Summary: GNU Ada 95 static libraries
Group: Development/Languages
Requires: libgnat-devel = %{version}-%{release}
Autoreq: true

%description -n libgnat-static
GNAT is a GNU Ada 95 front-end to GCC. This package includes static libraries.

%package go
Summary: Go support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgo = %{version}-%{release}
Requires: libgo-devel = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Autoreq: true

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%package -n libgo
Summary: Go runtime
Group: System Environment/Libraries
Autoreq: true

%description -n libgo
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%package -n libgo-devel
Summary: Go development libraries
Group: Development/Languages
Requires: libgo = %{version}-%{release}
Autoreq: true

%description -n libgo-devel
This package includes libraries and support files for compiling
Go programs.

%package -n libgo-static
Summary: Static Go libraries
Group: Development/Libraries
Requires: libgo = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libgo-static
This package contains static Go libraries.

%package plugin-devel
Summary: Support for compiling GCC plugins
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1

%description plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%if 0%{?_enable_debug_packages}
%define debug_package %{nil}
%global __debug_package 1
%global __debug_install_post \
   %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/gcc-%{version}-%{DATE}"\
    %{_builddir}/gcc-%{version}-%{DATE}/split-debuginfo.sh\
%{nil}

%package debuginfo
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: 0
Requires: gcc-base-debuginfo = %{version}-%{release}

%description debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%files debuginfo -f debugfiles.list
%defattr(-,root,root)

%package base-debuginfo
Summary: Debug information for libraries from package %{name}
Group: Development/Debug
AutoReqProv: 0

%description base-debuginfo
This package provides debug information for libgcc_s, libgomp and
libstdc++ libraries from package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%files base-debuginfo -f debugfiles-base.list
%defattr(-,root,root)
%endif

%prep
%setup -q -n gcc-%{version}-%{DATE}
%patch0 -p0 -b .hack~
%patch1 -p0 -b .c++-builtin-redecl~
%patch2 -p0 -b .java-nomulti~
%patch3 -p0 -b .ppc32-retaddr~
%patch5 -p0 -b .rh330771~
%patch6 -p0 -b .i386-libgomp~
%patch7 -p0 -b .sparc-config-detection~
%patch8 -p0 -b .libgomp-omp_h-multilib~
%patch9 -p0 -b .libtool-no-rpath~
%if %{build_cloog}
%patch10 -p0 -b .cloog-dl~
%endif
%patch11 -p0 -b .pr38757~
%if %{build_libstdcxx_docs}
%patch12 -p0 -b .libstdc++-docs~
%endif
%patch13 -p0 -b .no-add-needed~
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
%patch14 -p0 -b .ppl-0.10~
%endif
%patch15 -p0 -b .libitm-fno-exceptions~
%patch16 -p0 -b .rh837630~
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%patch17 -p0 -b .arm-hfp-ldso~
%endif
%patch18 -p0 -b .pr55137~
%patch19 -p0 -b .pr55236~

%if 0%{?_enable_debug_packages}
cat > split-debuginfo.sh <<\EOF
#!/bin/sh
BUILDDIR="%{_builddir}/gcc-%{version}-%{DATE}"
if [ -f "${BUILDDIR}"/debugfiles.list \
     -a -f "${BUILDDIR}"/debuglinks.list ]; then
  > "${BUILDDIR}"/debugsources-base.list
  > "${BUILDDIR}"/debugfiles-base.list
  cd "${RPM_BUILD_ROOT}"
  for f in `find usr/lib/debug -name \*.debug \
	    | egrep 'lib[0-9]*/lib(gcc|gomp|stdc|quadmath|itm)'`; do
    echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
    if [ -f "$f" -a ! -L "$f" ]; then
      cp -a "$f" "${BUILDDIR}"/test.debug
      /usr/lib/rpm/debugedit -b "${RPM_BUILD_DIR}" -d /usr/src/debug \
			     -l "${BUILDDIR}"/debugsources-base.list \
			     "${BUILDDIR}"/test.debug
      rm -f "${BUILDDIR}"/test.debug
    fi
  done
  for f in `find usr/lib/debug/.build-id -type l`; do
    ls -l "$f" | egrep -q -- '->.*lib[0-9]*/lib(gcc|gomp|stdc|quadmath|itm)' \
      && echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
  done
  grep -v -f "${BUILDDIR}"/debugfiles-base.list \
    "${BUILDDIR}"/debugfiles.list > "${BUILDDIR}"/debugfiles.list.new
  mv -f "${BUILDDIR}"/debugfiles.list.new "${BUILDDIR}"/debugfiles.list
  for f in `LC_ALL=C sort -z -u "${BUILDDIR}"/debugsources-base.list \
	    | grep -E -v -z '(<internal>|<built-in>)$' \
	    | xargs --no-run-if-empty -n 1 -0 echo \
	    | sed 's,^,usr/src/debug/,'`; do
    if [ -f "$f" ]; then
      echo "/$f" >> "${BUILDDIR}"/debugfiles-base.list
      echo "%%exclude /$f" >> "${BUILDDIR}"/debugfiles.list
    fi
  done
  mv -f "${BUILDDIR}"/debugfiles-base.list{,.old}
  echo "%%dir /usr/lib/debug" > "${BUILDDIR}"/debugfiles-base.list
  awk 'BEGIN{FS="/"}(NF>4&&$NF){d="%%dir /"$2"/"$3"/"$4;for(i=5;i<NF;i++){d=d"/"$i;if(!v[d]){v[d]=1;print d}}}' \
    "${BUILDDIR}"/debugfiles-base.list.old >> "${BUILDDIR}"/debugfiles-base.list
  cat "${BUILDDIR}"/debugfiles-base.list.old >> "${BUILDDIR}"/debugfiles-base.list
  rm -f "${BUILDDIR}"/debugfiles-base.list.old
fi
EOF
chmod 755 split-debuginfo.sh
%endif

# This testcase doesn't compile.
rm libjava/testsuite/libjava.lang/PR35020*

tar xzf %{SOURCE4}

%patch1000 -p0 -b .fastjar-0.97-segfault~
%patch1001 -p0 -b .fastjar-0.97-len1~
%patch1002 -p0 -b .fastjar-0.97-filename0~
%patch1003 -p0 -b .fastjar-CVE-2010-0831~
%patch1004 -p0 -b .fastjar-man~

%if %{bootstrap_java}
tar xjf %{SOURCE10}
%endif

sed -i -e 's/4\.7\.3/4.7.2/' gcc/BASE-VER
echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
# Default to -gdwarf-4 -fno-debug-types-section rather than -gdwarf-2
sed -i '/UInteger Var(dwarf_version)/s/Init(2)/Init(4)/' gcc/common.opt
sed -i '/flag_debug_types_section/s/Init(1)/Init(0)/' gcc/common.opt
sed -i '/dwarf_record_gcc_switches/s/Init(0)/Init(1)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)2\./\14./' gcc/doc/invoke.texi
%else
# Default to -gdwarf-3 rather than -gdwarf-2
sed -i '/UInteger Var(dwarf_version)/s/Init(2)/Init(3)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)2\./\13./' gcc/doc/invoke.texi
sed -i 's/#define[[:blank:]]*EMIT_ENTRY_VALUE[[:blank:]].*$/#define EMIT_ENTRY_VALUE 0/' gcc/{var-tracking,dwarf2out}.c
sed -i 's/#define[[:blank:]]*EMIT_TYPED_DWARF_STACK[[:blank:]].*$/#define EMIT_TYPED_DWARF_STACK 0/' gcc/dwarf2out.c
sed -i 's/#define[[:blank:]]*EMIT_DEBUG_MACRO[[:blank:]].*$/#define EMIT_DEBUG_MACRO 0/' gcc/dwarf2out.c
%endif

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

# Hack to avoid building multilib libjava
perl -pi -e 's/^all: all-redirect/ifeq (\$(MULTISUBDIR),)\nall: all-redirect\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-redirect/ifeq (\$(MULTISUBDIR),)\ninstall: install-redirect\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-redirect/ifeq (\$(MULTISUBDIR),)\ncheck: check-redirect\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^all: all-recursive/ifeq (\$(MULTISUBDIR),)\nall: all-recursive\nelse\nall:\n\techo Multilib libjava build disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^install: install-recursive/ifeq (\$(MULTISUBDIR),)\ninstall: install-recursive\nelse\ninstall:\n\techo Multilib libjava install disabled\nendif/' libjava/Makefile.in
perl -pi -e 's/^check: check-recursive/ifeq (\$(MULTISUBDIR),)\ncheck: check-recursive\nelse\ncheck:\n\techo Multilib libjava check disabled\nendif/' libjava/Makefile.in

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

%build

%if %{build_java}
export GCJ_PROPERTIES=jdt.compiler.useSingleThread=true
# gjar isn't usable, so even when GCC source tree no longer includes
# fastjar, build it anyway.
mkdir fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
cd fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
../configure CFLAGS="%{optflags}" --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir}
make %{?_smp_mflags}
export PATH=`pwd`${PATH:+:$PATH}
cd ../../
%endif

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_java}
%if !%{bootstrap_java}
# If we don't have gjavah in $PATH, try to build it with the old gij
mkdir java_hacks
cd java_hacks
cp -a ../../libjava/classpath/tools/external external
mkdir -p gnu/classpath/tools
cp -a ../../libjava/classpath/tools/gnu/classpath/tools/{common,javah,getopt} gnu/classpath/tools/
cp -a ../../libjava/classpath/tools/resource/gnu/classpath/tools/common/Messages.properties gnu/classpath/tools/common
cp -a ../../libjava/classpath/tools/resource/gnu/classpath/tools/getopt/Messages.properties gnu/classpath/tools/getopt
cd external/asm; for i in `find . -name \*.java`; do gcj --encoding ISO-8859-1 -C $i -I.; done; cd ../..
for i in `find gnu -name \*.java`; do gcj -C $i -I. -Iexternal/asm/; done
gcj -findirect-dispatch -O2 -fmain=gnu.classpath.tools.javah.Main -I. -Iexternal/asm/ `find . -name \*.class` -o gjavah.real
cat > gjavah <<EOF
#!/bin/sh
export CLASSPATH=`pwd`${CLASSPATH:+:$CLASSPATH}
exec `pwd`/gjavah.real "\$@"
EOF
chmod +x `pwd`/gjavah
cat > ecj1 <<EOF
#!/bin/sh
exec gij -cp /usr/share/java/eclipse-ecj.jar org.eclipse.jdt.internal.compiler.batch.GCCMain "\$@"
EOF
chmod +x `pwd`/ecj1
export PATH=`pwd`${PATH:+:$PATH}
cd ..
%endif
%endif

CC=gcc
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
%endif
%ifarch ppc64
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
fi
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables/' \
      ../gcc/Makefile.in
    ;;
esac
enablelgo=
enablelada=
%if %{build_ada}
enablelada=,ada
%endif
%if %{build_go}
enablelgo=,go
%endif
CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="`echo $OPT_FLAGS | sed 's/ -Wall / /g'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--disable-build-with-cxx --disable-build-poststage1-with-cxx \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object --enable-linker-build-id --with-linker-hash-style=gnu \
	--enable-languages=c,c++,objc,obj-c++,java,fortran${enablelada}${enablelgo},lto \
	--enable-plugin --enable-initfini-array \
%if !%{build_java}
	--disable-libgcj \
%else
	--enable-java-awt=gtk --disable-dssi \
	--with-java-home=%{_prefix}/lib/jvm/java-1.5.0-gcj-1.5.0.0/jre \
	--enable-libgcj-multifile \
%if !%{bootstrap_java}
	--enable-java-maintainer-mode \
%endif
	--with-ecj-jar=/usr/share/java/eclipse-ecj.jar \
	--disable-libjava-multilib \
%endif
%if %{build_cloog}
	--with-ppl --with-cloog \
%else
	--without-ppl --without-cloog \
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%if 0%{?rhel} >= 6
%ifarch ppc ppc64
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
%ifarch s390 s390x
	--with-arch=z9-109 --with-tune=z10 --enable-decimal-float \
%endif
%ifarch armv7hl
	--with-cpu=cortex-a8 --with-tune=cortex-a8 --with-arch=armv7-a \
	--with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform}
%endif

%ifarch %{arm} sparc sparcv9 sparc64
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
%else
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
%endif

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc
mkdir -p rpm.doc/boehm-gc rpm.doc/fastjar rpm.doc/libffi rpm.doc/libjava
mkdir -p rpm.doc/go rpm.doc/libgo rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp}

for i in {gcc,gcc/cp,gcc/java,gcc/ada,libstdc++-v3,libobjc,libmudflap,libgomp}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
(cd boehm-gc; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/boehm-gc/$i.gc
done)
(cd fastjar-%{fastjar_ver}; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/fastjar/$i.fastjar
done)
(cd libffi; for i in ChangeLog* README* LICENSE; do
	cp -p $i ../rpm.doc/libffi/$i.libffi
done)
(cd libjava; for i in ChangeLog* README*; do
	cp -p $i ../rpm.doc/libjava/$i.libjava
done)
cp -p libjava/LIBGCJ_LICENSE rpm.doc/libjava/
%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif
%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif
%if %{build_go}
(cd gcc/go; for i in README* ChangeLog*; do
	cp -p $i ../../rpm.doc/go/$i
done)
(cd libgo; for i in LICENSE* PATENTS* README; do
	cp -p $i ../rpm.doc/libgo/$i.libgo
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%if %{build_java_tar}
find libjava -name \*.h -type f | xargs grep -l '// DO NOT EDIT THIS FILE - it is machine generated' > libjava-classes.list
find libjava -name \*.class -type f >> libjava-classes.list
find libjava/testsuite -name \*.jar -type f >> libjava-classes.list
tar cf - -T libjava-classes.list | bzip2 -9 > $RPM_SOURCE_DIR/libjava-classes-%{version}-%{release}.tar.bz2
%endif

%install
export QA_RPATHS=$[ 0x0020 ]
rm -fr %{buildroot}

cd obj-%{gcc_target_platform}

%if %{build_java}
export GCJ_PROPERTIES=jdt.compiler.useSingleThread=true
export PATH=`pwd`/../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}${PATH:+:$PATH}
%if !%{bootstrap_java}
export PATH=`pwd`/java_hacks${PATH:+:$PATH}
%endif
%endif

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
%if %{build_java}
make DESTDIR=%{buildroot} -C %{gcc_target_platform}/libjava install-src.zip
%endif
%if %{build_ada}
chmod 644 %{buildroot}%{_infodir}/gnat*
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}

# fix some things
ln -sf gcc %{buildroot}%{_prefix}/bin/cc
rm -f %{buildroot}%{_prefix}/lib/cpp
ln -sf ../bin/cpp %{buildroot}/%{_prefix}/lib/cpp
ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
ln -sf gcc %{buildroot}%{_prefix}/bin/gnatgcc

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/*.h.gch dirs
# 1) there is no bits/*.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}/man3
cp -r -p $libstdcxx_doc_builddir/man/man3/* %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

%ifarch sparcv9 ppc
FULLLPATH=$FULLPATH/lib32
%endif
%ifarch sparc64 ppc64
FULLLPATH=$FULLPATH/lib64
%endif
if [ -n "$FULLLPATH" ]; then
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f
%if %{build_java}
# gcj -static doesn't work properly anyway, unless using --whole-archive
# and saving 35MB is not bad.
find %{buildroot} -name libgcj.a -o -name libgtkpeer.a \
		     -o -name libgjsmalsa.a -o -name libgcj-tools.a -o -name libjvm.a \
		     -o -name libgij.a -o -name libgcj_bc.a -o -name libjavamath.a \
  | xargs rm -f

mv %{buildroot}%{_prefix}/lib/libgcj.spec $FULLPATH/
sed -i -e 's/lib: /&%%{static:%%eJava programs cannot be linked statically}/' \
  $FULLPATH/libgcj.spec
%endif

mv %{buildroot}%{_prefix}/lib/libgfortran.spec $FULLPATH/
%if %{build_libitm}
mv %{buildroot}%{_prefix}/lib/libitm.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_version}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
%ifarch ppc
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif
%ifarch ppc64
rm -f $FULLPATH/32/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-powerpc)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%endif
%ifarch %{arm}
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT(elf32-littlearm)
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so %{buildroot}%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -dD -xc /dev/null | grep __LONG_MAX__.*2147483647; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

%if %{build_java}
pushd ../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}
make install DESTDIR=%{buildroot}
popd

if [ "%{_lib}" != "lib" ]; then
  mkdir -p %{buildroot}%{_prefix}/%{_lib}/pkgconfig
  sed '/^libdir/s/lib$/%{_lib}/' %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-*.pc \
    > %{buildroot}%{_prefix}/%{_lib}/pkgconfig/`basename %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-*.pc`
fi

%endif

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
pushd ../libstdc++-v3/python
for i in `find . -name \*.py`; do
  touch -r $i %{buildroot}%{_prefix}/share/gcc-%{gcc_version}/python/$i
done
touch -r hook.in %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc++*gdb.py
popd

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../libobjc.so.4 libobjc.so
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../libgfortran.so.3.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
ln -sf ../../../libmudflap.so.0.* libmudflap.so
ln -sf ../../../libmudflapth.so.0.* libmudflapth.so
%if %{build_go}
ln -sf ../../../libgo.so.0.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libitm}
ln -sf ../../../libitm.so.1.* libitm.so
%endif
%if %{build_java}
ln -sf ../../../libgcj.so.13.* libgcj.so
ln -sf ../../../libgcj-tools.so.13.* libgcj-tools.so
ln -sf ../../../libgij.so.13.* libgij.so
%endif
else
ln -sf ../../../../%{_lib}/libobjc.so.4 libobjc.so
ln -sf ../../../../%{_lib}/libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.3.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
ln -sf ../../../../%{_lib}/libmudflap.so.0.* libmudflap.so
ln -sf ../../../../%{_lib}/libmudflapth.so.0.* libmudflapth.so
%if %{build_go}
ln -sf ../../../../%{_lib}/libgo.so.0.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../../%{_lib}/libquadmath.so.0.* libquadmath.so
%endif
%if %{build_libitm}
ln -sf ../../../../%{_lib}/libitm.so.1.* libitm.so
%endif
%if %{build_java}
ln -sf ../../../../%{_lib}/libgcj.so.13.* libgcj.so
ln -sf ../../../../%{_lib}/libgcj-tools.so.13.* libgcj-tools.so
ln -sf ../../../../%{_lib}/libgij.so.13.* libgij.so
%endif
fi
%if %{build_java}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcj_bc.so $FULLLPATH/
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libmudflap{,th}.*a $FULLLPATH/
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_go}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgo.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgobegin.*a $FULLLPATH/
%endif

%if %{build_ada}
%ifarch sparcv9 ppc
rm -rf $FULLPATH/64/ada{include,lib}
%endif
%ifarch %{multilib_64_archs}
rm -rf $FULLPATH/32/ada{include,lib}
%endif
if [ "$FULLPATH" != "$FULLLPATH" ]; then
mv -f $FULLPATH/ada{include,lib} $FULLLPATH/
pushd $FULLLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../../libgnarl-*.so libgnarl-4.7.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-4.7.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-4.7.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-4.7.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-4.7.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-4.7.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-4.7.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-4.7.so
fi
popd
fi
%endif

%ifarch sparcv9 ppc
ln -sf ../../../../../lib64/libobjc.so.4 64/libobjc.so
ln -sf ../`echo ../../../../lib/libstdc++.so.6.*[0-9] | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.3.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
rm -f libmudflap.so libmudflapth.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflap.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflapth.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > 64/libmudflap.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > 64/libmudflapth.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgo.so.0.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgo.so.0.* | sed 's,^.*libg,libg,'`' )' > 64/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 64/libquadmath.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 64/libitm.so
%endif
%if %{build_java}
ln -sf ../`echo ../../../../lib/libgcj.so.13.* | sed s~/lib/~/lib64/~` 64/libgcj.so
ln -sf ../`echo ../../../../lib/libgcj-tools.so.13.* | sed s~/lib/~/lib64/~` 64/libgcj-tools.so
ln -sf ../`echo ../../../../lib/libgij.so.13.* | sed s~/lib/~/lib64/~` 64/libgij.so
ln -sf lib32/libgcj_bc.so libgcj_bc.so
ln -sf ../lib64/libgcj_bc.so 64/libgcj_bc.so
%endif
ln -sf lib32/libgfortran.a libgfortran.a
ln -sf ../lib64/libgfortran.a 64/libgfortran.a
mv -f %{buildroot}%{_prefix}/lib64/libobjc.*a 64/
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libsupc++.a libsupc++.a
ln -sf ../lib64/libsupc++.a 64/libsupc++.a
ln -sf lib32/libmudflap.a libmudflap.a
ln -sf ../lib64/libmudflap.a 64/libmudflap.a
ln -sf lib32/libmudflapth.a libmudflapth.a
ln -sf ../lib64/libmudflapth.a 64/libmudflapth.a
%if %{build_libquadmath}
ln -sf lib32/libquadmath.a libquadmath.a
ln -sf ../lib64/libquadmath.a 64/libquadmath.a
%endif
%if %{build_libitm}
ln -sf lib32/libitm.a libitm.a
ln -sf ../lib64/libitm.a 64/libitm.a
%endif
%if %{build_go}
ln -sf lib32/libgo.a libgo.a
ln -sf ../lib64/libgo.a 64/libgo.a
ln -sf lib32/libgobegin.a libgobegin.a
ln -sf ../lib64/libgobegin.a 64/libgobegin.a
%endif
%if %{build_ada}
ln -sf lib32/adainclude adainclude
ln -sf ../lib64/adainclude 64/adainclude
ln -sf lib32/adalib adalib
ln -sf ../lib64/adalib 64/adalib
%endif
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
ln -sf ../../../../libobjc.so.4 32/libobjc.so
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.*[0-9] | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgfortran.so.3.* | sed s~/../lib64/~/~` 32/libgfortran.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
rm -f libmudflap.so libmudflapth.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflap.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > libmudflapth.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflap.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflap.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libmudflapth.so.0.* | sed 's,^.*libm,libm,'`' )' > 32/libmudflapth.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgo.so.0.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgo.so.0.* | sed 's,^.*libg,libg,'`' )' > 32/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 32/libquadmath.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 32/libitm.so
%endif
%if %{build_java}
ln -sf ../`echo ../../../../lib64/libgcj.so.13.* | sed s~/../lib64/~/~` 32/libgcj.so
ln -sf ../`echo ../../../../lib64/libgcj-tools.so.13.* | sed s~/../lib64/~/~` 32/libgcj-tools.so
ln -sf ../`echo ../../../../lib64/libgij.so.13.* | sed s~/../lib64/~/~` 32/libgij.so
%endif
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%endif
%ifarch sparc64 ppc64
ln -sf ../lib32/libgfortran.a 32/libgfortran.a
ln -sf lib64/libgfortran.a libgfortran.a
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libsupc++.a 32/libsupc++.a
ln -sf lib64/libsupc++.a libsupc++.a
ln -sf ../lib32/libmudflap.a 32/libmudflap.a
ln -sf lib64/libmudflap.a libmudflap.a
ln -sf ../lib32/libmudflapth.a 32/libmudflapth.a
ln -sf lib64/libmudflapth.a libmudflapth.a
%if %{build_libquadmath}
ln -sf ../lib32/libquadmath.a 32/libquadmath.a
ln -sf lib64/libquadmath.a libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../lib32/libitm.a 32/libitm.a
ln -sf lib64/libitm.a libitm.a
%endif
%if %{build_go}
ln -sf ../lib32/libgo.a 32/libgo.a
ln -sf lib64/libgo.a libgo.a
ln -sf ../lib32/libgobegin.a 32/libgobegin.a
ln -sf lib64/libgobegin.a libgobegin.a
%endif
%if %{build_java}
ln -sf ../lib32/libgcj_bc.so 32/libgcj_bc.so
ln -sf lib64/libgcj_bc.so libgcj_bc.so
%endif
%if %{build_ada}
ln -sf ../lib32/adainclude 32/adainclude
ln -sf lib64/adainclude adainclude
ln -sf ../lib32/adalib 32/adalib
ln -sf lib64/adalib adalib
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgfortran.a 32/libgfortran.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libsupc++.a 32/libsupc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflap.a 32/libmudflap.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libmudflapth.a 32/libmudflapth.a
%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libquadmath.a 32/libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libitm.a 32/libitm.a
%endif
%if %{build_go}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgo.a 32/libgo.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgobegin.a 32/libgobegin.a
%endif
%if %{build_java}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/libgcj_bc.so 32/libgcj_bc.so
%endif
%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_version}/adalib 32/adalib
%endif
%endif
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libmudflap.a -o -name libmudflapth.a \
		    -o -name libgcc.a -o -name libgcov.a -o -name libquadmath.a \
		    -o -name libitm.a -o -name libgo.a -o -name libcaf\*.a \) \
		 -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.3.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmudflap{,th}.so.0.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%endif
%if %{build_go}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgo.so.0.*
%endif
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.4.*

%if %{build_ada}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnat*so*
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > %{buildroot}%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_prefix}/bin/c?9

cd ..
%find_lang %{name}
%find_lang cpplib

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a}
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
rm -f %{buildroot}%{_prefix}/bin/gappletviewer || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-%{version} || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gccgo || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcj || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ar || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-nm || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ranlib || :

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib/go/%{gcc_version}/%{gcc_target_platform}
%ifnarch sparc64 ppc64
ln -sf %{multilib_32_arch}-%{_vendor}-%{_target_os} %{buildroot}%{_prefix}/lib/go/%{gcc_version}/%{gcc_target_platform}
%endif
%endif
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib64/go/%{gcc_version}/%{gcc_target_platform}
%endif
%endif
%endif

%if %{build_java}
mkdir -p %{buildroot}%{_prefix}/share/java/gcj-endorsed \
	 %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
chmod 755 %{buildroot}%{_prefix}/share/java/gcj-endorsed \
	  %{buildroot}%{_prefix}/%{_lib}/gcj-%{version} \
	  %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
touch %{buildroot}%{_prefix}/%{_lib}/gcj-%{version}/classmap.db
%endif

rm -f %{buildroot}%{mandir}/man3/ffi*

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

%check
cd obj-%{gcc_target_platform}

%if %{build_java}
export PATH=`pwd`/../fastjar-%{fastjar_ver}/obj-%{gcc_target_platform}${PATH:+:$PATH}
%if !%{bootstrap_java}
export PATH=`pwd`/java_hacks${PATH:+:$PATH}
%endif
%endif

# run the tests.
make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
echo ====================TESTING=========================
( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%clean
rm -rf %{buildroot}

%post
if [ -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%preun
if [ $1 = 0 -a -f %{_infodir}/gcc.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcc.info.gz || :
fi

%post -n cpp
if [ -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%preun -n cpp
if [ $1 = 0 -a -f %{_infodir}/cpp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cpp.info.gz || :
fi

%post gfortran
if [ -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%preun gfortran
if [ $1 = 0 -a -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%post java
if [ -f %{_infodir}/gcj.info.gz ]; then
/sbin/install-info \
  --info-dir=%{_infodir} %{_infodir}/gcj.info.gz || :
fi

%preun java
if [ $1 = 0 -a -f %{_infodir}/gcj.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gcj.info.gz || :
fi

%post gnat
if [ -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

%preun gnat
if [ $1 = 0 -a -f %{_infodir}/gnat_rm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_rm.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat_ugn.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gnat-style.info.gz || :
fi

# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%postun -n libgcc -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%post -n libstdc++ -p /sbin/ldconfig

%postun -n libstdc++ -p /sbin/ldconfig

%post -n libobjc -p /sbin/ldconfig

%postun -n libobjc -p /sbin/ldconfig

%post -n libgcj
/sbin/ldconfig
if [ -f %{_infodir}/cp-tools.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/cp-tools.info.gz || :
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz || :
fi

%preun -n libgcj
if [ $1 = 0 -a -f %{_infodir}/cp-tools.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/cp-tools.info.gz || :
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/fastjar.info.gz || :
fi

%postun -n libgcj -p /sbin/ldconfig

%post -n libgfortran -p /sbin/ldconfig

%postun -n libgfortran -p /sbin/ldconfig

%post -n libgnat -p /sbin/ldconfig

%postun -n libgnat -p /sbin/ldconfig

%post -n libgomp
/sbin/ldconfig
if [ -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%preun -n libgomp
if [ $1 = 0 -a -f %{_infodir}/libgomp.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgomp.info.gz || :
fi

%postun -n libgomp -p /sbin/ldconfig

%post -n libmudflap -p /sbin/ldconfig

%postun -n libmudflap -p /sbin/ldconfig

%post -n libquadmath
/sbin/ldconfig
if [ -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%preun -n libquadmath
if [ $1 = 0 -a -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%postun -n libquadmath -p /sbin/ldconfig

%post -n libitm
/sbin/ldconfig
if [ -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%preun -n libitm
if [ $1 = 0 -a -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%postun -n libitm -p /sbin/ldconfig

%post -n libgo -p /sbin/ldconfig

%postun -n libgo -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/gcc-ar
%{_prefix}/bin/gcc-nm
%{_prefix}/bin/gcc-ranlib
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/liblto_plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdnoreturn.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia64intrin.h
%endif
%ifarch ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spe.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/paired.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/vec_types.h
%endif
%ifarch %{arm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%endif
%ifarch sparc sparcv9 sparc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/visintrin.h
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.spec
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmudflapth.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.so
%endif
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmudflapth.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.so
%endif
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
%endif
%endif
%dir %{_prefix}/libexec/getconf
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* gcc/COPYING* COPYING.RUNTIME

%files -n cpp -f cpplib.lang
%defattr(-,root,root,-)
%{_prefix}/lib/cpp
%{_prefix}/bin/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1

%files -n libgcc
%defattr(-,root,root,-)
/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
/%{_lib}/libgcc_s.so.1
%doc gcc/COPYING* COPYING.RUNTIME

%files c++
%defattr(-,root,root,-)
%{_prefix}/bin/%{gcc_target_platform}-*++
%{_prefix}/bin/g++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libstdc++.so.6*
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%dir %{_prefix}/share/gcc-%{gcc_version}
%dir %{_prefix}/share/gcc-%{gcc_version}/python
%{_prefix}/share/gcc-%{gcc_version}/python/libstdcxx

%files -n libstdc++-devel
%defattr(-,root,root,-)
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[^gjos]*
%{_prefix}/include/c++/%{gcc_version}/os*
%{_prefix}/include/c++/%{gcc_version}/s[^u]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libsupc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%defattr(-,root,root)
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%files objc
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libobjc.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%defattr(-,root,root,-)
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1objplus

%files -n libobjc
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libobjc.so.4*

%files gfortran
%defattr(-,root,root,-)
%{_prefix}/bin/gfortran
%{_prefix}/bin/f95
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib_kinds.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcaf_single.a
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortranbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.so
%endif
%doc rpm.doc/gfortran/*

%files -n libgfortran
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgfortran.so.3*

%files -n libgfortran-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgfortran.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgfortran.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%endif

%if %{build_java}
%files java
%defattr(-,root,root,-)
%{_prefix}/bin/gcj
%{_prefix}/bin/gjavah
%{_prefix}/bin/gcjh
%{_prefix}/bin/jcf-dump
%{_mandir}/man1/gcj.1*
%{_mandir}/man1/jcf-dump.1*
%{_mandir}/man1/gjavah.1*
%{_mandir}/man1/gcjh.1*
%{_infodir}/gcj*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ecj1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/jvgenmain
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj-tools.so
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgij.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgij.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj-tools.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcj_bc.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgij.so
%endif
%doc rpm.doc/changelogs/gcc/java/ChangeLog*

%files -n libgcj
%defattr(-,root,root,-)
%{_prefix}/bin/jv-convert
%{_prefix}/bin/gij
%{_prefix}/bin/gjar
%{_prefix}/bin/fastjar
%{_prefix}/bin/gnative2ascii
%{_prefix}/bin/grepjar
%{_prefix}/bin/grmic
%{_prefix}/bin/grmid
%{_prefix}/bin/grmiregistry
%{_prefix}/bin/gtnameserv
%{_prefix}/bin/gkeytool
%{_prefix}/bin/gorbd
%{_prefix}/bin/gserialver
%{_prefix}/bin/gcj-dbtool
%{_prefix}/bin/gjarsigner
%{_mandir}/man1/fastjar.1*
%{_mandir}/man1/grepjar.1*
%{_mandir}/man1/gjar.1*
%{_mandir}/man1/gjarsigner.1*
%{_mandir}/man1/jv-convert.1*
%{_mandir}/man1/gij.1*
%{_mandir}/man1/gnative2ascii.1*
%{_mandir}/man1/grmic.1*
%{_mandir}/man1/grmiregistry.1*
%{_mandir}/man1/gcj-dbtool.1*
%{_mandir}/man1/gkeytool.1*
%{_mandir}/man1/gorbd.1*
%{_mandir}/man1/grmid.1*
%{_mandir}/man1/gserialver.1*
%{_mandir}/man1/gtnameserv.1*
%{_infodir}/fastjar.info*
%{_infodir}/cp-tools.info*
%{_prefix}/%{_lib}/libgcj.so.*
%{_prefix}/%{_lib}/libgcj-tools.so.*
%{_prefix}/%{_lib}/libgcj_bc.so.*
%{_prefix}/%{_lib}/libgij.so.*
%dir %{_prefix}/%{_lib}/gcj-%{version}
%{_prefix}/%{_lib}/gcj-%{version}/libgtkpeer.so
%{_prefix}/%{_lib}/gcj-%{version}/libgjsmalsa.so
%{_prefix}/%{_lib}/gcj-%{version}/libjawt.so
%{_prefix}/%{_lib}/gcj-%{version}/libjvm.so
%{_prefix}/%{_lib}/gcj-%{version}/libjavamath.so
%dir %{_prefix}/share/java
%{_prefix}/share/java/[^sl]*
%{_prefix}/share/java/libgcj-%{version}.jar
%dir %{_prefix}/%{_lib}/security
%config(noreplace) %{_prefix}/%{_lib}/security/classpath.security
%{_prefix}/%{_lib}/logging.properties
%dir %{_prefix}/%{_lib}/gcj-%{version}/classmap.db.d
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_prefix}/%{_lib}/gcj-%{version}/classmap.db

%files -n libgcj-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/gcj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jawt_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jni_md.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/jvmpi.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj.spec
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgcj_bc.so
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgcj_bc.so
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcj_bc.so
%endif
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[gj]*
%{_prefix}/include/c++/%{gcc_version}/org
%{_prefix}/include/c++/%{gcc_version}/sun
%{_prefix}/%{_lib}/pkgconfig/libgcj-*.pc
%doc rpm.doc/boehm-gc/* rpm.doc/fastjar/* rpm.doc/libffi/*
%doc rpm.doc/libjava/*

%files -n libgcj-src
%defattr(-,root,root,-)
%dir %{_prefix}/share/java
%{_prefix}/share/java/src*.zip
%{_prefix}/share/java/libgcj-tools-%{version}.jar
%endif

%if %{build_ada}
%files gnat
%defattr(-,root,root,-)
%{_prefix}/bin/gnat
%{_prefix}/bin/gnat[^i]*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/adalib
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/adalib
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnarl.a
%endif

%files -n libgnat-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/adalib/libgnarl.a
%endif
%endif

%files -n libgomp
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%files -n libmudflap
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libmudflap.so.0*
%{_prefix}/%{_lib}/libmudflapth.so.0*

%files -n libmudflap-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mf-runtime.h
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.so
%endif
%doc rpm.doc/changelogs/libmudflap/ChangeLog*

%files -n libmudflap-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libmudflapth.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libmudflapth.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflap.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmudflapth.a
%endif

%if %{build_libquadmath}
%files -n libquadmath
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libquadmath.so.0*
%{_infodir}/libquadmath.info*
%doc rpm.doc/libquadmath/COPYING*

%files -n libquadmath-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%doc rpm.doc/libquadmath/ChangeLog*

%files -n libquadmath-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libquadmath.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libquadmath.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%endif
%endif

%if %{build_libitm}
%files -n libitm
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*

%files -n libitm-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/itm.h
#%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/itm_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
%endif
%doc rpm.doc/libitm/ChangeLog*

%files -n libitm-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libitm.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libitm.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%endif
%endif

%if %{build_go}
%files go
%defattr(-,root,root,-)
%{_prefix}/bin/gccgo
%{_mandir}/man1/gccgo.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/go1
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgobegin.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgobegin.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgobegin.a
%endif
%doc rpm.doc/go/*

%files -n libgo
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgo.so.0*
%doc rpm.doc/libgo/*

%files -n libgo-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/%{_lib}/go
%dir %{_prefix}/%{_lib}/go/%{gcc_version}
%{_prefix}/%{_lib}/go/%{gcc_version}/%{gcc_target_platform}
%ifarch %{multilib_64_archs}
%ifnarch sparc64 ppc64
%dir %{_prefix}/lib/go
%dir %{_prefix}/lib/go/%{gcc_version}
%{_prefix}/lib/go/%{gcc_version}/%{gcc_target_platform}
%endif
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgobegin.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgobegin.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.so
%endif

%files -n libgo-static
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libgo.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libgo.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgo.a
%endif
%endif

%files plugin-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/plugin

%changelog
* Fri Nov  9 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-8
- update from the 4.7 branch
  - PRs fortran/54917, libstdc++/28811, libstdc++/54482, libstdc++/55028,
	libstdc++/55215, middle-end/55219, target/55204,
	tree-optimization/54986
- further debug info quality improvements
- fix reassociation (PR c++/55137)
- fix range test optimization with -fwrapv (PR tree-optimization/55236)
- add BuildRequires hostname (#875001)
- __cxa_vec_new[23] overflow checking (#875009)

* Mon Nov  5 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-7
- update from the 4.7 branch
  - PRs c++/54984, c++/54988, debug/54828, libstdc++/55047, libstdc++/55123,
	libstdc++/55169, middle-end/54945, rtl-optimization/53701,
	rtl-optimization/54870, target/53975, target/54892, target/55019,
	target/55175, tree-optimization/53708, tree-optimization/54146,
	tree-optimization/54877, tree-optimization/54902,
	tree-optimization/54920, tree-optimization/54985
- backported s390{,x} zEC12 enablement (#805114)
- backport of selected debug info quality improvements
  - PRs debug/54402, debug/54693, debug/54953, debug/54970, debug/54971
- optimize away overflow checking for new char[n]; and similar cases
  where n is multiplied by 1

* Mon Oct 15 2012 Jon Ciesla <limburgher@gmail.com> 4.7.2-6
- Provides: bundled(libiberty)

* Mon Oct 15 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-5
- update from the 4.7 branch
  - PRs fortran/54784, libfortran/54736, libstdc++/54861

* Tue Oct  9 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-4
- update from the 4.7 branch
  - PRs c++/54777, c++/54858, debug/53135, target/54741, target/54785,
	target/54854
- backport of selected debug info quality improvements (#851467)
  - PRs debug/48866, debug/52983, debug/53740, debug/53923, debug/54519,
	debug/54551

* Mon Oct  1 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-3
- update from the 4.7 branch
  - PRs target/54083, target/54703, target/54746, testsuite/54007
- backport operator new[] overflow checking (#850911, PR c++/19351)

* Fri Sep 21 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-2
- update from the 4.7 branch
  - PRs c/54103, c/54552, libstdc++/54102, middle-end/54638, other/43620

* Thu Sep 20 2012 Jakub Jelinek <jakub@redhat.com> 4.7.2-1
- update from the 4.7 branch
  - GCC 4.7.2 release
  - PRs c++/53661, lto/54312, tree-optimization/54563

* Thu Sep 13 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-8
- update from the 4.7 branch
  - PRs c++/53836, c++/53839, c++/54086, c++/54197, c++/54253, c++/54341,
	c++/54506, c++/54511, c/54363, c/54428, c/54559, debug/54534,
	driver/54335, fortran/53306, fortran/54208, fortran/54225,
	fortran/54435, fortran/54443, fortran/54556, gcov-profile/54487,
	libstdc++/54172, libstdc++/54185, libstdc++/54297, libstdc++/54351,
	libstdc++/54376, libstdc++/54388, lto/53572, middle-end/53667,
	middle-end/53992, middle-end/54146, middle-end/54486,
	middle-end/54515, rtl-optimization/54088, rtl-optimization/54369,
	rtl-optimization/54455, target/45070, target/46254, target/54212,
	target/54220, target/54252, target/54436, target/54461,
	target/54476, target/54536, tree-opt/54494,
	tree-optimization/53922, tree-optimization/54498
- fix up _mm_f{,n}m{add,sub}_s{s,d} fma intrinsics (PR target/54564)

* Mon Aug 13 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-7
- update from the 4.7 branch
  - PR rtl-optimization/53942
- backport -mrdseed, -mprfchw and -madx support

* Fri Aug 10 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-6
- update from the 4.7 branch
  - PRs libstdc++/54036, libstdc++/54075, rtl-optimization/54157,
	target/33135, target/52530

* Fri Jul 20 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-5
- update from the 4.7 branch
  - PRs c++/54026, middle-end/54017, rtl-optimization/52250, target/53877,
	target/54029
  - fix endless hang of C++ compiler (#841814, PR c++/54038)

* Wed Jul 18 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-4
- update from the 4.7 branch
  - PRs c++/53549, c++/53989, c++/53995, libstdc++/53978

* Mon Jul 16 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-3
- update from the 4.7 branch
  - C++11 ABI change - std::list and std::pair in C++11 ABI compatible again
    with C++03, but ABI incompatible with C++11 in GCC 4.7.[01]
  - PRs bootstrap/52947, c++/53733, c++/53816, c++/53821, c++/53826,
	c++/53882, c++/53953, fortran/53732, libstdc++/49561,
	libstdc++/53578, libstdc++/53657, libstdc++/53830, libstdc++/53872,
	middle-end/38474, middle-end/50708, middle-end/52621,
	middle-end/52786, middle-end/53433, rtl-optimization/53908,
	target/53110, target/53811, target/53853, target/53961,
	testsuite/20771, tree-optimization/53693
- backport -mrtm and -mhle support (PRs target/53194, target/53201,
  target/53315)
- fix up ppc32 *movdi_internal32 pattern (#837630)
- apply ld.so arm hfp patch on all arm arches
- enable go support on arm

* Fri Jul 13 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-2
- change ld.so pathname for arm hfp for F18+

* Fri Jun 29 2012 Jakub Jelinek <jakub@redhat.com> 4.7.1-1
- update from the 4.7 branch
  - GCC 4.7.1 release
  - PRs ada/53592, c++/51214, c++/52637, c++/52841, c++/52988, c++/53202,
	c++/53305, c++/53498, c++/53524, c++/53594, c++/53599, c++/53602,
	c++/53616, c++/53651, c++/53752, debug/53682, fortran/50619,
	fortran/53597, fortran/53685, fortran/53691, gcov-profile/53744,
	libgomp/52993, libstdc++/53270, libstdc++/53678, middle-end/53470,
	middle-end/53580, middle-end/53790, preprocessor/37215,
	rtl-optimization/53589, rtl-optimization/53700, target/52908,
	target/53559, target/53595, target/53621, target/53759,
	tree-optimization/52558

* Mon Jun  4 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-7
- update from the 4.7 branch
  - PRs ada/53517, c++/52725, c++/52905, c++/52973, c++/53137, c++/53220,
	c++/53356, c++/53484, c++/53491, c++/53500, c++/53503,
	fortran/53521, libstdc++/52007, middle-end/47530, middle-end/48124,
	middle-end/48493, middle-end/52080, middle-end/52097,
	middle-end/52979, middle-end/53008, middle-end/53471,
	middle-end/53501, rtl-optimization/52528, rtl-optimization/53519,
	target/46261, target/52642, target/52667, tree-optimization/53438,
	tree-optimization/53505, tree-optimization/53516,
	tree-optimization/53550

* Fri May 25 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-6
- update from the 4.7 branch
  - PRs ada/52362, ada/52494, bootstrap/53183, c++/53209, c++/53301,
	c/53418, debug/52727, fortran/53310, fortran/53389, libstdc++/52700,
	middle-end/51071, middle-end/52584, middle-end/53460,
	rtl-optimization/52804, target/46098, target/53256, target/53272,
	target/53358, target/53385, target/53416, target/53435, target/53448,
	tree-optimization/53364, tree-optimization/53366,
	tree-optimization/53408, tree-optimization/53409,
	tree-optimization/53410, tree-optimization/53436,
	tree-optimization/53465

* Mon May  7 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-5
- update from the 4.7 branch
  - PRs fortran/53111, fortran/53255, target/48496, target/52999,
	target/53228, tree-optimization/52633, tree-optimization/52870,
	tree-optimization/53195, tree-optimization/53239

* Fri May  4 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-4
- update from the 4.7 branch
  - PRs c++/53186, fortran/52864, libstdc++/53193, lto/52605,
	target/52684, target/53199, tree-optimization/53144
  - fix up gcc-ar, gcc-nm and gcc-ranlib (#818311, PR plugins/53126)

* Wed May  2 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-3
- update from the 4.7 branch
  - PRs bootstrap/52840, c++/38543, c++/50303, c++/50830, c++/53003,
	c/51527, c/52880, c/53060, fortran/53148, libstdc++/52689,
	libstdc++/52839, libstdc++/53027, libstdc++/53067, libstdc++/53115,
	middle-end/52939, middle-end/52999, middle-end/53084,
	middle-end/53136, rtl-optimization/53160, target/52932,
	target/53020, target/53033, target/53065, target/53120,
	target/53138, testsuite/52641, testsuite/53046,
	tree-optimization/53085, tree-optimization/53163,
	tree-optimizations/52891
- fix ARM SELECT_CC_MODE ICE (#817086, PR target/53187)
- fix predictive commoning debug info ICE (PR debug/53174)

* Mon Apr 16 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-2
- update from the 4.7 branch
  - PRs c++/52292, c++/52380, c++/52465, c++/52487, c++/52596, c++/52671,
	c++/52672, c++/52685, c++/52718, c++/52743, c++/52746, c++/52759,
	c++/52796, c++/52824, c++/52906, c/52682, c/52862, fortran/52452,
	fortran/52668, fortran/52893, libgfortran/52758, libitm/52854,
	libstdc++/52433, libstdc++/52476, libstdc++/52540, libstdc++/52591,
	libstdc++/52699, libstdc++/52799, libstdc++/52822, libstdc++/52924,
	libstdc++/52942, middle-end/51893, middle-end/52493,
	middle-end/52547, middle-end/52580, middle-end/52640,
	middle-end/52691, middle-end/52693, middle-end/52720,
	middle-end/52750, middle-end/52894, other/52545,
	rtl-optimization/52543, target/48596, target/48806, target/50310,
	target/52461, target/52484, target/52488, target/52496, target/52499,
	target/52505, target/52506, target/52507, target/52508, target/52610,
	target/52692, target/52698, target/52717, target/52736, target/52737,
	target/52775, tree-optimization/52406, tree-optimization/52678,
	tree-optimization/52701, tree-optimization/52754,
	tree-optimization/52835, tree-optimization/52943,
	tree-optimization/52969
- avoid duplicate pointers in C++ debug info due to injected class name
  (PR debug/45088)
- libjava locale fixes (#712013)

* Thu Mar 22 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-1
- update from the 4.7 branch
  - GCC 25th Anniversary 4.7.0 release
  - fix up new auto mangling

* Thu Mar 15 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.20
- update from the 4.7 branch
  - PRs fortran/52469, libitm/52526, libstdc++/52456, target/52450
  - fix __builtin_ir{ound,int}{,f,l} expansion (#803689, PR middle-end/52592)
  - fix up devirtualization (#802731, PR c++/52582)
- fix up user defined literal operator"" lookup (PR c++/52521)
- avoid false positive -Wunused-but-set-* warnings with __builtin_shuffle
  (PR c/52577)

* Thu Mar  8 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.19
- update from trunk and the 4.7 branch
  - PRs libstdc++/51785, middle-end/52419, middle-end/52443,
	middle-end/52463, rtl-optimization/52417, target/49939,
	target/51417, target/52408, target/52437, target/52481,
	testsuite/52297, tree-opt/52242, tree-optimization/52424,
	tree-optimization/52429, tree-optimization/52445
  - fix up mangling of operator"" (PR c++/52521)
- decrease size of .debug_ranges by ~ 20% (PR debug/51902)
- add support for demangling operator""
- package %{_prefix}/bin/gcc-{ar,nm,ranlib} binaries for LTO

* Wed Feb 29 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.18
- update from trunk
  - PRs boehm-gc/48299, bootstrap/52397, bootstrap/52414, fortran/52386,
	libstdc++/52191, lto/52400, middle-end/51752, target/49448,
	target/51534, target/52148, target/52407, tree-optimization/52395,
	tree-optimization/52402, tree-optimization/53207
  - fix bootstrap on ppc*/arm/s390*

* Mon Feb 27 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.17
- update from trunk
  - PRs boehm-gc/52179, libffi/52223, libstdc++/52188, middle-end/52355,
	middle-end/52361, target/49263, target/49461, target/50580,
	target/52352, target/52375, target/52390, testsuite/52201,
	tree-optimization/52376

* Fri Feb 24 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.16
- update from trunk
  - fix vtable for std::num_get<char, std::istreambuf_iterator<char,
    std::char_traits<char> > > and vtable for std::num_get<wchar_t,
    std::istreambuf_iterator<wchar_t, std::char_traits<wchar_t> > >
    ABI breakage
  - PR bootstrap/52287

* Thu Feb 23 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.15
- update from trunk
  - PRs c/52290, fortran/52335, go/52349, libstdc++/50349, lto/50616,
	middle-end/52329, rtl-optimization/50063, target/18145, target/52330,
	tree-optimization/52019
- disable go on arm again, still not ready there

* Tue Feb 21 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.14
- update from trunk
  - PRs c++/51415, c++/52126, c++/52248, c++/52312, fortran/52295,
	libstdc++/47058, libstdc++/52189, libstdc++/52241, libstdc++/52300,
	libstdc++/52309, libstdc++/52317, middle-end/52141, middle-end/52314,
	rtl-optimization/52208, target/50166, target/51753, target/52137,
	target/52238, target/52294, testsuite/52229, translation/52232,
	translation/52234, translation/52245, translation/52246,
	translation/52262, translation/52273, tree-optimization/52285,
	tree-optimization/52286, tree-optimization/52298,
	tree-optimization/52318, tree-optimization/52324

* Thu Feb 16 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.13
- update from trunk
  - PRs boehm-gc/48514, bootstrap/52172, c++/39055, c++/51910, c++/52215,
	c/52181, c/52190, debug/52165, debug/52260, driver/48524,
	fortran/32380, fortran/52151, go/48411, go/51874, libffi/52221,
	libitm/52042, libitm/52220, libstdc++/51368, lto/52178,
	middle-end/48600, middle-end/51867, middle-end/51929,
	middle-end/52140, middle-end/52142, middle-end/52177,
	middle-end/52209, middle-end/52214, middle-end/52230,
	rtl-optimization/52175, target/51921, target/52146, target/52199,
	target/52205, target/52261, testsuite/50076, translation/52193,
	translation/52211, translation/52264, tree-optimization/50031,
	tree-optimization/50561, tree-optimization/52210,
	tree-optimization/52244, tree-optimization/52255
  - fix asm goto handling in templates (#790221, PR c++/52247)
- reenable go on ppc/ppc64/s390/s390x/arm

* Wed Feb  8 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.12
- update from trunk
  - PRs c++/52035, fortran/51514, gcov-profile/52150, libstdc++/51296,
	libstdc++/51906, middle-end/24306, middle-end/51994,
	middle-end/52074, rtl-optimization/52139, rtl-optimization/52170,
	target/40068, target/52152, target/52154, target/52155,
	tree-optimization/46886
  - fix up build on ppc*
  - don't look for lto plugin/lto-wrapper if -E/-S/-c or in cpp
- move liblto_plugin.so* back into gcc subpackage

* Mon Feb  6 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.11
- update from trunk
  - PRs bootstrap/52039, bootstrap/52041, bootstrap/52058, c++/48680,
	c++/51327, c++/51370, c++/51852, c++/52043, c++/52088, c/52118,
	debug/52001, debug/52027, debug/52048, fortran/32373, fortran/41587,
	fortran/41600, fortran/46356, fortran/48705, fortran/48847,
	fortran/51754, fortran/51808, fortran/51870, fortran/51943,
	fortran/51946, fortran/51953, fortran/51958, fortran/51970,
	fortran/51972, fortran/51977, fortran/52012, fortran/52013,
	fortran/52016, fortran/52022, fortran/52024, fortran/52029,
	fortran/52038, fortran/52093, fortran/52102, go/47656, go/48501,
	libitm/51822, libjava/48512, libstdc++/49445, libstdc++/51649,
	libstdc++/51795, libstdc++/51798, libstdc++/51811, libstdc++/51956,
	libstdc++/52068, libstdc++/52104, libstdc++/52119, libstdc++/52128,
	middle-end/43967, middle-end/47982, middle-end/48071,
	middle-end/51389, middle-end/51959, middle-end/51998,
	middle-end/52047, rtl-optimization/49800, rtl-optimization/51374,
	rtl-optimization/51978, rtl-optimization/52092,
	rtl-optimization/52095, rtl-optimization/52113, target/51500,
	target/51835, target/51871, target/51920, target/51974, target/52079,
	target/52107, target/52125, target/52129, testsuite/51875,
	testsuite/52011, tree-optimization/48794, tree-optimization/50444,
	tree-optimization/50955, tree-optimization/50969,
	tree-optimization/51528, tree-optimization/51990,
	tree-optimization/52020, tree-optimization/52028,
	tree-optimization/52045, tree-optimization/52046,
	tree-optimization/52073, tree-optimization/52091,
	tree-optimization/52115
  - fix i?86 mem += reg; mem cmp 0 8-bit peephole2 (#786570, PR target/52086)
  - fix fortran ICE on elemental call (#785433, PR fortran/52059)
- fix up /lib/cpp symlink for UsrMove (#787460)
- move LTO plugin into cpp subpackage (#787345)
- fix debug ICE with i387 reg-stack (#787518, PR debug/52132)
- fix ARM combine bug (PR rtl-optimization/52060)
- fix a DWARF4 .debug_types DIE cloning bug (PR debug/51950)

* Thu Jan 26 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.10
- update from trunk
  - PRs bootstrap/51985, c++/51223, c++/51812, c++/51917, c++/51928,
	c++/51930, c++/51973, c++/51992, driver/47249, fortran/51966,
	fortran/51995, libstdc++/49829, lto/51698, middle-end/45678,
	middle-end/51986, rtl-optimization/48308, rtl-optimization/48374
  - fix data-ref handling of non-volatile inline asms (#784242,
    PR tree-optimization/51987)
- fix ARM ICE with invalid peephole (#784748, PR target/52006)

* Mon Jan 23 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.9
- update from trunk
  - PRs ada/46192, c++/51344, c++/51398, c++/51402, c++/51832, c++/51919,
	c++/51922, debug/45682, fortran/50556, fortran/51056, fortran/51904,
	fortran/51913, fortran/51948, libgcj/23182, libgfortran/51899,
	libitm/51830, libstdc++/50982, lto/51916, middle-end/45416,
	rtl-optimization/40761, rtl-optimization/51924, target/47096,
	target/49868, target/50313, target/50887, target/51106, target/51819,
	target/51900, target/51915, target/51931, target/51934,
	testsuite/51941, tree-optimization/51895, tree-optimization/51903,
	tree-optimization/51914, tree-optimization/51949
  - fix REE pass (#783481, PR rtl-optimization/51933)
  - further overload fixes with using decls (#783586, PR c++/51925)
- fix ICE during expansion with BLKmode MEM_REF (#782868, PR middle-end/51895)
- fix ppc64 profiledbootstrap (PR target/51957)
- revert broken stack layout change (PR tree-optimization/46590)
- fix ARM ICE on neon insn splitting (PR target/51968)

* Thu Jan 19 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.8
- update from trunk
  - PRs bootstrap/50237, c++/51225, c++/51889, fortran/48426, fortran/51634,
	go/50656, libmudflap/40778, libstdc++/51845, libstdc++/51866,
	lto/51280, middle-end/51192, rtl-optimization/48496,
	rtl-optimization/51505, tree-optimization/37997,
	tree-optimization/46590
- fix a reload bug on s390 (#773565, PR rtl-optimization/51856)

* Tue Jan 17 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.7
- update from trunk
  - PRs bootstrap/51860, c++/14179, c++/20681, c++/50012, c++/51403,
	c++/51620, c++/51633, c++/51714, c++/51777, c++/51813, c++/51827,
	c++/51854, c++/51868, c/12245, fortran/36755, fortran/48351,
	fortran/51800, fortran/51809, fortran/51816, fortran/51842,
	fortran/51869, libitm/51173, libitm/51855, middle-end/51782,
	middle-end/8081, other/51165, rtl-optimization/51821, target/47852,
	target/50925, target/51756, tree-optimization/51865
  - fix up ppc64 bootstrap with -mminimal-toc (#773040, PR bootstrap/51872)
  - fix up -ftree-tail-merge (#782231, PR tree-optimization/51877)
- package up arm and sparc specific headers (#781765)
- enable libitm and disable go on ppc/ppc64
- fix up big-endian libstdc++ miscompilation (PR middle-end/50325)
- fix up arm neon vectorization ICEs (PR target/51876)

* Thu Jan 12 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.6
- update from trunk
  - PRs ada/41929, bootstrap/51705, bootstrap/51796, c++/47450,
	c++/48051, c++/50855, c++/51322, c++/51433, c++/51565,
	c++/51613, c++/51614, c++/51818, c++/6057, debug/51471,
	fortran/51057, fortran/51578, fortran/51616, fortran/51652,
	fortran/51758, fortran/51791, fortran/51792, gcov-profile/50127,
	gcov-profile/51715, gcov-profile/51717, libstdc++/51673,
	middle-end/51516, middle-end/51806, preprocessor/33919,
	preprocessor/51776, rtl-optimization/51271, target/47333,
	rarget/49868, testsuite/51655, tree-optimization/49642,
	tree-optimization/50913, tree-optimization/51600,
	tree-optimization/51680, tree-optimization/51694,
	tree-optimization/51759, tree-optimization/51775,
	tree-optimization/51799, tree-optimization/51801

* Fri Jan  6 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.5
- update from trunk
  - PRs c++/51541, fortran/48946, libstdc++/51504, lto/51774,
	rtl-optimization/51771, target/51681, tree-optimization/51315
- disable go on s390{,x}
- disable profiledbootstrap on arm and sparc* for now

* Thu Jan  5 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.4
- update from trunk
  - PRs bootstrap/51072, bootstrap/51648, debug/51746, debug/51762,
	lto/41576, lto/50490, middle-end/44777, middle-end/49710,
	middle-end/51472, middle-end/51761, middle-end/51764,
	middle-end/51768, other/51171, rtl-optimization/51767,
	tree-optimization/51624, tree-optimization/51760
- disable go on arm (#771482)
- enable profiledbootstrap

* Wed Jan  4 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.3
- update from trunk
  - PRs bootstrap/51006, bootstrap/51734, c++/29273, c++/51064, c++/51738,
	debug/51695, fortran/49693, fortran/50981, middle-end/51696,
	middle-end/51750, other/51163, other/51164, tree-optimization/49651
- fix up libitm.so.1

* Tue Jan  3 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.2
- update from trunk
  - PRs bootstrap/51686, bootstrap/51725, c++/15867, c++/16603, c++/20140,
	c++/23211, c++/51316, c++/51379, c++/51397, c++/51462, c++/51507,
	c++/51547, c++/51666, c++/51669, c++/51675, c++/51723, debug/51650,
	driver/48306, fortran/46262, fortran/46328, fortran/51052,
	fortran/51502, fortran/51529, fortran/51682, libfortran/51646,
	libgcj/49193, libstdc++/48362, libstdc++/49204, libstdc++/51608,
	libstdc++/51701, libstdc++/51711, lto/51650, middle-end/48641,
	middle-end/51200, middle-end/51212, middle-end/51252,
	middle-end/51730, other/51679, pch/51722, rtl-optimization/50396,
	rtl-optimization/51069, rtl-optimization/51667, target/27468,
	target/47643, target/51345, target/51552, target/51623, target/51643,
	target/51729, testsuite/50722, testsuite/51645, testsuite/51702,
	tree-optimization/43491, tree-optimization/51070,
	tree-optimization/51269, tree-optimization/51683,
	tree-optimization/51684, tree-optimization/51692,
	tree-optimization/51704, tree-optimization/51719

* Wed Dec 21 2011 Jakub Jelinek <jakub@redhat.com> 4.7.0-0.1
- new package
