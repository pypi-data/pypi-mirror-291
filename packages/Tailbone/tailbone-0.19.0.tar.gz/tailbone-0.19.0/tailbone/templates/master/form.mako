## -*- coding: utf-8; -*-
<%inherit file="/form.mako" />

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ## declare extra data needed by form
    % if form is not Undefined and getattr(form, 'json_data', None):
        % for key, value in form.json_data.items():
            ${form.component_studly}Data.${key} = ${json.dumps(value)|n}
        % endfor
    % endif

    % if master.deletable and instance_deletable and master.has_perm('delete') and getattr(master, 'delete_confirm', 'full') == 'simple':

        ThisPage.methods.deleteObject = function() {
            if (confirm("Are you sure you wish to delete this ${model_title}?")) {
                this.$refs.deleteObjectForm.submit()
            }
        }

    % endif
  </script>

  % if form is not Undefined and hasattr(form, 'render_included_templates'):
      ${form.render_included_templates()}
  % endif

</%def>


${parent.body()}
