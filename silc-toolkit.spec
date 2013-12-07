%define api_version 1.1
%define silcmajor 2
%define clientmajor 3
%define silclibname %mklibname silc %{api_version} %{silcmajor}
%define silclibname_orig %mklibname silc %{api_version}
%define clientlibname %mklibname silcclient %{api_version} %{clientmajor}
%define clientlibname_orig %mklibname silcclient %{api_version}

Summary:	SILC toolkit
Name:		silc-toolkit
Version:	1.1.10
Release:	12
License:	GPLv2
Group:		Networking/Chat
URL:		http://silcnet.org/
Source0:	http://silcnet.org/download/toolkit/sources/%{name}-%{version}.tar.gz
Patch2:		silc-toolkit-1.1.5-docinst.patch
#gw fix linking, link libsilc with pthread and dl, link silcclient with silc
Patch3:		silc-toolkit-1.1.10-fix-linking.patch
Requires:	%{silclibname} = %{version}-%{release}
BuildRequires:	libtool
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	nasm

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
Provides:	%{_lib}silc-client1 = %{version}-%{release}

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
Provides:	%{_lib}client1-devel = %{version}-%{release}
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
%patch2 -p1 -b .docinst
%patch3 -p1

#find -type f | xargs file | grep -v script | cut -d: -f1 | xargs chmod -x
autoreconf -fi

%build

%configure2_5x \
	--with-simdir=%{_libdir}/silc/modules \
	--enable-ipv6 \
	--enable-shared \
	--includedir=%{_includedir}/silc

# parallel will succeed but produce broken library
%make -j1 LIBTOOL=%{_bindir}/libtool

%install
%makeinstall_std LIBTOOL=%{_bindir}/libtool

chmod 0755 %{buildroot}%{_libdir}/silc/modules/*.so

%triggerpostun -- libsilc-client1 <= 1.0.1-2mdk
tempfile=`mktemp /etc/ld.so.conf.XXXXXX` || exit $?
grep -v "^%{_libdir}/silc$" /etc/ld.so.conf > $tempfile && cat $tempfile > /etc/ld.so.conf
rm -f $tempfile

%files
%doc %{_docdir}/%{name}/README*
%doc %{_docdir}/%{name}/ChangeLog
%doc %{_docdir}/%{name}/TODO
%{_libdir}/silc

%files -n %{silclibname}
%{_libdir}/libsilc-%{api_version}.so.%{silcmajor}*

%files -n %{clientlibname}
%{_libdir}/libsilcclient-%{api_version}.so.%{clientmajor}*

%files devel
%doc %{_docdir}/%{name}/*
%exclude %{_docdir}/%{name}/README*
%exclude %{_docdir}/%{name}/ChangeLog
%exclude %{_docdir}/%{name}/TODO
%{_includedir}/silc
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.10-5mdv2011.0
+ Revision: 669980
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.10-4mdv2011.0
+ Revision: 607537
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.10-3mdv2010.1
+ Revision: 520219
- rebuilt for 2010.1

* Thu Sep 17 2009 Götz Waschk <waschk@mandriva.org> 1.1.10-2mdv2010.0
+ Revision: 443905
- drop patch 1, it no longer works with libidn 1.13
- fix linking
- reenable --no-undefined

* Tue Sep 15 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1.10-1mdv2010.0
+ Revision: 443001
- 1.1.10

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.1.9-2mdv2010.0
+ Revision: 427140
- rebuild

* Sun Jan 11 2009 Funda Wang <fwang@mandriva.org> 1.1.9-1mdv2009.1
+ Revision: 328294
- new client major
- use system libtool
- use our own libtool
- New version 1.1.9

* Sun Oct 26 2008 Funda Wang <fwang@mandriva.org> 1.1.8-1mdv2009.1
+ Revision: 297336
- fix file list
- New version 1.1.8

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.1.7-4mdv2009.0
+ Revision: 265697
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jun 08 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.7-3mdv2009.0
+ Revision: 216838
- add buildrequires on nasm
- spec file clean
- new license policy

* Thu Apr 24 2008 Götz Waschk <waschk@mandriva.org> 1.1.7-2mdv2009.0
+ Revision: 197112
- drop patch 0, trying to fix bug #40137

* Sun Apr 20 2008 Götz Waschk <waschk@mandriva.org> 1.1.7-1mdv2009.0
+ Revision: 195861
- new version

* Tue Mar 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.6-1mdv2008.1
+ Revision: 188508
- 1.1.6, fixes #38836 (CVE-2008-1227: silc - remote DoS and/or arbitrary code execution)
- sync with fc9

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request

* Wed Nov 21 2007 Funda Wang <fwang@mandriva.org> 1.1.5-1mdv2008.1
+ Revision: 110844
- update to new version 1.1.5

* Wed Oct 17 2007 Funda Wang <fwang@mandriva.org> 1.1.3-2mdv2008.1
+ Revision: 99721
- correct libname according to lib policy at http://wiki.mandriva.com/en/Policies/Library
- New version 1.1.3

* Mon Jul 23 2007 Funda Wang <fwang@mandriva.org> 1.1.2-2mdv2008.0
+ Revision: 54684
- clean spec file
- remove wrong obsoletes and provides

* Mon Jul 23 2007 Funda Wang <fwang@mandriva.org> 1.1.2-1mdv2008.0
+ Revision: 54533
- perl-silc is provided by silc-client now
- Obsoletes old library
- New version

* Tue May 08 2007 Funda Wang <fwang@mandriva.org> 1.0.2-2mdv2008.0
+ Revision: 25013
- fix rpm group


* Sat Jan 20 2007 Götz Waschk <waschk@mandriva.org> 1.0.2-1mdv2007.0
+ Revision: 110993
- we need glib 1.2
- fix buildrequires
- new version
- fix major
- fix installation
- add perl module

  + Emmanuel Andry <eandry@mandriva.org>
    - Import silc-toolkit

* Mon May 08 2006 Stefan van der Eijk <stefan@eijk.nu> 0.9.13-3mdk
- rebuild for sparc

* Sat Jul 02 2005 Abel Cheung <deaddog@mandriva.org> 0.9.13-2mdk
- Fix 64bit arch install

* Wed Apr 27 2005 Abel Cheung <deaddog@mandriva.org> 0.9.13-1mdk
- New release 0.9.13

* Tue Feb 01 2005 Abel Cheung <deaddog@mandrake.org> 0.9.12-3mdk
- multiarch

* Sun Jan 02 2005 Abel Cheung <deaddog@mandrake.org> 0.9.12-2mdk
- Disable parallel build

* Sun Oct 24 2004 Abel Cheung <deaddog@mandrake.org> 0.9.12-1mdk
- First package for Mandrakelinux
- Replace the libraries and devel package from silc-client

