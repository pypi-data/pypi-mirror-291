## -*- coding: utf-8; -*-
## ##############################################################################
## 
## Default master 'versions' template, for showing an object's version history.
## 
## ##############################################################################
<%inherit file="/page.mako" />

<%def name="title()">${model_title_plural} » ${instance_title} » history</%def>

<%def name="content_title()">
  Version History
</%def>

<%def name="render_this_page()">
  ${self.page_content()}
</%def>

<%def name="make_this_page_component()">
  ${parent.make_this_page_component()}
  <script type="text/javascript">

    TailboneGrid.data = function() { return TailboneGridData }

    Vue.component('tailbone-grid', TailboneGrid)

  </script>
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}

  ## TODO: stop using |n filter
  ${grid.render_complete()|n}
</%def>

<%def name="page_content()">
  <tailbone-grid :csrftoken="csrftoken">
  </tailbone-grid>
</%def>

${parent.body()}
