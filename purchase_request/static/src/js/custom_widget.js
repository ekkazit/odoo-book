odoo.define('purchase_request.custom_widget', function (require) {
    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');

    var LabelStatusWidget = AbstractField.extend({
        _render: function () {
            var cssClass = 'status-default';
            if (this.value === 'approve') {
                cssClass = 'status-success';
            } else if (this.value === 'cancel') {
                cssClass = 'status-danger';
            }
            this.$el.html('<span class="' + cssClass + '">' + this.value + '</span>');
        }
    });

    var FormRenderer = require('web.FormRenderer');
    FormRenderer.include({
        autofocus: function () {
            var self = this.state;
            window.$('.o_form_button_edit').show();

            if(self.model === 'pr.pr'){
                var state = self.data.state;
                if(state == 'approve' || state == 'cancel') {
                    window.$('.o_form_button_edit').hide();
                }
            }
            return this._super();
        },
    });

    registry.add('labelstatus', LabelStatusWidget)

    return {
        LabelStatusWidget: LabelStatusWidget,
    }
});
