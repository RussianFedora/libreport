%{!?python_site: %define python_site %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
# platform-dependent
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Generic library for reporting various problems
Name: libreport
Version: 2.0.10
Release: 3%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: https://fedorahosted.org/abrt/
Source: https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.gz
Patch0: 0001-Add-cgroup-information-filename.patch
Patch1: 0001-rhbz795548-opt-out-smolt.patch
Patch2: 0001-fixed-memory-leak-in-comment-dup.patch
Patch3: 0001-rhbz-820985-bz-4.2-doesn-t-have-bug_id-member-it-s-i.patch
Patch4: 0002-bugzilla-query-bz-version-and-for-4.2-use-id-element.patch
Patch99: %{name}-2.0.5-read-fedora-release.patch
BuildRequires: dbus-devel
BuildRequires: gtk2-devel
BuildRequires: curl-devel
BuildRequires: desktop-file-utils
BuildRequires: xmlrpc-c-devel
BuildRequires: python-devel
BuildRequires: gettext
BuildRequires: libxml2-devel
BuildRequires: libtar-devel
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: nss-devel
BuildRequires: texinfo
BuildRequires: asciidoc
BuildRequires: xmlto
BuildRequires: newt-devel
BuildRequires: libproxy-devel
Requires: libreport-filesystem
# required for update from old report library, otherwise we obsolete report-gtk
# and all it's plugins, but don't provide the python bindings and the sealert
# end-up with: can't import report.GtkIO
# FIXME: can be removed when F15 will EOLed, needs to stay in rhel6!
Requires: libreport-python = %{version}-%{release}

# for rhel6
%if 0%{?rhel} >= 6
BuildRequires: gnome-keyring-devel
%else
BuildRequires: libgnome-keyring-devel
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Libraries providing API for reporting different problems in applications
to different bug targets like Bugzilla, ftp, trac, etc...

%package filesystem
Summary: Filesystem layout for libreport
Group: Applications/File

%description filesystem
Filesystem layout for libreport

%package devel
Summary: Development libraries and headers for libreport
Group: Development/Libraries
Requires: libreport = %{version}-%{release}

%description devel
Development libraries and headers for libreport

%package python
Summary: Python bindings for report-libs
# Is group correct here? -
Group: System Environment/Libraries
Requires: libreport = %{version}-%{release}
Provides: report = 0:0.23-1
Obsoletes: report < 0:0.23-1
# in report the rhtsupport is in the main package, so we need to install it too
%if 0%{?rhel} >= 6
Requires: libreport-plugin-rhtsupport
%endif

%description python
Python bindings for report-libs.

%package cli
Summary: %{name}'s command line interface
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}

%description cli
This package contains simple command line tool for working
with problem dump reports

%package newt
Summary: %{name}'s newt interface
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
Provides: report-newt = 0:0.23-1
Obsoletes: report-newt < 0:0.23-1

%description newt
This package contains a simple newt application for reporting
bugs

%package gtk
Summary: GTK front-end for libreport
Group: User Interface/Desktops
Requires: libreport = %{version}-%{release}
Provides: report-gtk = 0:0.23-1
Obsoletes: report-gtk < 0:0.23-1

%description gtk
Applications for reporting bugs using libreport backend

%package gtk-devel
Summary: Development libraries and headers for libreport
Group: Development/Libraries
Requires: libreport-gtk = %{version}-%{release}

%description gtk-devel
Development libraries and headers for libreport-gtk

%package plugin-kerneloops
Summary: %{name}'s kerneloops reporter plugin
Group: System Environment/Libraries
Requires: curl
Requires: %{name} = %{version}-%{release}

%description plugin-kerneloops
This package contains plugin which sends kernel crash information to specified
server, usually to kerneloops.org.

%package plugin-logger
Summary: %{name}'s logger reporter plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: abrt-plugin-logger < 2.0.4
Provides: report-plugin-localsave = 0:0.23-1
Obsoletes: report-plugin-localsave < 0:0.23-1
Provides: report-config-localsave = 0:0.23-1
Obsoletes: report-config-localsave < 0:0.23-1

