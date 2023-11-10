#=================================================
# Specification file for White Pages
#
# Install LTB project White Pages
#
# GPL License
#
# Copyright (C) 2009-2023 Clement OUDOT
# Copyright (C) 2009-2023 LTB-project
#=================================================

%global wp_destdir   %{_datadir}/%{name}
%global wp_cachedir  %{_localstatedir}/cache/%{name}

Name:      white-pages
Version:   0.4
Release:   3%{?dist}
Summary:   LDAP white pages web interface
URL:       https://ltb-project.org/documentation/white-pages.html
License:   GPL-3.0-only

BuildArch: noarch

Source0:   https://github.com/ltb-project/white-pages/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:   white-pages-apache.conf
Source2:   white-pages-vendor_autoload
Source3:   white-pages-config_inc_local

# https://github.com/ltb-project/white-pages/commit/1d7b6b2eb32c62b0f7fec2c10e979c024ef7e84c.patch
Patch0:    white-pages-0.4-phpunit_6+_fix.patch

Requires(pre):  httpd
Requires:  coreutils
Requires:  mod_php
Requires:  php
Requires:  php-ldap
Requires:  php-gd
Requires:  php-Smarty
Requires:  php-phpmailer6
Requires:  php-ltb-project-ldap

# Fonts
Provides:  bundled(fontawesome-fonts) = 4.7.0
# CSS
Provides:  bundled(css-hover) = 2.0.1
# Javascripts
Provides:  bundled(js-bootstrap) = 3.2.0
Provides:  bundled(js-bootstrap-datepicker) = 1.6.4
Provides:  bundled(js-datatables) = 1.10.16
Provides:  bundled(js-jquery) = 1.10.2
Provides:  bundled(js-leaflet) = 1.9.3
Provides:  bundled(js-leaflet.markercluster) = 1.5.3


%description
White Pages is a PHP application that allows users to search and display data
stored in an LDAP directory.
White Pages is provided by LDAP Tool Box project: https://ltb-project.org


%prep
%autosetup -p1


%build
# Nothing to build


%install
# Create directories
mkdir -p %{buildroot}/%{wp_destdir}
mkdir -p %{buildroot}/%{wp_destdir}/bin
mkdir -p %{buildroot}/%{wp_destdir}/conf
mkdir -p %{buildroot}/%{wp_destdir}/htdocs
mkdir -p %{buildroot}/%{wp_destdir}/lang
mkdir -p %{buildroot}/%{wp_destdir}/lib
mkdir -p %{buildroot}/%{wp_destdir}/templates
mkdir -p %{buildroot}/%{wp_destdir}/vendor
mkdir -p %{buildroot}/%{wp_cachedir}/cache
mkdir -p %{buildroot}/%{wp_cachedir}/templates_c

