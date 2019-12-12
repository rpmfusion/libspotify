Name:		libspotify
Version:	12.1.51
Release:	6%{?dist}
Summary:	Official Spotify API
License:	Redistributable, no modification permitted
URL:		https://mopidy.github.io/libspotify-archive/
Source0:	https://mopidy.github.io/libspotify-archive/libspotify-%{version}-Linux-i686-release.tar.gz
Source1:	https://mopidy.github.io/libspotify-archive/libspotify-%{version}-Linux-x86_64-release.tar.gz
Source4:	https://mopidy.github.io/libspotify-archive/libspotify-%{version}-Linux-armv7-release.tar.gz
ExclusiveArch:	i686 x86_64 armv7hl

%description
libspotify is the official Spotify API.  Applications can use this API to play
music using a user's Spotify account, provided that the user has a Spotify
Premium Account.

%package devel
Summary:	Development files for official Spotify API
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This contains the files needed to develop using libspotify

%prep
%ifarch i686
%setup -q -b 0 -n %{name}-%{version}-Linux-i686-release
%endif
%ifarch x86_64
%setup -q -b 1 -n %{name}-%{version}-Linux-x86_64-release
sed -i 's,prefix)/lib,prefix)/lib64,g' Makefile
%endif
%ifarch armv7hl
%setup -q -b 4 -n %{name}-%{version}-Linux-armv7-release
%endif
%ifnarch i686 x86_64 armv7hl
echo "This cpu architecture is not supported"
exit 1
%endif
cat Makefile | grep -v ldconfig > Makefile.new
rm -f Makefile
mv Makefile.new Makefile

%install
%ifnarch i686 x86_64 armv7hl
echo "This cpu architecture is not supported"
exit 1
%endif
make install prefix=%{buildroot}/usr
ls -l ./
cd %{buildroot}%{_libdir}/pkgconfig
cat libspotify.pc | grep -v "^prefix=" > libspotify.pc.new
echo "prefix=/usr" > libspotify.pc
cat libspotify.pc.new >> libspotify.pc
rm -f libspotify.pc.new
%ifarch x86_64
sed -i s/"\/lib"/"\/lib64"/g libspotify.pc
%endif
chmod 644 %{buildroot}%{_includedir}/libspotify/*

%build

%files
%license LICENSE licenses.xhtml
%doc README
%{_libdir}/libspotify.so.12
%{_libdir}/libspotify.so.12.1.51

%files devel
%license LICENSE licenses.xhtml
%doc README
%{_includedir}/*
%{_libdir}/libspotify.so
%{_libdir}/pkgconfig/*


%changelog
* Sun Dec 08 2019 Tobias Girstmair <t-rpmfusion@girst.at> - 12.1.51-6
- Change upstream to Mopidy's Spotify SDK archive
- Remove unsupported arches armv5 and armv6

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 12.1.51-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 12.1.51-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 12.1.51-3
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 11 2012 Jonathan Dieter <jdieter@gmail.com> - 12.1.51-2
- Add in armv5, armv6 and armv7

* Thu Jun 28 2012 Jonathan Dieter <jdieter@gmail.com> - 12.1.51-1
- Update to 12.1.51

* Mon Mar 26 2012 Jonathan Dieter <jdieter@gmail.com> - 10.1.16-3
- Change license
- Add empty build section to make rpmlint happy

* Mon Jan 23 2012 Jonathan Dieter <jdieter@gmail.com> - 10.1.16-2
- Add documentation to both main and devel package
- Only prep tarball that we're going to use when building

* Wed Jan  4 2012 Jonathan Dieter <jdieter@gmail.com> - 10.1.16-1
- Initial release
