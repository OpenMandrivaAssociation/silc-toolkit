%define api_version 1.1
%define silcmajor 2
%define clientmajor 3
%define silclibname %mklibname silc %{api_version} %{silcmajor}
%define silclibname_orig %mklibname silc %{api_version}
%define clientlibname %mklibname silcclient %{api_version} %{clientmajor}
%define clientlibname_orig %mklibname silcclient %{api_version}

Summary:	SILC toolkit
Name:		silc-toolkit
Version:	1.1.9
Release:	%mkrel 1
License:	GPLv2
Group:		Networking/Chat
URL:		http://silcnet.org/
Source0:	http://silcnet.org/download/toolkit/sources/%{name}-%{version}.tar.bz2
Patch1:		silc-toolkit-1.1.5-libidn.patch
Patch2:		silc-toolkit-1.1.5-docinst.patch
Requires:	%{silclibname} = %{version}-%{release}
BuildRequires:	libidn-devel
BuildRequires:	libtool
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ncurses-devel
BuildRequires:	nasm
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as IRC.
Other than that they are nothing alike.  Major differences are that SILC
is secure what IRC is not in any way.  The network model is also entirely
different compared to IRC.

This package provides development related files for any application that
has SILC support.

%package -n %{silclibname}
Summary:	SILC library
Group:		System/Libraries
Provides:	%{silclibname_orig} = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%mklibname silc- 1.0 %{silcmajor}
Obsoletes:	%mklibname silc- 1.1 2

%description -n %{silclibname}
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as IRC.
Other than that they are nothing alike.  Major differences are that SILC
is secure what IRC is not in any way.  The network model is also entirely
different compared to IRC.

This is the library implementing SILC protocol, including core components,
cryptographic algorithms and utility functions.

%package -n %{clientlibname}
Summary:	SILC client library
Group:		System/Libraries
Provides:	%{clientlibname_orig} = %{version}-%{release}
Obsoletes:	%{_lib}silc-client1
Provides:	%{_lib}silc-client1 = %{version}-%{release}
Obsoletes:	%mklibname silcclient- 1.0 1
Obsoletes:	%mklibname silcclient- 1.1 2

%description -n %{clientlibname}
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as IRC.
Other than that they are nothing alike.  Major differences are that SILC
is secure what IRC is not in any way.  The network model is also entirely
different compared to IRC.

The SILC Client library. Implementation of the SILC Client without
the user interface.  The library provides an interface for user
interface designers.

%package devel
Summary:	SILC toolkit
Group:		Development/Other
# rpmlint wants that, so be it
Requires:	%{name} = %{version}-%{release}
Provides:	%{clientlibname_orig}-devel = %{version}-%{release}
Requires:	%{clientlibname} = %{version}-%{release}
Provides:	%{silclibname_orig}-devel = %{version}-%{release}
Requires:	%{silclibname} = %{version}-%{release}
Obsoletes:	%{_lib}client1-devel
Provides:	%{_lib}client1-devel = %{version}-%{release}
Obsoletes:	%{_lib}silc-client1-devel
Provides:	%{_lib}silc-client1-devel = %{version}-%{release}

%description devel
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as IRC.
Other than that they are nothing alike.  Major differences are that SILC
is secure what IRC is not in any way.  The network model is also entirely
different compared to IRC.

This package contains all development related files for developing or 
compiling applications using SILC protocol.

%prep
%setup -q
%patch1 -p1 -b .libidn
%patch2 -p1 -b .docinst

find -type f | xargs file | grep -v script | cut -d: -f1 | xargs chmod -x

%build
autoreconf
%define _disable_ld_no_undefined 1

%configure2_5x \
	--with-simdir=%{_libdir}/silc/modules \
	--enable-ipv6 \
	--enable-shared \
	--includedir=%{_includedir}/silc

# parallel will succeed but produce broken library
%make -j1 LIBTOOL=%_bindir/libtool

%install
rm -rf %{buildroot}

%makeinstall_std LIBTOOL=%_bindir/libtool

%if %mdkversion < 200900
%post -n %{silclibname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{silclibname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{clientlibname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{clientlibname} -p /sbin/ldconfig
%endif

%triggerpostun -- libsilc-client1 <= 1.0.1-2mdk
tempfile=`mktemp /etc/ld.so.conf.XXXXXX` || exit $?
grep -v "^%{_libdir}/silc$" /etc/ld.so.conf > $tempfile && cat $tempfile > /etc/ld.so.conf
rm -f $tempfile

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README* ChangeLog TODO
%{_libdir}/silc

%files -n %{silclibname}
%defattr(-,root,root)
%{_libdir}/libsilc-%{api_version}.so.%{silcmajor}*

%files -n %{clientlibname}
%defattr(-,root,root)
%{_libdir}/libsilcclient-%{api_version}.so.%{clientmajor}*

%files devel
%defattr(-,root,root)
%doc %{_docdir}/%{name}
%{_includedir}/silc
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*.pc
