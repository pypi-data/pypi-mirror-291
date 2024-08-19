## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="title()">${index_title}</%def>

## nb. avoid hero bar for index page
<%def name="content_title()"></%def>

<%def name="page_content()">
  % if grid is not Undefined:
      ${grid.render_vue_tag()}
  % endif
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}
  % if grid is not Undefined:
      ${grid.render_vue_template()}
  % endif
</%def>

<%def name="finalize_this_page_vars()">
  ${parent.finalize_this_page_vars()}
  % if grid is not Undefined:
      <script>
        ${grid.vue_component}.data = function() { return ${grid.vue_component}Data }
        Vue.component('${grid.vue_tagname}', ${grid.vue_component})
      </script>
  % endif
</%def>

${parent.body()}