%description plugin-logger
The simple reporter plugin which writes a report to a specified file.

%package plugin-mailx
Summary: %{name}'s mailx reporter plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: mailx
Obsoletes: abrt-plugin-mailx < 2.0.4

%description plugin-mailx
The simple reporter plugin which sends a report via mailx to a specified
email address.

%package plugin-bugzilla
Summary: %{name}'s bugzilla plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: abrt-plugin-bugzilla < 2.0.4
Provides: report-plugin-bugzilla = 0:0.23-1
Obsoletes: report-plugin-bugzilla < 0:0.23-1
Provides: report-config-bugzilla-redhat-com = 0:0.23-1
Obsoletes: report-config-bugzilla-redhat-com < 0:0.23-1

%package plugin-bodhi
Summary: %{name}'s bodhi plugin
BuildRequires: json-c-devel
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: PackageKit
BuildRequires: rpm-devel

%description plugin-bodhi
Search for a new updates in bodhi server

%description plugin-bugzilla
Plugin to report bugs into the bugzilla.

%package plugin-rhtsupport
Summary: %{name}'s RHTSupport plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: abrt-plugin-rhtsupport < 2.0.4

%description plugin-rhtsupport
Plugin to report bugs into RH support system.

%package compat
Summary: %{name}'s compat layer for obsoleted 'report' package
Group: System Environment/Libraries
Requires: %{name}-plugin-bugzilla
Requires: %{name}-plugin-rhtsupport

%description compat
Provides 'report' command-line tool.

%package plugin-reportuploader
Summary: %{name}'s reportuploader plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: abrt-plugin-reportuploader < 2.0.4
Provides: report-plugin-ftp = 0:0.23-1
Obsoletes: report-plugin-ftp < 0:0.23-1
Provides: report-config-ftp = 0:0.23-1
Obsoletes: report-config-ftp < 0:0.23-1
Provides: report-plugin-scp = 0:0.23-1
Obsoletes: report-plugin-scp < 0:0.23-1
Provides: report-config-scp = 0:0.23-1
Obsoletes: report-config-scp < 0:0.23-1

%description plugin-reportuploader
Plugin to report bugs into anonymous FTP site associated with ticketing system.

%prep
%setup -q
%patch0 -p1 -b .cgroups
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch99 -p1

%build
autoconf
%configure
CFLAGS="-fno-strict-aliasing"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
%find_lang %{name}

# remove all .la and .a files
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f
mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/events.d/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/events/

# After everything is installed, remove info dir
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%check
make check

%post gtk
/sbin/ldconfig
# update icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun gtk
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gtk
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING
%config(noreplace) %{_sysconfdir}/%{name}/report_event.conf
%config(noreplace) %{_sysconfdir}/%{name}/forbidden_words.conf
%{_libdir}/libreport.so.*
%{_libdir}/libabrt_dbus.so.*
%{_libdir}/libabrt_web.so.*
%exclude %{_libdir}/libabrt_web.so
%{_mandir}/man5/report_event.conf.5*

%files filesystem
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/events.d/
%dir %{_sysconfdir}/%{name}/events/
%dir %{_sysconfdir}/%{name}/plugins/

%files devel
%defattr(-,root,root,-)
# Public api headers:
%{_includedir}/libreport/client.h
%{_includedir}/libreport/dump_dir.h
%{_includedir}/libreport/event_config.h
%{_includedir}/libreport/problem_data.h
%{_includedir}/libreport/report.h
%{_includedir}/libreport/run_event.h
# Private api headers:
%{_includedir}/libreport/internal_abrt_dbus.h
%{_includedir}/libreport/internal_libreport.h
%{_libdir}/libreport.so
%{_libdir}/libabrt_dbus.so
%{_libdir}/pkgconfig/libreport.pc
%dir %{_includedir}/libreport

