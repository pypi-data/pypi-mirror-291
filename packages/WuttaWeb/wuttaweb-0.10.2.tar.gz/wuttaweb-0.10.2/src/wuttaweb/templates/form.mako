## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="page_content()">
  <div style="margin-top: 2rem; width: 50%;">
    % if form is not Undefined:
        ${form.render_vue_tag()}
    % endif
  </div>
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}
  % if form is not Undefined:
      ${form.render_vue_template()}
  % endif
</%def>

<%def name="finalize_this_page_vars()">
  ${parent.finalize_this_page_vars()}
  % if form is not Undefined:
      ${form.render_vue_finalize()}
  % endif
</%def>


${parent.body()}
