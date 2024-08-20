# Changelog

All significant changes made to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.2] - 2024-08-19

### Added

- **Disable user privacy**: The ability to explicitly control whether user information is saved. By default, user information is not saved to ensure privacy. However, this can be overridden by setting `privacy=False` in the `start_bot` function: `start_bot(token=TOKEN, ..., privacy=False)`.

### Planned Features

- **Scheduling Enhancements**: Introduce new functions to schedule actions with frequencies other than daily.
- **Enhanced Message Handling**: Implement support for multiple types of messages beyond text.
- **User Statistics Command**: Develop a Telegram command to return user statistics and graphs, such as active users and new users.

## [0.1.1] - 2024-08-17

### Added

- Fully functional main feature.

### Fixed

- Fixed a critical issue that caused an import error when the library was used.

## [0.1.0] - 2024-08-07 [RETRACTED]

### Added

- Initial version of the library.

> **Note:** This version was retracted from PyPI due to a critical issue that caused an import error, making the library unusable.
