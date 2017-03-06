[![Build Status](https://travis-ci.org/drazul/universal-deployer.svg?branch=master)](https://travis-ci.org/drazul/universal-deployer)

# Table of Contents
* [Universal deployer](#universal-deployer)
* [Dependencies](#dependencies)
	* [Dependencies by plugins](#dependencies-by-plugins)
* [Usage](#usage)
	* [Default values](#default-values)
	* [App types](#app-types)
		* [iis_website](#iis_website) 
		* [sc_service](#sc_service) 
		* [nssm_service](#nssm_service) 
		* [curator](#curator) 
		* [databases](#database)
	* [Utilities](#utilities)
		* [Chocolatey](#chocolatey)
* [Writting a new plugin](#writting-a-new-plugin)

# Universal deployer

Universal_deployer is developed to simplify and homogenize the deployment of heterogeneous application types.

With universal_deployer you can:

 * deploy all you applications with one simple command
   (```universal_deployer --deploy all```) instead of execute a specific  and different command by each application type
 * define a configuration file where specify each application to be deployed
 * define different weights on each application to alter deployment order
 * reuse same configuration file for future deployment only changing the version numbers
 * add new plugins to implement new application types easily

# Dependencies

You need install all dependencies listed on requeriment.txt file as follow
```bash
pip install -r requirements.txt -t .
```

And you need install some extra dependencies if you use some plugins

## Dependencies by plugins
* chocolatey: go to [chocolatey.org](https://chocolatey.org) and download latest version

* iis_website: you need enable IIS from windows features
* nssm_service: ```choco install nssm```
* curator: ```pip install elasticsearch-curator -t . ```
* database: ```choco install liquibase``` You also need add jdbc plugin to liquibase installation


# Usage

You need to define a yaml file with the deployment configuration. You can find an explanation in following lines

```yaml
config:                           # <-- global configuration accesible by all apps
  config_path: /etc/config_path   # <-- config path where load config templates
  install_path: /opt/install_path # <-- install path where to be deployed all apps
  environment: production         # <-- you can declare you own configuration

apps:
  app_type:             # <-- define the application tipe used to instantiate a class defined on plugins folder
    weight: 100         # <-- define deployment order for all apps on app_type
    app_name:           # <-- application name, used on iis
      weight: 110       # <-- define deployment order or this app
      version: 0.0.3    # <-- version to be deployed
      pkg_name: ex_pkg  # <-- package to be downloaded and deployed
      params:           # <-- map where store specific values needed for that app_type
```
## Default values

  * config_path   --> [C:]/etc/universal-deployer
  * install_path  --> [C:]/opt/universal-deployer
  * backup_path   --> [C:]/opt/universal-deployer-backups
  * backup        --> False
  * weight        --> 0 (zero) on all apps
  * log           --> level INFO and writed on console

## App types

### iis_website

IIS is a Windows Web Server used to serve .net apps

```yaml
apps:
  iis_website:
    frontend_app:
      pkg_name: frontend_pkg
      version: 1.0.2.5
      params:
        webconfig:  # <-- key/value to be stored on webconfig/settings
          swaggerBasePath: api/client
          schema: https
        replace:    # <-- values to be replaced on files
          file_pattern: '*endpoints.js'
          patterns:
            'usersapi': 'usersapi.example.com'
            'gamesapi': 'example.com/gamesapi'
```

### sc_service

SC is a windows application used to configure windows services

```yaml
apps:
  sc_service:
    service_app:
      pkg_name: sc_service_app
      version: 1.2.0.18
      params:
        executable: service.exe
```

### nssm_service

NSSM is a utility to simplify the windows service management

```yaml
apps:
  nssm_service:
    nssm_service_app:
      pkg_name: nssm_service_app
      version: 1.2.0.6
      params:
        executable: service.exe
        arguments: '--debug'
```

### curator

curator is a aplication created by elastic.co to perform some tasks on elasticsearch cluster, like create indices and alias or delete old data

```yaml
apps:
  curator:
    rc_elasticsearch_schema:
      pkg_name: elasticsearch_schema
      version: 1.2.0.18
```

### databases

database type use liquibase as version control

```yaml
apps:
  databases:
    audit:
      pkg_name: audit_database
      version: 1.2.0.18
      params:
        create_database: False  # <-- in some cases (as Azure databases) scripts cannot create new databases
        host: database.VM1
        database_name: audit
        arguments: '-DNODEID=1' # <-- values to be deplaced by liquibase on changelog files
        contexts: demo          # <-- liquibase execute changelogs only on specific contexts
```

## Utilities

###Chocolatey


Chocolatey is a packet manager for windows that use nuget packages. Chocolatey is used on some app types classes to download packages. 

#####Notes:
* At default chocolatey only download specified packages and don't execute powershell attached scripts. 
* At default chocolatey try to download from all configured sources, but you can specify one repository to use to download 
```yaml
config:
  choco_source: http://example.org
```

#Writting a new plugin

To write a new plugin you just need to create a class with the same name that application type you define and inherit from application_deployer class located [here](/plugins/application_deployer.py).

Now you should overwrite methods you need to implement the requeriment functionallity in order to homogeinize the deployment steps.

You can see some examples on [/plugins](/plugins) path.