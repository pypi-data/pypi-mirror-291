## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    % if custorder_xref_markers_data is not Undefined:
        ${form.component_studly}Data.custorderXrefMarkersData = ${json.dumps(custorder_xref_markers_data)|n}
    % endif

  </script>
</%def>

${parent.body()}
