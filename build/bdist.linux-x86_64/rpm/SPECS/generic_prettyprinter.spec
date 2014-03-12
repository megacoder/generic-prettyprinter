%define name generic_prettyprinter
%define version 1.0.6
%define unmangled_version 1.0.6
%define release 1

Summary: Generic Pretty Printer, using plugins
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Tommy Reynolds <Tommy.Reynolds@MegaCoder.com>
Packager: Tommy Reynolds <Tommy.Reynolds@MegaCoder.com>
Url: http://www.MegaCoder.com

%description
                             generic-prettyprinter

   Displays a variety of files in a canonical form. Trivial prettyprinters
   for lots of kinds of files. Really easy to extend.


%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
