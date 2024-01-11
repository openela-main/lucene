%bcond_with     jp_minimal

Summary:        High-performance, full-featured text search engine
Name:           lucene
Version:        8.4.1
Release:        5%{?dist}
Epoch:          0
License:        ASL 2.0
URL:            http://lucene.apache.org/
# solr source contains both lucene and dev-tools
Source0:        https://archive.apache.org/dist/lucene/solr/%{version}/solr-%{version}-src.tgz

Patch0:         0001-Disable-ivy-settings.patch
Patch1:         0002-Dependency-generation.patch

BuildRequires:  ant
BuildRequires:  ivy-local
BuildRequires:  maven-local
BuildRequires:  mvn(com.ibm.icu:icu4j)
BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%if %{without jp_minimal}
BuildRequires:  mvn(commons-codec:commons-codec)
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.antlr:antlr4-runtime)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.eclipse.jetty:jetty-continuation)
BuildRequires:  mvn(org.eclipse.jetty:jetty-http)
BuildRequires:  mvn(org.eclipse.jetty:jetty-io)
BuildRequires:  mvn(org.eclipse.jetty:jetty-server)
BuildRequires:  mvn(org.eclipse.jetty:jetty-servlet)
BuildRequires:  mvn(org.eclipse.jetty:jetty-util)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-commons)
BuildRequires:  mvn(xerces:xercesImpl)
%endif

Provides:       %{name}-core = %{epoch}:%{version}-%{release}

# Obsolete since F32
# Required deps were removed from fedora
Obsoletes: %{name}-benchmark < 8.1.1-3
Obsoletes: %{name}-demo < 8.1.1-3
Obsoletes: %{name}-facet < 8.1.1-3
Obsoletes: %{name}-replicator < 8.1.1-3
Obsoletes: %{name}-spatial < 8.1.1-3
Obsoletes: %{name}-spatial-extras < 8.1.1-3
Obsoletes: %{name}-spatial3d < 8.1.1-3
Obsoletes: %{name}-test-framework < 8.4.1-4

%if %{with jp_minimal}
# Remove left-over packages that would have broken deps when built in minimal mode
Obsoletes: %{name}-parent < %{version}-%{release}
Obsoletes: %{name}-solr-grandparent < %{version}-%{release}
Obsoletes: %{name}-expressions < %{version}-%{release}
Obsoletes: %{name}-analyzers-phonetic < %{version}-%{release}
Obsoletes: %{name}-analyzers-icu < %{version}-%{release}
Obsoletes: %{name}-analyzers-nori < %{version}-%{release}
Obsoletes: %{name}-analyzers-kuromoji < %{version}-%{release}
Obsoletes: %{name}-analyzers-stempel < %{version}-%{release}
%endif

BuildArch:      noarch

%description
Apache Lucene is a high-performance, full-featured text search
engine library written entirely in Java. It is a technology suitable
for nearly any application that requires full-text search, especially
cross-platform.

%package analysis
Summary:      Lucene Common Analyzers
# Obsoletes since F30
# This module was removed upstream and no replacement exists
Obsoletes: %{name}-analyzers-uima < 8.1.1-3
# Obsolete since F32
# Required deps were removed from fedora
Obsoletes: %{name}-analyzers-morfologik < 8.1.1-3

%description analysis
Lucene Common Analyzers.

%package analyzers-smartcn
Summary:      Smart Chinese Analyzer

%description analyzers-smartcn
Lucene Smart Chinese Analyzer.

%package grouping
Summary:      Lucene Grouping Module

%description grouping
Lucene Grouping Module.

%package highlighter
Summary:      Lucene Highlighter Module

%description highlighter
Lucene Highlighter Module.

%package join
Summary:      Lucene Join Module

%description join
Lucene Join Module.

%package memory
Summary:      Lucene Memory Module

%description memory
High-performance single-document index to compare against Query.

%package misc
Summary:      Miscellaneous Lucene extensions

%description misc
Miscellaneous Lucene extensions.

%package queries
Summary:      Lucene Queries Module

%description queries
Lucene Queries Module.

%package queryparser
Summary:      Lucene QueryParsers Module

%description queryparser
Lucene QueryParsers Module.

%package sandbox
Summary:      Lucene Sandbox Module