%files python
%defattr(-,root,root,-)
%{python_sitearch}/report/*
%{python_sitearch}/reportclient/*

%files cli
%defattr(-,root,root,-)
%{_bindir}/report-cli
%{_mandir}/man1/report-cli.1.gz

%files newt
%defattr(-,root,root,-)
%{_bindir}/report-newt

%files gtk
%defattr(-,root,root,-)
%{_bindir}/report-gtk
%{_libdir}/libreport-gtk.so.*

%files gtk-devel
%defattr(-,root,root,-)
%{_libdir}/libreport-gtk.so
%{_includedir}/libreport/internal_libreport_gtk.h
%{_libdir}/pkgconfig/libreport-gtk.pc

%files plugin-kerneloops
%defattr(-,root,root,-)
%{_sysconfdir}/libreport/events/report_Kerneloops.xml
%{_mandir}/man*/reporter-kerneloops.*
%{_bindir}/reporter-kerneloops

%files plugin-logger
%defattr(-,root,root,-)
%{_sysconfdir}/libreport/events/report_Logger.conf
%{_sysconfdir}/libreport/events/report_Logger.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/print_event.conf
%{_bindir}/reporter-print
%{_mandir}/man*/reporter-print.*

%files plugin-mailx
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/plugins/mailx.conf
%{_sysconfdir}/libreport/events/report_Mailx.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/mailx_event.conf
%{_mandir}/man*/reporter-mailx.*
%{_bindir}/reporter-mailx

%files plugin-bodhi
%defattr(-,root,root,-)
%{_bindir}/abrt-bodhi
%{_mandir}/man1/abrt-bodhi.1.gz

%files plugin-bugzilla
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla.conf
%{_sysconfdir}/libreport/events/report_Bugzilla.xml
%config(noreplace) %{_sysconfdir}/libreport/events/report_Bugzilla.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_event.conf
# FIXME: remove with the old gui
%{_mandir}/man1/reporter-bugzilla.1.gz
%{_bindir}/reporter-bugzilla

%files plugin-rhtsupport
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/plugins/rhtsupport.conf
%{_sysconfdir}/libreport/events/report_RHTSupport.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/rhtsupport_event.conf
%{_mandir}/man1/reporter-rhtsupport.1.gz
%{_bindir}/reporter-rhtsupport

%files compat
%defattr(-,root,root,-)
%{_bindir}/report
%{_mandir}/man1/report.1.gz

%files plugin-reportuploader
%defattr(-,root,root,-)
%{_mandir}/man*/reporter-upload.*
%{_bindir}/reporter-upload
%{_sysconfdir}/libreport/events/report_Uploader.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/uploader_event.conf

%changelog
* Mon May 14 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.10-3.R
- fixed compatibility with bugzilla 4.2
- Resolved: #820985, #795548

* Mon Apr 02 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.10-2.R
- added cgroups filename define

* Wed Mar 28 2012 Arkady L. Shane <ashejn@russianfedora.ru> 2.0.10-1.R
- send Fedora to bugzilla instead of RFRemix

* Tue Mar 26 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.10-1
- updated to latest upstream

* Mon Jan 23 2012 Dan Horák <dan@danny.cz> - 2.0.8-6
- rebuilt for json-c-0.9-4.fc17

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Nikola Pajkovsky <npajkovs@redhat.com> 2.0.8-4
- 768647 - [abrt] libreport-plugin-bugzilla-2.0.8-3.fc16: libreport_xatou:
           Process /usr/bin/reporter-bugzilla was killed by signal 11 (SIGSEGV)

* Fri Dec 09 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-3
- fixed few crashes in bodhi plugin

* Thu Dec 08 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-2
- fixed crash in bodhi plugin
- re-upload better backtrace if available
- fixed dupe finding for selinux
- don't duplicate comments in bugzilla
- fixed problem with empty release

