## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="page_content()">
  <div style="margin-top: 2rem; width: 50%;">
    % if form is not Undefined:
        ${form.render_vue_tag()}
    % endif
  </div>
</%def>

<%def name="render_vue_templates()">
  ${parent.render_vue_templates()}
  % if form is not Undefined:
      ${form.render_vue_template()}
  % endif
</%def>

<%def name="make_vue_components()">
  ${parent.make_vue_components()}
  % if form is not Undefined:
      ${form.render_vue_finalize()}
  % endif
</%def>