%description sandbox
Lucene Sandbox Module.

%package backward-codecs
Summary:      Lucene Backward Codecs Module

%description backward-codecs
Codecs for older versions of Lucene.

%package codecs
Summary:      Codecs and postings formats for Apache Lucene

%description codecs
Codecs and postings formats for Apache Lucene.

%package classification
Summary:      Lucene Classification Module

%description classification
Lucene Classification Module.

%package suggest
Summary:      Lucene Suggest Module

%description suggest
Lucene Suggest Module.

%package monitor
Summary:      Lucene Monitor Module

%description monitor
Lucene Monitor Module.

%if %{without jp_minimal}

%package parent
Summary:      Parent POM for Lucene

%description parent
Parent POM for Lucene.

%package solr-grandparent
Summary:      Lucene Solr grandparent POM

%description solr-grandparent
Lucene Solr grandparent POM.

%package expressions
Summary:      Lucene Expressions Module

%description expressions
Dynamically computed values to sort/facet/search on based on a pluggable
grammar.

%package analyzers-phonetic
Summary:      Lucene Phonetic Filters

%description analyzers-phonetic
Provides phonetic encoding via Commons Codec.

%package analyzers-icu
Summary:      Lucene ICU Analysis Components

%description analyzers-icu
Provides integration with ICU (International Components for Unicode) for
stronger Unicode and internationalization support.

%package analyzers-nori
Summary:      An analyzer with morphological analysis for Korean

%description analyzers-nori
An analyzer with morphological analysis for Korean.

%package analyzers-kuromoji
Summary:      Lucene Kuromoji Japanese Morphological Analyzer

%description analyzers-kuromoji
Lucene Kuromoji Japanese Morphological Analyzer.

%package analyzers-stempel
Summary:      Lucene Stempel Analyzer

%description analyzers-stempel
Lucene Stempel Analyzer.

%endif

%package javadoc
Summary:        Javadoc for Lucene

%description javadoc
%{summary}.

%prep
%setup -q -n solr-%{version}

%patch0 -p1
%patch1 -p1

rm -rf solr

find -name "*.jar" -delete

mkdir -p lucene/build/analysis/{kuromoji,nori}

# don't generate uses clauses in osgi metadata
sed -i -e "/<Export-Package>/a<_nouses>true</_nouses>" dev-tools/maven/pom.xml.template

# compatibility with existing packages
%mvn_alias :%{name}-analyzers-common :%{name}-analyzers

%mvn_package ":%{name}-analysis-modules-aggregator" %{name}-analysis
%mvn_package ":%{name}-analyzers-common" %{name}-analysis
%mvn_package ":{*}-aggregator" @1

%build
pushd %{name}
find -maxdepth 2 -type d -exec mkdir -p '{}/lib' \;

# generate maven dependencies
ant -f build.xml generate-maven-artifacts -Divy.mode=local -Dversion=%{version} -Divy.available=true

# fix source dir + move to expected place
for pom in `find build/poms/%{name} -name pom.xml`; do
    sed 's/\${module-path}/${basedir}/g' "$pom" > "${pom##build/poms/%{name}/}"
done
%pom_disable_module src/test core
%pom_disable_module src/test codecs

popd

mv lucene/build/poms/pom.xml .

# deal with split packages in core/misc/analysis modules by adding additional metadata and
# require-bundling the core bundle from misc
%pom_xpath_set "pom:Export-Package" "*;version=\"%{version}\""
%pom_add_plugin org.apache.felix:maven-bundle-plugin lucene/misc \
"<configuration><instructions>
<Require-Bundle>org.apache.lucene.core;bundle-version=\"%{version}\"</Require-Bundle>
<Export-Package>
 org.apache.lucene.document;version=\"%{version}\";misc=split;mandatory:=misc,
 org.apache.lucene.index;version=\"%{version}\";misc=split;mandatory:=misc,
 org.apache.lucene.search;version=\"%{version}\";misc=split;mandatory:=misc,
 org.apache.lucene.store;version=\"%{version}\";misc=split;mandatory:=misc,
 org.apache.lucene.util.fst;version=\"%{version}\";misc=split;mandatory:=misc,
 *;version=\"%{version}\"</Export-Package>