* Tue Dec 06 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-1
- new version
- added bodhi plugin rhbz#655783
- one tab per file on details page rhbz#751833
- search box search thru all data (should help with privacy) rhbz#748457
- fixed close button position rhbz#741230
- rise the attachment limit to 4kb rhbz#712602
- fixed make check (rpath problem)
- save chnages in editable lines rhbz#710100
- ignore backup files rhbz#707959
- added support for proxies rhbz#533652
- Resolves: 753183 748457 737991 723219 712602 711986 692274 636000 631856 655783 741257 748457 741230 712602 753183 748457 741230 712602 710100 707959 533652

* Sat Nov 05 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.7-2
- bumped release

* Fri Nov 04 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.7-1
- new version
- added support for bodhi (preview)
- dropped unused patches
- reporter-bugzilla/rhts: add code to prevent duplicate reporting. Closes rhbz#727494 (dvlasenk@redhat.com)
- wizard: search thru all items + tabbed details rhbz#748457 (jmoskovc@redhat.com)
- wizard: add "I don't know what caused this problem" checkbox. Closes rhbz#712508 (dvlasenk@redhat.com)
- reporter-bugzilla: add optional 'Product' parameter. Closes rhbz#665210 (dvlasenk@redhat.com)
- rhbz#728190 - man pages contain suspicious version string (npajkovs@redhat.com)
- reporter-print: expand leading ~/ if present. Closes rhbz#737991 (dvlasenk@redhat.com)
- reporter-rhtsupport: ask rs/problems endpoint before creating new case. (working on rhbz#677052) (dvlasenk@redhat.com)
- reporter-mailx: use Bugzilla's output format. Closes rhbz#717321. (dvlasenk@redhat.com)
- report-newt: add option to display version (rhbz#741590) (mlichvar@redhat.com)
- Resolves: #727494 #748457 #712508 #665210 rhbz#728190 #737991 #677052 #717321 #741590

* Fri Oct 07 2011 Nikola Pajkovsky <npajkovs@redhat.com> 2.0.6-2
- refuse reporting when not reportable file exist

* Mon Oct 03 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.6-1
- updated to the latest upstrem
- just a bug fixing release

* Mon Sep 26 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5.982-1
- re-fix rhbz#730887
- re-fixed prgname (nice icons in gnome3) rhbz#741231
- Resolves: #741231 #730887

* Thu Sep 22 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-9
- don't allow sending reports with bad rating rhbz#672023
- don't allow reporting without duphash rhbz#739182
- tell users to fill out reports in English rhbz#734037
- fixed config for kerneloops reporter rhbz#731189
- Resolves: #672023 #739182 #734037 #731189

* Fri Sep 09 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-8
- allow bugzilla to send binary files
- Related: #733448

* Tue Aug 30 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-7
- added glob support to event xml files
- changed handling of long text files
- added a simple editor as a fallback when no editor is installed (i.e in anaconda) rhbz#728479
- Resolves: #733448 #728479

* Tue Aug 16 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-6
- improved release parsing rhbz#730887
- Resolves: #730887

* Fri Aug 12 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-5
- more anaconda fixes
- Resolves: #729537

* Tue Aug 02 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-4
- silent keyring warning rhbz#692433
- further improvements to Anaconda compatibility

* Fri Jul 29 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-3
- enable bugzilla reporter for analyzer=libreport rhbz#725970
- improved compatibility with anaconda

* Thu Jul 21 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-2
- obsolete report in rawhide properly rhbz#723320
- added button to add attachments
- ignore backup files
- improved support for interactive plugins
- added description text for logger
- added python bindings for interactive plugins
- Resolves: #723320

* Mon Jul 18 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.5-1
- move reporter plugins from abrt to libreport
- fixed provides/obsolete to properly obsolete report package
- wizard: make more fields editable

* Mon Jul 11 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-3
- bump release

* Mon Jun 27 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-2
- removed Provides/Obsoletes: report-gtk

* Mon Jun 20 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-1
- new upstream release
- cleaned some header files

* Thu Jun 16 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.3-1
- added report-cli
- updated translation

* Wed Jun 01 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.2-1
- initial packaging
