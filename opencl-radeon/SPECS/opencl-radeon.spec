%define radeon_major 1
%define libname %mklibname %name %{radeon_major}
%define develname %mklibname -d %name

Name:		opencl-radeon
Version:	2.9.1.599.381
Release:	%mkrel 1
Summary:	Finnish invoicing software
Group:		System/Libraries
License:	Other
URL:		http://developer.amd.com/tools-and-sdks/opencl-zone/amd-accelerated-parallel-processing-app-sdk/
Source0:	AMD-APP-SDK-linux-v2.9-1.599.381-GA-x86.tar.bz2
Source1:	AMD-APP-SDK-linux-v2.9-1.599.381-GA-x64.tar.bz2
ExcludeArch:	%{arm}

%description
OpenCL is a royalty-free standard for cross-platform, parallel programming
of modern processors found in personal computers, servers and
handheld/embedded devices.

This package provides an Installable Client Driver loader (ICD Loader).
The provided libOpenCL library is able to load any free or non-free installed
ICD (driver backend).

%package -n	%{libname}
Summary:	Radeon OpenCL
Group:		System/Libraries

%description -n %{libname}
OpenCL is a royalty-free standard for cross-platform, parallel programming
of modern processors found in personal computers, servers and
handheld/embedded devices.

This package provides an Installable Client Driver loader (ICD Loader).
The provided libOpenCL library is able to load any free or non-free installed
ICD (driver backend).

%package -n     %{develname}
Summary:        Development files for %{name}
Group:         	Development/C
Requires:       %{libname} = %{version}-%{release}
Provides:       opencl-radeon-devel = %{version}-%{release}
Provides:       libopencl-radeon-devel = %{version}-%{release}
Provides:       opencl-devel = %{version}-%{release}
Provides:	opencl-headers

%description -n %{develname}
OpenCL is a royalty-free standard for cross-platform, parallel programming
of modern processors found in personal computers, servers and
handheld/embedded devices.

This package provides an Installable Client Driver loader (ICD Loader).
The provided libOpenCL library is able to load any free or non-free installed
ICD (driver backend).


%prep
%ifarch x86_64
%setup -q -T -b1 -c
%else
%setup -q -T -b0 -c
%endif

%build
%ifarch x86_64
sh AMD-APP-SDK-v2.9-1.599.381-GA-linux64.sh --noexec --nox11 --nochown --keep
%else
sh AMD-APP-SDK-v2.9-1.599.381-GA-linux32.sh --noexec --nox11 --nochown --keep
%endif

%install

cd 2.9.599.381
%{__install} -d %{buildroot}%{_includedir}/CL
%{__install} -d %{buildroot}%{_libdir}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_sysconfdir}/OpenCL/vendors
%{__install} -d %{buildroot}%{_sysconfdir}/profile.d

%ifarch x86_64
#{__install} -m 0755 bin/x86_64/clinfo  %{buildroot}%{_sbindir}
%{__install} -m 0755 lib/x86_64/*  %{buildroot}%{_libdir}/
echo libamdocl64.so > "%{buildroot}%{_sysconfdir}/OpenCL/vendors/amdocl64.icd"
%else
#{__install} -m 0755 bin/x86/clinfo  %{buildroot}%{_sbindir}
%{__install} -m 0755 lib/x86/*  %{buildroot}%{_libdir}/
echo libamdocl32.so > "%{buildroot}%{_sysconfdir}/OpenCL/vendors/amdocl32.icd"
%endif
%{__install} -m 0755 include/CL/*  %{buildroot}%{_includedir}/CL
echo export OPENCL_VENDOR_PATH="%{_sysconfdir}/OpenCL/vendors/" > %{buildroot}%{_sysconfdir}/profile.d/99radeon.sh

#find %{buildroot} -name '*.la' -delete
#find %{buildroot} -name '*.a' -delete

%files -n %{libname}
%{_sysconfdir}/profile.d/99radeon.sh
%{_libdir}/*.so.%{radeon_major}
%ifarch x86_64
%{_sysconfdir}/OpenCL/vendors/amdocl64.icd
%{_libdir}/libamdocl64.so
%{_libdir}/libamdoclcl64.so
%{_libdir}/libaparapi_x86_64.so
%else
%{_sysconfdir}/OpenCL/vendors/amdocl32.icd
%{_libdir}/libamdocl32.so
%{_libdir}/libamdoclcl32.so
%{_libdir}/libaparapi_x86.so
%endif

%files -n %{develname}
%{_includedir}/CL/
%{_libdir}/libGLEW.so
%{_libdir}/libglut.so
%{_libdir}/libOpenCL.so
%{_libdir}/libGLEW.a
%ifarch x86_64
%{_libdir}/libglut.a
%endif
