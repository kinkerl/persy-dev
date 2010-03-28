Name:           persy
Version:        0.9
Release:        1%{?dist}
Summary:        personal synchronization application - based on git

Group:          Applications/Archiving
License:        GPLv2+
URL:            http://kinkerl.github.com/persy/
BuildArch:      noarch
Source0:        http://rserver.de/download/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         %{name}-0.9.patch

BuildRequires:  gettext python-sphinx python-devel
Requires:       git gitk python pygtk2 pygtk2-libglade
Requires:       python-paramiko python-inotify gnome-python2-rsvg python-configobj


%description
backup or synchronize your data with multiple machines. 
persy is designed to run by its own on the computer or in an environment with 
at least one server in reach of every computer with synced files.


%prep
%setup -q

%patch0 -p1


%build
export DISPLAY=":0.0"
./configure && make


%install
rm -rf %{buildroot}
make install \
     PREFIX="%{_prefix}" \
     DESTDIR="%{buildroot}"


%files
%defattr(-,root,root,-)
%doc INSTALL README.markdown
/%{_bindir}/%{name}
/%{_datadir}/%{name}/*
/%{_datadir}/doc/%{name}/*
/%{_datadir}/applications/%{name}.desktop
/%{_datadir}/icons/%{name}.svg
/%{_mandir}/man1/%{name}.1.gz
/%{_sysconfdir}/bash_completion.d/persy


%clean
rm -rf %{buildroot}


%changelog
* Wed Mar 10 2010 Rafael Roemhild <rafael@roemhild.de> 0.9-1
- Initial packaging
