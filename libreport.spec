%{!?python_site: %define python_site %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
# platform-dependent
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Generic library for reporting various problems
Name: libreport
Version: 2.0.5
Release: 8%{?dist}.1.R
License: GPLv2+
Group: System Environment/Libraries
URL: https://fedorahosted.org/abrt/
Source: https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.gz
Patch0: 0006-support-interactive-plugins-in-GUI-and-CLI.patch
Patch1: 0007-wizard-if-more-than-one-reporter-is-chosen-select-al.patch
Patch2: 0008-added-xml-file-for-Logger-event.patch
Patch3: 0009-report-cli-don-t-crash-when-invalid-analyzer-is-sele.patch
Patch4: 0011-add-python-bindings-for-interactive-plugins.patch
Patch5: 0012-run_event_on_dir-fix-double-free.patch
Patch6: 0015-honor-minimal-rating.patch
Patch7: 0025-added-minimal-rating-entry-to-all-event-xml-files.patch
Patch8: 0026-rhbz-724999-fix-null-in-summary.patch
Patch10: 0001-fix-el6-keyring.patch
Patch11: 0031-added-bugzilla_event.conf-to-enable-Bugzilla-for-all.patch
Patch12: 0032-improved-compatibility-with-anaconda-rhbz-725857.patch
Patch13: 0001-warn-silently-if-keyring-is-not-available-rhbz-72585.patch
Patch14: 0002-don-t-reload-event-configuration-when-dump_dir-chang.patch
Patch15: 0003-wizard-add-configure-event-button-to-wrong-settings-.patch
Patch16: 0004-check-settings-only-for-last-selected-reporter.patch
Patch17: fix_adding_external_files_to_report.patch
Patch18: emptylines_interactive_di.patch
Patch19: 0003-Ignore-files-which-seem-to-be-editor-backups.-Closes.patch
Patch22: 0010-Add-another-reporting-flag-LIBREPORT_GETPID.patch
Patch23: 0001-libreport-force-run-cli-event-if-DISPLAY-exist.patch
Patch27: 0018-report-cli-sync-man-page-with-actual-switches.patch
Patch28: 0019-compare-problem-data-by-content-of-file-FILENAME_.patch
Patch29: 0021-fix-wrong-casting.patch
Patch30: 0024-wizard-rename-Configure-Event-Preferences.patch
Patch31: 0025-attach-file-to-bugzilla-ticket.patch
Patch34: 0028-add-report-compat-tool.-Closes-315-bz-725660.patch
Patch35: 0029-fixed-wrapping-in-comment-textview-rhbz-728132.patch
Patch37: 0033-rename-plugins-Bugzilla.conf-plugins-bugzilla.conf.patch
Patch39: 0035-dd_opendir-require-time-file-to-exist-even-in-read-o.patch
Patch41: 0037-reporter-rhtsupport-do-not-hardcode-blacklisting.patch
Patch42: 0038-report-newt-fix-help-text-option-o-is-mandatory.patch
Patch43: 0039-report-newt-fit-reporting-window-to-standard-termina.patch
Patch45: 0041-report_-.xml-exclude-count-event_log-reported_to-vmc.patch
Patch46: 0042-added-xml-and-event-conf-for-uploader.patch
Patch48: 0044-reporter-rhtsupport-fix-product-name-reported-to-ser.patch
Patch50: 0046-uploader_event.conf-added-new-line-to-the-end-of-fil.patch
Patch51: 0047-read-default-CONFFILE-if-no-c-option-is-given.patch
Patch52: 0048-fixed-reporting-from-anaconda-newtUI-rhbz-729537-rhb.patch
Patch54: 0050-report-expand-help-text-mention-.conf-files-in-it.patch
Patch55: 0051-fix-make-check.patch
Patch56: parse_release_bz.patch
Patch57: libreport-fallback-textedit.patch
Patch58: 0001-reporter-bugzilla-fix-file-attaching-was-using-strle.patch
Patch59: 0002-wizard-support-shell-glob-patterns-in-.xml-item-sele.patch
Patch60: 0001-reporter-bugzilla-add-b-to-make-it-possible-to-attac.patch
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
Provides: report = 0.23-1
Obsoletes: report < 0.23-1
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
Provides: report-newt = 0.23-1
Obsoletes: report-newt < 0.23-1

%description newt
This package contains a simple newt application for reporting
bugs

%package gtk
Summary: GTK front-end for libreport
Group: User Interface/Desktops
Requires: libreport = %{version}-%{release}
Provides: report-gtk = 0.23-1
Obsoletes: report-gtk < 0.23-1

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
Provides: report-plugin-localsave = 0.23-1
Obsoletes: report-plugin-localsave < 0.23-1
Provides: report-config-localsave = 0.23-1
Obsoletes: report-config-localsave < 0.23-1

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
Provides: report-plugin-bugzilla = 0.23-1
Obsoletes: report-plugin-bugzilla < 0.23-1
Provides: report-config-bugzilla-redhat-com = 0.23-1
Obsoletes: report-config-bugzilla-redhat-com < 0.23-1

%description plugin-bugzilla
Plugin to report bugs into the bugzilla.

%package plugin-rhtsupport
Summary: %{name}'s RHTSupport plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: abrt-plugin-rhtsupport < 2.0.4

%description plugin-rhtsupport
Plugin to report bugs into RH support system.

%package plugin-reportuploader
Summary: %{name}'s reportuploader plugin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: abrt-plugin-reportuploader < 2.0.4
Provides: report-plugin-ftp = 0.23-1
Obsoletes: report-plugin-ftp < 0.23-1
Provides: report-config-ftp = 0.23-1
Obsoletes: report-config-ftp < 0.23-1
Provides: report-plugin-scp = 0.23-1
Obsoletes: report-plugin-scp < 0.23-1
Provides: report-config-scp = 0.23-1
Obsoletes: report-config-scp < 0.23-1

%description plugin-reportuploader
Plugin to report bugs into anonymous FTP site associated with ticketing system.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch22 -p1
%patch23 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch34 -p1
%patch35 -p1
%patch37 -p1
%patch39 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch45 -p1
%patch46 -p1
%patch48 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch99 -p1

%build
mkdir -p m4
test -r m4/aclocal.m4 || touch m4/aclocal.m4
autoconf
automake
%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
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
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/events.d/
%dir %{_sysconfdir}/%{name}/events/
%config(noreplace) %{_sysconfdir}/%{name}/report_event.conf
%{_libdir}/libreport.so.*
%{_libdir}/libabrt_dbus.so.*
%{_libdir}/libabrt_web.so.*
%exclude %{_libdir}/libabrt_web.so
%{_bindir}/report

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
%{_sysconfdir}/libreport/events/report_Mailx.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/mailx_event.conf
%{_mandir}/man*/reporter-mailx.*
%{_bindir}/reporter-mailx

%files plugin-bugzilla
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla.conf
%{_sysconfdir}/libreport/events/report_Bugzilla.xml
%config(noreplace) %{_sysconfdir}/libreport/events/report_Bugzilla.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_event.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_event.conf
# FIXME: remove with the old gui
%{_mandir}/man1/reporter-bugzilla.1.gz
%{_bindir}/reporter-bugzilla

%files plugin-rhtsupport
%defattr(-,root,root,-)
#%config(noreplace) %{_sysconfdir}/libreport/plugins/rhtsupport.conf
%{_sysconfdir}/libreport/events/report_RHTSupport.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/rhtsupport_event.conf
# {_mandir}/man7/abrt-RHTSupport.7.gz
%{_bindir}/reporter-rhtsupport

%files plugin-reportuploader
%defattr(-,root,root,-)
%{_mandir}/man*/reporter-upload.*
%{_bindir}/reporter-upload
%{_sysconfdir}/libreport/events/report_Uploader.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/uploader_event.conf

%changelog
* Fri Sep 17 2011 Arkady L. Shane <ashejn@russianfedora.ru> 2.0.5-8.1.R
- read fedora-release

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