# Copy files
## Program
install -m 755 bin/*          %{buildroot}/%{wp_destdir}/bin
install -m 644 htdocs/*.php   %{buildroot}/%{wp_destdir}/htdocs
cp -a          htdocs/css     %{buildroot}/%{wp_destdir}/htdocs
cp -a          htdocs/js      %{buildroot}/%{wp_destdir}/htdocs
cp -a          htdocs/images  %{buildroot}/%{wp_destdir}/htdocs
cp -a          htdocs/vendor  %{buildroot}/%{wp_destdir}/htdocs
install -m 644 lang/*         %{buildroot}/%{wp_destdir}/lang
install -m 644 lib/*          %{buildroot}/%{wp_destdir}/lib
install -m 644 templates/*    %{buildroot}/%{wp_destdir}/templates

# External libs
mkdir -p %{buildroot}/%{wp_destdir}/vendor
install -m 644 %{SOURCE2} %{buildroot}/%{wp_destdir}/vendor/autoload.php

## Apache configuration
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -m 644 %{SOURCE1} \
  %{buildroot}%{_sysconfdir}/httpd/conf.d/white-pages.conf

# Adapt Smarty paths
sed -i \
  -e 's:/usr/share/php/smarty3:/usr/share/php/Smarty:' \
  -e 's:^#$smarty_cache_dir.*:$smarty_cache_dir = "'%{wp_cachedir}/cache'";:' \
  -e 's:^#$smarty_compile_dir.*:$smarty_compile_dir = "'%{wp_cachedir}/templates_c'";:' \
  conf/config.inc.php

# Move conf dir
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 644 conf/config.inc.php \
  %{buildroot}/%{_sysconfdir}/%{name}/
ln -s %{_sysconfdir}/%{name}/config.inc.php \
  %{buildroot}%{wp_destdir}/conf/config.inc.php
install -m 644 %{SOURCE3} \
  %{buildroot}/%{_sysconfdir}/%{name}/config.inc.local.php


%check
%{?fedora:phpunit9 --verbose --testdox --do-not-cache-result tests}


%post
# Move configuration for older installation
if [ -f "%{wp_destdir}/conf/config.inc.php" ]; then
    mv %{wp_destdir}/conf/config.inc.php %{_sysconfdir}/%{name}/config.inc.php
fi
# Move configuration override too
if [ -f "%{wp_destdir}/conf/config.inc.local.php" ]; then
    mv %{wp_destdir}/conf/config.inc.local.php \
      %{_sysconfdir}/%{name}/config.inc.local.php
fi


%files
%license LICENCE
%doc AUTHORS README.md
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config.inc.php
%config(noreplace) %{_sysconfdir}/%{name}/config.inc.local.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/white-pages.conf
%{wp_destdir}/
%dir %{wp_cachedir}
%attr(-,apache,apache) %{wp_cachedir}/cache/
%attr(-,apache,apache) %{wp_cachedir}/templates_c/


%changelog
* Fri Nov 10 2023 Xavier Bachelot <xavier@bachelot.org> - 0.4-3
- Spec file cleanup

* Wed May 17 2023 - Clement Oudot <clem@ltb-project.org> - 0.4-2
- gh#126: Missing bin/ directory in packages

* Thu May 04 2023 - Clement Oudot <clem@ltb-project.org> - 0.4-1
- gh#75: Display account : empty result
- gh#76: add a option to change timeout of ldap connexion
- gh#77: Gallery by group
- gh#79: Add gallery by group
- gh#80: Add possibility to use gravatar as photo
- gh#81: Disable PHP errors (error_reporting) if debug is not set
- gh#82: Disable error reporting if debug is false
- gh#84: Manage "bytes" attributes
- gh#85: New type "bytes"
- gh#87: Possibility to negates value in search
- gh#88: Move documentation in sources
- gh#89: Add ldap_network_timeout option
- gh#92: Allow the Smarty path to be set in conf.inc.local.php
- gh#93: Configure cache dir and template cache dir
- gh#95: feat(docker): sample docker image & kubernetes deployment
- gh#97: Groups Vcard
- gh#98: Patch datepicker lang
- gh#104: Fix undefined warnings
- gh#106: Issue 88 & Small Fixes
- gh#107: Fixes on online doc
- gh#108: Bad value displayed when attribute type is a list
- gh#109: Backup files are loaded as config in lang/
- gh#110: Restrict languages to php files
- gh#112: Display list value
- gh#113: Manage cache dirs
- gh#115: WP incompatible with PHP 8+ (ldap_sort)
- gh#116: Split debug and debug_smarty
- gh#117: Provide CSS map files for minified version
- gh#118: New feature: Map
- gh#119: Use LTB LDAP common lib
- gh#120: Factorize search
- gh#121: Displayer for address
- gh#122: Address displayer (issue #121)
- gh#123: Smarty debug (issue #116)
- gh#124: Bug in group display in user and group base are the same
- gh#125: Group rendering

* Tue Jul 23 2019 - Clement Oudot <clem@ltb-project.org> - 0.3-1
- gh#42: add dropdown list to advanced search criteria
- gh#47: Do not display not found groups/users
- gh#48: Check ldap_bind return code instead of ldap_errorno
- gh#49: Add url link to web ldap editor tool for each users entrie
- gh#50: Provide a way to know the installed version
- gh#51: No information is displayed when opening user details in a multi-organizational DIT
- gh#52: fix(display): introducing optional `$ldap_user_regex`
- gh#54: Hide photo box if there is no picture
- gh#55: Can we get a list of all groups
- gh#58: XSS protection added
- gh#60: Sort group members
- gh#61: Adapt other templates to changes in value_displayer.tpl (ltb-project#47)
- gh#62: Set version in code and display it in footer (ltb-project#50)
- gh#63: Add buttons in directory page to switch between users and groups (ltb-project#55)
- gh#64: Set LDAP debug if $debug is set
- gh#65: Enable debug in php-ldap (ltb-project#64)
- gh#66: Sort values when displaying entry (ltb-project#60)
- gh#68: Possibility to set a specific filter for gallery (ltb-project#54)
- gh#69: Configure default page
- gh#70: Bad quote escaping in advanced search page
- gh#71: Option to add an edit link in entry display page (ltb-project#49)
- gh#72: Sorting and paging regression
- gh#73: Option to display a logout link in the menu
- gh#74: Provide a new type (list)

* Mon Apr 16 2018 - Clement Oudot <clem@ltb-project.org> - 0.2-1
- gh#4: Italian language file
- gh#5: Feature request : add export to CSV
- gh#7: Export entry as VCard
- gh#8: Doc : fix typo in "Installation from tarball"
- gh#10: Directory thumbnail frame are unformatted
- gh#11: Add a menu to display groups (based on groupofmember)
- gh#16: Print results as rows or boxes
- gh#17: Quick search return with pattern like "foo*"
- gh#18: Replace exact matching by substring matching in advanced search
- gh#21: [Security] LDAP Injection in quick search
- gh#22: Possibility to configure photo attribute
- gh#23: Create tel: links for telephone numbers
- gh#24: PHP >= 5.6 prerequisite
- gh#25: New view "directory" which display all entries in a list with datatables
- gh#26: checkboxes in advanced search form for substring matching
- gh#30: Config.inc.php : include local file and document variables
- gh#31: Configure a print button with Datatables
- gh#32: List view directory search
- gh#33: Add config option for autoPrint feature in Datatables
- gh#34: Improve browsing on pages with Datatables
- gh#35: Sort icons should be more close than their column name
- gh#36: Change icon for Directory or Gallery view
- gh#37: Logo not visible on other pages than homepage
- gh#38: Text and look for print buttons
- gh#39: Add display for member/memberOf attributes
- gh#40: Displaying binary data attributes
- gh#41: Move label to title leads to misunderstanding

* Tue Nov 22 2016 - Clement Oudot <clem@ltb-project.org> - 0.1-1
- First release
