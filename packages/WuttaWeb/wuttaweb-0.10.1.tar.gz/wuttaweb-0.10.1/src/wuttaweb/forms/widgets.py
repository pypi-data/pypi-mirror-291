# -*- coding: utf-8; -*-
################################################################################
#
#  wuttaweb -- Web App for Wutta Framework
#  Copyright © 2024 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Form widgets

This module defines some custom widgets for use with WuttaWeb.

However for convenience it also makes other Deform widgets available
in the namespace:

* :class:`deform:deform.widget.Widget` (base class)
* :class:`deform:deform.widget.TextInputWidget`
* :class:`deform:deform.widget.TextAreaWidget`
* :class:`deform:deform.widget.PasswordWidget`
* :class:`deform:deform.widget.CheckedPasswordWidget`
* :class:`deform:deform.widget.SelectWidget`
* :class:`deform:deform.widget.CheckboxChoiceWidget`
"""

import colander
from deform.widget import (Widget, TextInputWidget, TextAreaWidget,
                           PasswordWidget, CheckedPasswordWidget,
                           SelectWidget, CheckboxChoiceWidget)
from webhelpers2.html import HTML

from wuttaweb.db import Session


class ObjectRefWidget(SelectWidget):
    """
    Widget for use with model "object reference" fields, e.g.  foreign
    key UUID => TargetModel instance.

    While you may create instances of this widget directly, it
    normally happens automatically when schema nodes of the
    :class:`~wuttaweb.forms.schema.ObjectRef` (sub)type are part of
    the form schema; via
    :meth:`~wuttaweb.forms.schema.ObjectRef.widget_maker()`.

    In readonly mode, this renders a ``<span>`` tag around the
    :attr:`model_instance` (converted to string).

    Otherwise it renders a select (dropdown) element allowing user to
    choose from available records.

    This is a subclass of :class:`deform:deform.widget.SelectWidget`
    and uses these Deform templates:

    * ``select``
    * ``readonly/objectref``

    .. attribute:: model_instance

       Reference to the model record instance, i.e. the "far side" of
       the foreign key relationship.

       .. note::

          You do not need to provide the ``model_instance`` when
          constructing the widget.  Rather, it is set automatically
          when the :class:`~wuttaweb.forms.schema.ObjectRef` type
          instance (associated with the node) is serialized.
    """
    readonly_template = 'readonly/objectref'

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


class NotesWidget(TextAreaWidget):
    """
    Widget for use with "notes" fields.

    In readonly mode, this shows the notes with a background to make
    them stand out a bit more.

    Otherwise it effectively shows a ``<textarea>`` input element.

    This is a subclass of :class:`deform:deform.widget.TextAreaWidget`
    and uses these Deform templates:

    * ``textarea``
    * ``readonly/notes``
    """
    readonly_template = 'readonly/notes'


class WuttaCheckboxChoiceWidget(CheckboxChoiceWidget):
    """
    Custom widget for :class:`python:set` fields.

    This is a subclass of
    :class:`deform:deform.widget.CheckboxChoiceWidget`, but adds
    Wutta-related params to the constructor.

    :param request: Current :term:`request` object.

    :param session: Optional :term:`db session` to use instead of
       :class:`wuttaweb.db.Session`.

    It uses these Deform templates:

    * ``checkbox_choice``
    * ``readonly/checkbox_choice``
    """

    def __init__(self, request, session=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.config = self.request.wutta_config
        self.app = self.config.get_app()
        self.session = session or Session()


class RoleRefsWidget(WuttaCheckboxChoiceWidget):
    """
    Widget for use with User
    :attr:`~wuttjamaican:wuttjamaican.db.model.auth.User.roles` field.

    This is a subclass of :class:`WuttaCheckboxChoiceWidget`.
    """

    def serialize(self, field, cstruct, **kw):
        """ """
        # special logic when field is editable
        readonly = kw.get('readonly', self.readonly)
        if not readonly:

            # but does not apply if current user is root
            if not self.request.is_root:
                auth = self.app.get_auth_handler()
                admin = auth.get_role_administrator(self.session)

                # prune admin role from values list; it should not be
                # one of the options since current user is not admin
                values = kw.get('values', self.values)
                values = [val for val in values
                          if val[0] != admin.uuid]
                kw['values'] = values

        # default logic from here
        return super().serialize(field, cstruct, **kw)


class PermissionsWidget(WuttaCheckboxChoiceWidget):
    """
    Widget for use with Role
    :attr:`~wuttjamaican:wuttjamaican.db.model.auth.Role.permissions`
    field.

    This is a subclass of :class:`WuttaCheckboxChoiceWidget`.  It uses
    these Deform templates:

    * ``permissions``
    * ``readonly/permissions``
    """
    template = 'permissions'
    readonly_template = 'readonly/permissions'

    def serialize(self, field, cstruct, **kw):
        """ """
        kw.setdefault('permissions', self.permissions)

        if 'values' not in kw:
            values = []
            for gkey, group in self.permissions.items():
                for pkey, perm in group['perms'].items():
                    values.append((pkey, perm['label']))
            kw['values'] = values

        return super().serialize(field, cstruct, **kw)
