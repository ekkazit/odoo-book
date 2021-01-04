odoo.define('purchase_request.counter', function (require) {
    var Widget = require('web.Widget');
    var Counter = Widget.extend({
        template: 'my_counter_template',
        events: {
            'click #btnMinus': '_onDecrement',
            'click #btnPlus': '_onIncrement',
        },
        init: function (parent) {
            this._super(parent);
            this.count = 0;
        },
        _onDecrement: function () {
            this.count--;
            this.$('#result').text(this.count);
        },
        _onIncrement: function () {
            this.count++;
            this.$('#result').text(this.count);
        },
    });
    return Counter;
});

odoo.define('purchase_request.dashboard', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var Counter = require('purchase_request.counter');

    var Dashboard = AbstractAction.extend({
        template: 'my_dashboard_template',
        xmlDependencies: ['/purchase_request/static/src/xml/dashboard.xml'],
        jsLibs: ['/purchase_request/static/src/js/Chart.js'],
        init: function(parent, context) {
            this._super(parent, context);
        },
        start: function() {
            this.counter = new Counter(this);
            this.counter.appendTo(this.$('#my_counter'));
        },
    });

    core.action_registry.add('my_dashboard_action', Dashboard);
    return Dashboard;
});
