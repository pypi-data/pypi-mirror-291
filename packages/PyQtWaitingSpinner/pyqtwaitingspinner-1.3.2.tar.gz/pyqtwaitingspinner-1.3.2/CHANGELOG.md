# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 1.3.2 - 2024-08-20
### Fixed
- **[Configurator]** A exception when serializing to yaml while saving a spinner to a .yaml file.

## 1.3.1 - 2024-08-10
### Added
- **[parameters.py]** Added `parameters.from_file` as an alias for `parameters.load_yaml()`

### Changed
- **[parameters.py]** Renamed `parameters.from_file()` to `parameters.load_yaml()`.

## 1.3.0 - 2024-08-10
### Added
- This CHANGELOG
- **[WaitingSpinner]** can now rotate both clockwise and counterclockwise by setting an appropriate value to `SpinnerParameters.spin_direction`.
- **[Configurator]** Added a ComboBox for selecting either [CLOCKWISE] or [COUNTERCLOCKWISE] spin directions.
