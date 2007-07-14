%define version 1.1.2
%define release %mkrel 1

%define api_version 1.1
%define silcmajor 2
%define clientmajor 2
%define silclibname %mklibname silc- %{api_version} %{silcmajor}
%define silclibname_orig %mklibname silc- %{api_version}
%define clientlibname %mklibname silcclient- %{api_version} %{clientmajor}
%define clientlibname_orig %mklibname silcclient- %{api_version}

%define silclibdir %{_libdir}/silc

Summary:	SILC toolkit
Name:		silc-toolkit
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		Networking/Chat
URL:		http://silcnet.org/
Source:		http://silcnet.org/download/toolkit/sources/%{name}-%{version}.tar.bz2
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
#BuildRequires: perl-devel
#BuildRequires: glib2-devel
#BuildRequires: libncurses-devel
Requires:	%{silclibname} = %{version}

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


%package	-n %{silclibname}
Summary:	SILC library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	%{silclibname_orig} = %{version}-%{release}
Obsoletes:	%{_lib}client1
Provides:	%{_lib}client1 = %{version}-%{release}
Requires:	%{name} = %{version}
Obsoletes:	%mklibname silc- 1.0 %{silcmajor}

%description	-n %{silclibname}
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

%package	-n %{clientlibname}
Summary:	SILC client library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Provides:	%{clientlibname_orig} = %{version}-%{release}
Obsoletes:	%{_lib}silc-client1
Provides:	%{_lib}silc-client1 = %{version}-%{release}
Obsoletes:	%mklibname silcclient- 1.0 1

%description	-n %{clientlibname}
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

%package	devel
Summary:	SILC toolkit
Group:		Development/Other
# rpmlint wants that, so be it
Requires:	%{name} = %{version}
Provides:	%{clientlibname_orig}-devel = %{version}-%{release}
Requires:	%{clientlibname} = %{version}
Provides:	%{silclibname_orig}-devel = %{version}-%{release}
Requires:	%{silclibname} = %{version}
Obsoletes:	%{_lib}client1-devel
Provides:	%{_lib}client1-devel = %{version}-%{release}
Obsoletes:	%{_lib}silc-client1-devel
Provides:	%{_lib}silc-client1-devel = %{version}-%{release}

%description	devel
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

%package -n perl-silc
Group: Development/Perl
Summary: Perl part of the SILC toolkit

%description -n perl-silc
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as IRC.
Other than that they are nothing alike.  Major differences are that SILC
is secure what IRC is not in any way.  The network model is also entirely
different compared to IRC.

This contains the perl modules that come with SILC.


%prep
%setup -q

find -type f | xargs file | grep -v script | cut -d: -f1 | xargs chmod -x

%build
%configure2_5x \
	--with-logsdir=%{_var}/log/silc \
	--with-simdir=%{silclibdir}/modules \
	--with-silcd-pid-file=%{_var}/run/silcd.pid \
	--enable-ipv6 \
	--enable-shared \
	--with-perl=module \
	--with-perl-lib=vendor \
	--without-silcd \
	--without-irssi \
	--includedir=%{_includedir}/silc

# parallel will succeed but produce broken library
make

%install
rm -rf %{buildroot}
%makeinstall_std
# mv %buildroot%buildroot%_datadir/silc/help %buildroot%_datadir/silc/

# let rpm macros handle documents
# rm -rf package-doc
# mv %{buildroot}%{_prefix}/doc package-doc
# mv %{buildroot}%buildroot%{_prefix}/doc/* package-doc
# mkdir -p package-doc/tutorial
# install -m 644 tutorial/mybot/{README,mybot.c} package-doc/tutorial/

# remove files not bundled
# rm -rf %{buildroot}%{_sysconfdir}
# rm -rf %{buildroot}%{_mandir}

# multiarch
# multiarch_includes %{buildroot}%{_includedir}/silc/silcincludes.h


%post -n %{silclibname} -p /sbin/ldconfig
%postun -n %{silclibname} -p /sbin/ldconfig
%post -n %{clientlibname} -p /sbin/ldconfig
%postun -n %{clientlibname} -p /sbin/ldconfig

%triggerpostun -- libsilc-client1 <= 1.0.1-2mdk
tempfile=`mktemp /etc/ld.so.conf.XXXXXX` || exit $?
grep -v "^%{_libdir}/silc$" /etc/ld.so.conf > $tempfile && cat $tempfile > /etc/ld.so.conf
rm -f $tempfile

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
#%_bindir/silc
%{_libdir}/silc
#%_datadir/silc
#%_sbindir/silcd

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
# multiarch %{multiarch_includedir}/silc/*.h
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*.pc

%files -n perl-silc
%defattr(-,root,root)
#%{perl_vendorarch}/*
