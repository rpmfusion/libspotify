Name:		libspotify
Version:	10.1.16
Release:	3%{?dist}
Summary:	Official Spotify API
Group:		Development/Libraries
License:	Redistributable, no modification permitted
URL:		http://developer.spotify.com/en/libspotify/overview/
Source0:	http://developer.spotify.com/download/libspotify/libspotify-10.1.16-Linux-i686-release.tar.gz
Source1:	http://developer.spotify.com/download/libspotify/libspotify-10.1.16-Linux-x86_64-release.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
libspotify is the official Spotify API.  Applications can use this API to play
music using a user's Spotify account, provided that the user has a Spotify
Premium Account.

%package devel
Summary:	Development files for official Spotify API
Requires:	libspotify = %{version}-%{release}

%description devel
This contains the files needed to develop using libspotify

%prep
mkdir -p %{name}-%{version}
cd %{name}-%{version}
%ifarch %{ix86}
tar -xf %{SOURCE0}
cd libspotify-Linux-i686-release
cat Makefile | grep -v ldconfig > Makefile.new
rm -f Makefile
mv Makefile.new Makefile
cd ..
%endif
%ifarch x86_64
tar -xf %{SOURCE1}
cd libspotify-Linux-x86_64-release
cat Makefile | grep -v ldconfig > Makefile.new
rm -f Makefile
mv Makefile.new Makefile
sed -i s/"\$(prefix)\/lib"/"\$(prefix)\/lib64"/g Makefile
cd ..
%endif
%ifnarch %{ix86} x86_64
echo "This cpu architecture is not supported"
exit 1
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}-%{version}
%ifarch %{ix86}
cd libspotify-Linux-i686-release
%endif
%ifarch x86_64
cd libspotify-Linux-x86_64-release
%endif
%ifnarch %{ix86} x86_64
echo "This cpu architecture is not supported"
exit 1
%endif
make install prefix=$RPM_BUILD_ROOT/usr
cp LICENSE README licenses.xhtml ../
ls -l ../
cd $RPM_BUILD_ROOT%{_libdir}/pkgconfig
cat libspotify.pc | grep -v "^prefix=" > libspotify.pc.new
echo "prefix=/usr" > libspotify.pc
cat libspotify.pc.new >> libspotify.pc
rm -f libspotify.pc.new
%ifarch x86_64
sed -i s/"\/lib"/"\/lib64"/g libspotify.pc
%endif
chmod 644 $RPM_BUILD_ROOT%{_includedir}/libspotify/*

%build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc %{name}-%{version}/LICENSE %{name}-%{version}/README %{name}-%{version}/licenses.xhtml
%{_libdir}/libspotify.so.*

%files devel
%defattr(-,root,root,-)
%doc %{name}-%{version}/LICENSE %{name}-%{version}/README %{name}-%{version}/licenses.xhtml
%{_includedir}/*
%{_libdir}/libspotify.so
%{_libdir}/pkgconfig/*


%changelog
* Mon Mar 26 2012 Jonathan Dieter <jdieter@gmail.com> - 10.1.16-3
- Change license
- Add empty build section to make rpmlint happy

* Mon Jan 23 2012 Jonathan Dieter <jdieter@gmail.com> - 10.1.16-2
- Add documentation to both main and devel package
- Only prep tarball that we're going to use when building

* Wed Jan  4 2012 Jonathan Dieter <jdieter@gmail.com> - 10.1.16-1
- Initial release