</instructions></configuration>"
%pom_add_plugin org.apache.felix:maven-bundle-plugin lucene/analysis/common \
"<configuration><instructions>
<Require-Bundle>org.apache.lucene.core;bundle-version=\"%{version}\"</Require-Bundle>
<Export-Package>
 org.apache.lucene.analysis.standard;version=\"%{version}\";analysis=split;mandatory:=analysis,
 *;version=\"%{version}\"</Export-Package>
</instructions></configuration>"

%pom_disable_module solr
%pom_remove_plugin -r :gmaven-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin -r :forbiddenapis
%pom_remove_plugin -r :buildnumber-maven-plugin

# don't build modules for which deps are not in fedora or not new enough in fedora
pushd lucene
%pom_disable_module benchmark
%pom_disable_module demo
%pom_disable_module test-framework
%pom_disable_module facet
%pom_disable_module replicator
%pom_disable_module spatial
%pom_disable_module spatial-extras
%pom_disable_module spatial3d

%pom_disable_module opennlp analysis
%pom_disable_module morfologik analysis
popd

%if %{with jp_minimal}
pushd lucene
%pom_disable_module expressions
%pom_disable_module icu analysis
%pom_disable_module kuromoji analysis
%pom_disable_module phonetic analysis
%pom_disable_module stempel analysis
%pom_disable_module nori analysis
popd

%mvn_package :lucene-parent __noinstall
%mvn_package :lucene-solr-grandparent __noinstall
%endif

# For some reason TestHtmlParser.testTurkish fails when building inside SCLs
%mvn_build -s -f

%install
%mvn_install

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

%files -f .mfiles-%{name}-core
%doc lucene/CHANGES.txt lucene/README.txt
%doc lucene/MIGRATE.txt lucene/JRE_VERSION_MIGRATION.txt
%license lucene/LICENSE.txt lucene/NOTICE.txt

%files analysis -f .mfiles-%{name}-analysis

%files analyzers-smartcn -f .mfiles-%{name}-analyzers-smartcn

%files grouping -f .mfiles-%{name}-grouping

%files highlighter -f .mfiles-%{name}-highlighter

%files join -f .mfiles-%{name}-join

%files memory -f .mfiles-%{name}-memory

%files misc -f .mfiles-%{name}-misc

%files queries -f .mfiles-%{name}-queries

%files queryparser -f .mfiles-%{name}-queryparser

%files sandbox -f .mfiles-%{name}-sandbox

%files backward-codecs -f .mfiles-%{name}-backward-codecs

%files codecs -f .mfiles-%{name}-codecs

%files classification -f .mfiles-%{name}-classification

%files suggest -f .mfiles-%{name}-suggest

%files monitor -f .mfiles-%{name}-monitor
%if %{without jp_minimal}

%files parent -f .mfiles-%{name}-parent

%files solr-grandparent -f .mfiles-%{name}-solr-grandparent

%files expressions -f .mfiles-%{name}-expressions

%files analyzers-phonetic -f .mfiles-%{name}-analyzers-phonetic

%files analyzers-icu -f .mfiles-%{name}-analyzers-icu

%files analyzers-nori -f .mfiles-%{name}-analyzers-nori

%files analyzers-kuromoji -f .mfiles-%{name}-analyzers-kuromoji

%files analyzers-stempel -f .mfiles-%{name}-analyzers-stempel
%endif

%files javadoc -f .mfiles-javadoc
%license lucene/LICENSE.txt lucene/NOTICE.txt

%changelog
* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 0:8.4.1-5
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed May 06 2020 Mat Booth <mat.booth@redhat.com> - 0:8.4.1-4
- Fix jp_minimal mode

* Tue May 5 2020 Alexander Kurtakov <akurtako@redhat.com> - 0:8.4.1-3
- Disable test-framework as its dependency (randomizedtesting) is removed.

* Sat Mar 21 2020 Mat Booth <mat.booth@redhat.com> - 0:8.4.1-2
- Fix deps for minimal mode

* Sat Mar 21 2020 Mat Booth <mat.booth@redhat.com> - 0:8.4.1-1
- Update to latest upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:8.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Mat Booth <mat.booth@redhat.com> - 0:8.1.1-3
- Drop spatial, morfologik, replicator, demo and benchmark modules due to missing deps
- Fix obsoletes when built in minimal mode

