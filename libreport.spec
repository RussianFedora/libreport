%{!?python_site: %define python_site %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
# platform-dependent
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Generic library for reporting various problems
Name: libreport
Version: 2.0.4
Release: 1%{?dist}.1.R
License: GPLv2+
Group: System Environment/Libraries
URL: https://fedorahosted.org/abrt/
Source: https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.gz
Patch0: remove_pyreport.patch
Patch99: %{name}-2.0.3-read-fedora-release.patch
BuildRequires: dbus-devel
BuildRequires: gtk2-devel
BuildRequires: curl-devel
BuildRequires: rpm-devel >= 4.6
BuildRequires: desktop-file-utils
BuildRequires: libnotify-devel
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

%package cli
Summary: %{name}'s command line interface
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}

%description cli
This package contains simple command line tool for working
with problem dump reports

%package gtk
Summary: GTK front-end for libreport
Group: User Interface/Desktops
Requires: libreport = %{version}-%{release}
Provides: report-gtk > 0.20
Obsoletes: report-gtk <= 0.20

%description gtk
Applications for reporting bugs using libreport backend

%package gtk-devel
Summary: Development libraries and headers for libreport
Group: Development/Libraries
Requires: libreport-gtk = %{version}-%{release}

%description gtk-devel
Development libraries and headers for libreport-gtk

%prep
%setup -q
%patch0 -p1 -b remove_python
%patch99 -p1 -b .read-fedora-release

%build
autoconf
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

%files devel
%defattr(-,root,root,-)
# Public api headers:
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

%files cli
%defattr(-,root,root,-)
%{_bindir}/report-cli
%{_mandir}/man1/report-cli.1.gz

%files gtk
%defattr(-,root,root,-)
%{_bindir}/report-gtk
%{_libdir}/libreport-gtk.so.*

%files gtk-devel
%defattr(-,root,root,-)
%{_libdir}/libreport-gtk.so
%{_includedir}/libreport/libreport-gtk.h
%{_libdir}/pkgconfig/libreport-gtk.pc

%changelog
* Mon Jun 27 2011 Arkady L. Shane <ashejn@yandex-team.ru> 2.0.4-1.1.R
- update to 2.0.4
  new upstream release
  cleaned some header files

* Fri Jun 24 2011 Arkady L. Shane <ashejn@yandex-team.ru> 2.0.3-1.1.R
- read product from fedora-release

* Thu Jun 16 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.3-1
- added report-cli
- updated translation

* Wed Jun 01 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.2-1
- initial packaging
