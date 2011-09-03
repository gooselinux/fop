Summary:        XSL-driven print formatter
Name:           fop
Version:        0.95
Release:        4.2%{?dist}
License:        ASL 2.0
Group:          Applications/Text
Source0:        http://www.apache.org/dist/xmlgraphics/fop/source/%{name}-%{version}-src.tar.gz
Source1:        %{name}.script
Source2:        batik-pdf-MANIFEST.MF
Patch0:         %{name}-manifest.patch
Patch1:         %{name}-main.patch
URL:            http://xmlgraphics.apache.org/fop

Requires:       xmlgraphics-commons >= 1.2
Requires:       avalon-framework >= 4.1.4
Requires:       batik >= 1.7
Requires:       xalan-j2 >= 2.7.0
Requires:       xml-commons-apis >= 1.3.04
Requires:       jakarta-commons-httpclient
Requires:       jakarta-commons-io >= 1.2
Requires:       jakarta-commons-logging >= 1.0.4
Requires:       java-1.6.0-openjdk

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ant
BuildRequires:  ant-trax
BuildRequires:  java-1.6.0-openjdk-devel
BuildRequires:  java-1.6.0-openjdk-javadoc

ExclusiveArch: x86_64 i686

%description
FOP is the world's first print formatter driven by XSL formatting
objects. It is a Java application that reads a formatting object tree
and then turns it into a PDF document. The formatting object tree, can
be in the form of an XML document (output by an XSLT engine like XT or
Xalan) or can be passed in memory as a DOM Document or (in the case of
XT) SAX events.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description    javadoc
Javadoc for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p0

%build
export ANT_HOME=/usr/share/ant
export JAVA_HOME=/usr/lib/jvm/java-openjdk
export CLASSPATH=$CLASSPATH:/usr/share/java/ant/ant-trax-1.7.0.jar
export CLASSPATH=$CLASSPATH:/usr/share/java/xmlgraphics-commons.jar
export CLASSPATH=$CLASSPATH:/usr/share/java/batik-all.jar
export CLASSPATH=$CLASSPATH:/usr/share/java/xml-commons-apis.jar
export CLASSPATH=$CLASSPATH:/usr/share/java/xml-commons-apis-ext.jar
ant clean jar-main transcoder-pkg javadocs

%install
rm -rf $RPM_BUILD_ROOT
# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/%{name}.jar META-INF/MANIFEST.MF

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p build/%{name}-transcoder.jar $RPM_BUILD_ROOT%{_javadir}/pdf-transcoder.jar
pushd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}*
do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
done
popd

# script
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/fop

# data
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr conf $RPM_BUILD_ROOT%{_datadir}/%{name}

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README NOTICE
%{_javadir}/%{name}*.jar
%{_datadir}/%{name}
%{_javadir}/pdf-transcoder.jar
%attr(0755,root,root) %{_bindir}/fop


%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Tue Jun 01 2010 Deepak Bhole <dbhole@redhat.com> - 0.95-4.2
- Make builds x86/x86_64 only for RHEL6

* Thu Jan 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0.95-4.1
- Add dist to the release.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 6 2009 Alexander Kurtakov <akurtako@redhat.com> 0.95-2
- Add OSGi manifest (needed for eclipse-birt).

* Thu Dec 18 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.95-1
- New upstream release

* Wed Apr  2 2008 Lillian Angel <langel at redhat.com> - 0.95.0.2.beta1
- Updated release.

* Tue Apr  1 2008 Lillian Angel <langel at redhat.com> - 0.95.0.1.beta1
- Added CLASSPATH to fop.script.

* Mon Mar 31 2008 Lillian Angel <langel at redhat.com> - 0.95.0.1.beta1
- Updated sources to 0.95 beta.
- Updated patches.
- Updated release.

* Mon Mar 31 2008 Lillian Angel <langel at redhat.com> - 0.94.4
- Updated CLASSPATH.
- Updated release.

* Mon Mar 31 2008 Lillian Angel <langel at redhat.com> - 0.94.3
- Fixed JAVA_HOME to point to openjdk, instead of icedtea.

* Mon Mar 31 2008 Lillian Angel <langel at redhat.com> - 0.94.3
- Updated build requirements and requirements to include java-1.6.0-openjdk.
- Updated release.

* Fri Dec  7 2007 Lillian Angel <langel at redhat.com> - 0.94-2
- Updated Release.

* Thu Dec  6 2007 Lillian Angel <langel at redhat.com> - 0.94-1
- Removed ppc/64 conditions since IcedTea is now available for ppc/64.

* Tue Nov 27 2007 Lillian Angel <langel at redhat.com> - 0.94-1
- Fixed to build with gcj on ppc/64.

* Fri Nov 23 2007 Lillian Angel <langel at redhat.com> - 0.94-1
- Fixed rpmlint errors.

* Tue Sep 18 2007 Joshua Sumali <jsumali at redhat.com> - 0:0.94-1
- Update to fop 0.94

* Thu Mar 30 2006 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-9jpp
- First build for JPP-1.7
- Replace avalon-framework, avalon-logkit with their new excalibur-*
  counterparts
- Drop non-free jimi and jai BRs

* Tue Oct 11 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-8jpp
- Patch to Batik >= 1.5.1

* Fri Oct 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-7jpp
- Omit ant -d flag

* Mon Aug 23 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-6jpp
- Build with ant-1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.20.5-5jpp
- Void change

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:0.20.5-4jpp
- Upgrade to Ant 1.6.X

* Thu Jan  8 2004 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-3jpp
- BuildRequires ant-optional.
- Crosslink with full J2SE javadocs instead of just JAXP/XML-commons.
- Add Main-Class back to manifest.

* Tue Sep 23 2003 Paul Nasrat <pauln at truemesh.com> - 0:0.20.5-2jpp
- Fix script and requires
- Remove class path in manifest
- New javadoc style

* Sat Jul 19 2003 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-1jpp
- Update to 0.20.5.
- Crosslink with xml-commons-apis and batik javadocs.
- BuildRequires jai, jce and jimi.

* Sat Jun  7 2003 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-0.rc3a.1jpp
- Update to 0.20.5rc3a.
- Include fop script.
- Non-versioned javadoc symlinks.

* Thu Apr 17 2003 Ville SkyttÃ¤ <ville.skytta at iki.fi> - 0:0.20.5-0.rc2.1jpp
- Update to 0.20.5rc2 and JPackage 1.5.

* Sun Mar 10 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.20.3-1jpp
- 0.20.3 final
- fixed missing symlink

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.20.3-0.rc.1jpp
- 0.20.3rc
- first unified release
- javadoc into javadoc package
- no dependencies for manual package
- s/jPackage/JPackage
- adaptation to new xalan-j2 package
- requires and buildrequires avalon-logkit

* Thu Aug 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 0.20.1-1mdk
- first release
