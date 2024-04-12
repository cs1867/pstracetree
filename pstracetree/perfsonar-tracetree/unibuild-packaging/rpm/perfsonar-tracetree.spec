%define install_base        /usr/lib/perfsonar/
%define pstt_bin_base       %{install_base}/bin
%define command_base        %{pstt_bin_base}/pstracetree_commands
%define config_base         /etc/perfsonar
%define pstt_config_base    %{config_base}/pstracetree
%define doc_base            /usr/share/doc/perfsonar/pstracetree
%define pstt_web_dir        %{install_base}/pstracetree

%define apacheconf      apache-perfsonar-tracetree.conf

#Version variables set by automated scripts
%define perfsonar_auto_version 5.1.0
%define perfsonar_auto_relnum alfa1

%define release_only  %{perfsonar_auto_relnum}

Name:			perfsonar-tracetree
Version:		%{perfsonar_auto_version}
Release:		%{perfsonar_auto_relnum}%{?dist}
Summary:		perfSONAR graphical traceroute tree viewer
License:		ASL 2.0
Group:			Development/Libraries
URL:			http://www.perfsonar.net
Source0:		perfsonar-tracetree-%{version}.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:		noarch
Requires:		httpd
Requires:               mod_ssl
Requires:               perl
Requires:               perl(CGI)
Requires:               perl(Config::General)
Requires:               perl(Log::Log4perl)
Requires:               perl(Net::IP)
Requires:               perl(Params::Validate)
Requires:               perl(Data::Dumper)
Requires:               perl(JSON)
Requires:               perl(HTTP::Tiny)
Requires:               ca-certificates
Requires:               js-jquery
Requires:               js-jquery-ui
Requires:               sorttablejs
Requires:               visjs


%description
perfSONAR tracetree provides a web based graphical viewer of
traceroute measuremets from perfSONAR archives. Routes are
presented as  a node graph as well as a summrized table.

%prep
%setup -q

%install
rm -rf %{buildroot}
make ROOTPATH=%{buildroot}/%{pstt_web_dir} CONFIGPATH=%{buildroot}/%{config_base} install

mkdir -p %{buildroot}/etc/httpd/conf.d
install -D -m 0644 %{buildroot}/%{config_base}/%{apacheconf} %{buildroot}/etc/httpd/conf.d/%{apacheconf}
install -D -m 0755 -t %{buildroot}/%{command_base} %{buildroot}/%{pstt_web_dir}/bin/* 
rm -rf %{buildroot}/%{pstt_web_dir}/bin
rm -rf %{buildroot}/%{config_base}/%{apacheconf}

%clean
rm -rf %{buildroot}

%post
if [ ! -f /etc/pki/tls/certs/localhost.crt ]; then
    # Selfsign cert missing. Generate one.
    openssl req -newkey rsa:2048 -nodes -keyout /etc/pki/tls/private/localhost.key -x509 -days 365 -out /etc/pki/tls/certs/localhost.crt -subj "/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN=example.com"
fi
service httpd restart &> /dev/null || :
# Make jquery and jquery-ui available
ln -s /usr/share/javascript/jquery/latest/jquery.min.js %{pstt_web_dir}/js/jquery.min.js
ln -s /usr/share/javascript/jquery/latest/jquery.min.map %{pstt_web_dir}/js/jquery.min.map
ln -s /usr/share/javascript/jquery-ui/jquery-ui.min.js %{pstt_web_dir}/js/jquery-ui.min.js
ln -s /usr/share/javascript/jquery-ui/jquery-ui.min.css %{pstt_web_dir}/css/jquery-ui.min.css
ln -s /usr/share/javascript/jquery-ui/images %{pstt_web_dir}/css/images

# Make visjs available
ln -s /usr/share/javascript/visjs/4.21.0/vis.js   %{pstt_web_dir}/js/vis.js
ln -s /usr/share/javascript/visjs/4.21.0/vis.css   %{pstt_web_dir}/css/vis.css
ln -s /usr/share/javascript/visjs/4.21.0/img   %{pstt_web_dir}/css/img 
ln -s /usr/share/javascript/visjs/4.21.0/vis-timeline-graph2d.min.css   %{pstt_web_dir}/css/vis-timeline-graph2d.min.css
# Make sorttable available
ln -s /usr/share/javascript/sorttable/v2/sorttable.js %{pstt_web_dir}/js/sorttable.js

%files
%defattr(0644,perfsonar,perfsonar,0755)
%license %{pstt_web_dir}/LICENSE
%attr(0644,perfsonar,perfsonar) %{pstt_web_dir}/js/*
%attr(0644,perfsonar,perfsonar) %{pstt_web_dir}/css/*
%attr(0644,perfsonar,perfsonar) %{pstt_web_dir}/img/*
%attr(0755,perfsonar,perfsonar) %{command_base}/*
%attr(0644,perfsonar,perfsonar) %{pstt_web_dir}/*.html
%attr(0644,perfsonar,perfsonar) /etc/httpd/conf.d/%{apacheconf}

%changelog
* Thu Feb 15 2024 Otto.Wittner@sikt.no 5.1.0-1-alfa
- Restructuring and misc cleaning
* Mon Dec 10 2018 Valentin.Vidic@CARNet.hr 4.1-0.0.a1
- Initial packaging