* Thu Jun 13 2019 Mat Booth <mat.booth@redhat.com> - 0:8.1.1-2
- Enable additional module in jp_minimal mode

* Wed Jun 12 2019 Mat Booth <mat.booth@redhat.com> - 0:8.1.1-1
- Update to latest upstream release

* Thu Feb 14 2019 Mat Booth <mat.booth@redhat.com> - 0:7.7.0-1
- Update to latest upstream release
- Drop deprecated uima analyzers sub-package
- Added nori Korean analyzers sub-package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 26 2018 Mat Booth <mat.booth@redhat.com> - 0:7.1.0-2
- Fix split package information in OSGi metadata

* Thu Apr 12 2018 Mat Booth <mat.booth@redhat.com> - 0:7.1.0-1
- Update to a newer upstream release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 07 2017 Mat Booth <mat.booth@redhat.com> - 0:6.1.0-7
- Enable more modules in jp_minimal profile, rhbz#1455267

* Mon Oct 16 2017 Michael Simacek <msimacek@redhat.com> - 0:6.1.0-6
- Backport fix for CVE-2017-12629

* Thu Sep 21 2017 Mat Booth <mat.booth@redhat.com> - 0:6.1.0-5
- Rebuild to regenerate OSGi metadata due to objectweb-asm update

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:6.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 04 2017 Mat Booth <mat.booth@redhat.com> - 0:6.1.0-3
- Add better OSGi metadata for dealing with core/misc split packages
- Drop F24-specific hack

* Tue Mar 21 2017 Michael Simacek <msimacek@redhat.com> - 0:6.1.0-2
- Update jp_minimal conditional

* Mon Mar 20 2017 Mat Booth <mat.booth@redhat.com> - 0:6.1.0-1
- Update to lucene 6
- Add "spatial-extras" subpackage, this decouples dependencies on spatial4j.

* Thu Mar 16 2017 Michael Simacek <msimacek@redhat.com> - 0:5.5.0-7
- Add jp_minimal conditional

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 0:5.5.0-6
- Remove buildnumber-plugin

* Mon Aug 22 2016 Roman Vais <rvais@redhat.com> - 0:5.5.0-5
- Removed test dependency macros for lucene demo that caused conflict (duplicity)

* Wed Jul 13 2016 Roland Grunberg <rgrunber@redhat.com> - 0:5.5.0-4
- analyzers-common should have versioned requires on package from core.

* Fri Jul 08 2016 Mat Booth <mat.booth@redhat.com> - 0:5.5.0-3
- Misc module should require core module, the split package
  causes problems for OSGi consumers

* Mon Apr 18 2016 Mat Booth <mat.booth@redhat.com> - 0:5.5.0-2
- Add missing BR on ant, fixes FTBFS

* Wed Feb 24 2016 Michael Simacek <msimacek@redhat.com> - 0:5.5.0-1
- Update to upstream version 5.5.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:5.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Alexander Kurtakov <akurtako@redhat.com> 0:5.4.1-2
- Organize Sources numbering.
- Drop old jpackage header - package has nothing in common anymore.
- Drop 3+ years old provides/obsoletes.
- Move old changelog to separate file to ease working with the spec file.

* Mon Jan 25 2016 Alexander Kurtakov <akurtako@redhat.com> 0:5.4.1-1
- Update to upstream 5.4.1 release.

* Thu Jan 21 2016 Alexander Kurtakov <akurtako@redhat.com> 0:5.4.0-1
- Update to upstream 5.4.0 release.

* Tue Oct 6 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.3.1-1
- Update to upstream 5.3.1 release.

* Thu Aug 27 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.3.0-1
- Update to upstream 5.3.0 release.

* Wed Aug 26 2015 Mat Booth <mat.booth@redhat.com> - 0:5.2.1-4
- Remove forbidden SCL macros

* Wed Jun 24 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.2.1-3
- Disable generation of uses clauses in OSGi manifests.

* Wed Jun 24 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.2.1-2
- Drop old workarounds.

* Tue Jun 23 2015 Alexander Kurtakov <akurtako@redhat.com> 0:5.2.1-1
- Update to upstream 5.2.1.