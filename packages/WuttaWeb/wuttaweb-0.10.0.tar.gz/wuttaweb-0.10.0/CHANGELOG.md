
# Changelog
All notable changes to wuttaweb will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v0.10.0 (2024-08-18)

### Feat

- add multi-column sorting (frontend or backend) for grids

### Fix

- improve grid display when data is empty

## v0.9.0 (2024-08-16)

### Feat

- add backend pagination support for grids
- add initial/basic pagination for grids

## v0.8.1 (2024-08-15)

### Fix

- improve backward compat for `util.get_liburl()`

## v0.8.0 (2024-08-15)

### Feat

- add form/grid label auto-overrides for master view

### Fix

- add `person` to template context for `PersonView.view_profile()`

## v0.7.0 (2024-08-15)

### Feat

- add sane views for 403 Forbidden and 404 Not Found
- add permission checks for menus, view routes
- add first-time setup page to create admin user
- expose User password for editing in master views
- expose Role permissions for editing
- expose User "roles" for editing
- improve widget, rendering for Role notes

### Fix

- add stub for `PersonView.make_user()`
- allow arbitrary kwargs for `Form.render_vue_field()`
- make some tweaks for better tailbone compatibility
- prevent delete for built-in roles

## v0.6.0 (2024-08-13)

### Feat

- add basic Roles view
- add Users view; improve CRUD master for SQLAlchemy models
- add People view; improve CRUD master for SQLAlchemy models
- add basic support for SQLAlchemy model in master view
- add basic Create support for CRUD master view
- add basic Delete support for CRUD master view
- add basic Edit support for CRUD master view
- add auto-link (to "View") behavior for grid columns
- add basic support for "view" part of CRUD
- add basic `Grid` class, and /settings master view

### Fix

- rename MasterView method to `configure_grid()`
- replace default logo, favicon images
- tweak labels for Web Libraries config

## v0.5.0 (2024-08-06)

### Feat

- add basic support for fanstatic / libcache
- expose Web Libraries in app info config page
- add basic configure view for appinfo

### Fix

- bump min version for wuttjamaican

## v0.4.0 (2024-08-05)

### Feat

- add basic App Info view (index only)
- add initial `MasterView` support

### Fix

- add `notfound()` View method; auto-append trailing slash
- bump min version for wuttjamaican

## v0.3.0 (2024-08-05)

### Feat

- add support for admin user to become / stop being root
- add view to change current user password
- add basic logo, favicon images
- add auth views, for login/logout
- add custom security policy, login/logout for pyramid
- add `wuttaweb.views.essential` module
- add initial/basic forms support
- add `wuttaweb.db` module, with `Session`
- add `util.get_form_data()` convenience function

### Fix

- allow custom user getter for `new_request_set_user()` hook

## v0.2.0 (2024-07-14)

### Feat

- add basic support for menu handler

- add "web handler" feature; it must get the menu handler

## v0.1.0 (2024-07-12)

### Feat

- basic support for WSGI app, views, templates
