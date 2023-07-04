# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.1] - 2023-07-04
### Fixed
- failed authentication when custom_API_key is empty (#4) @Geniucker  
- unable to use host proxy when using Docker in Linux (#5) @Geniucker  
- response body is not complete (#7) @Geniucker  


## [2.1.0] - 2023-07-01
### Added
- support for https  


## [2.0.0] - 2020-06-30

### Added
- support for authentication for custom API key  

### Fixed
- the condition of expiration of access_token  


## earlier versions
### Features
- automatically retrieve access_token using emails and passwords, and automatically refreshes the access_token upon expiration (only applicable for email password login  
- easy to deploy  