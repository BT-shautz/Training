odoo.define('library.Dashboard', function (require) {
    "use strict";

    var Core = require('web.core');
    var Widget = require('web.Widget');
    var ChartWidget = require('library.ChartWidget');
    var QWeb = Core.qweb;
    var _t = Core._t;

    // Represents the top area of a tree, form... where the breadcrumbs, buttons, search bar... are located
    var ControlPanelMixin = require('web.ControlPanelMixin');

    // Creates a new widget WITH a control panel; this widget will provide the desired dashboard
    // The GUI of the widget is defined in the associated template (in our case, the template name is "Dashboard" and it
    // is defined in the "/static/src/xml/dashboard.xml" file)
    var Dashboard = Widget.extend(ControlPanelMixin, {
        template: 'Dashboard',

        // This "events" work only for buttons defined within the current template
        // If a button is defined outside (e.g., within the control panel), this doesn't work! In such a case, the
        // "start" function must be used and manual bindings must be performed (see "start" function below)
        events: {
            'click .btn_lost_rentals': '_get_lost_rentals',
            'click .btn_bad_customers': '_get_bad_customers'
        },

        // This "custom_events" define custom events that can be triggered somewhere within our widget and that the
        // widget can consume in order to execute a particular function
        custom_events: {
            // "open_books" is the name of the event that a "trigger_up" function can call (in particular, this is
            // triggered by the ChartWidget when clicking on a portion of the chart)
            // "_open_books" is the function to be called
            'open_books': '_open_books'
        },

        init: function (parent, action) {
            // The parent of a widget is always the action manager; saves it for later
            this.action_manager = parent;
            this.action = action;

            return this._super.apply(this, arguments);
        },

        willStart: function () {
            //Fetches the data that the widget will need during the rendering process
            var self = this;
            var def1 = this._rpc({route: '/library/statistics'}).then(function (stats) {
                self.stats = stats;
            });
            var def2 = this._super.apply(this, arguments);
            return $.when(def1, def2);
        },

        start: function () {
            // The widget is being rendered

            this._render_buttons();
            this._update_control_panel();
            var def1 = this._render_chart();
            var def2 = this._super.apply(this, arguments);
            return $.when(def1, def2);
        },

        do_show: function () {
            // This function is called if the widget was hidden (e.g., we moved to a linked object) and now it is being
            // shown again (e.g., going back via the breadcrumbs)

            this._super.apply(this, arguments);

            this._render_chart();
            this._update_control_panel();
            this.action_manager.do_push_state({action: this.action.id});
        },

        _render_buttons: function () {
            var self = this;

            // Renders the buttons that will be passed to the control panel
            this.$buttons = $(QWeb.render('DashboardButtons'));

            // Each of the buttons in the "DashboardButtons" template is assigned a click event
            this.$buttons.find('.btn_lost_rentals_cp').click(function () {
                self._get_lost_rentals();
            });
            this.$buttons.find('.btn_bad_customers_cp').click(function () {
                self._get_bad_customers();
            });

            // The two previous click event bindings could have also been achieved as follows:
            // this.$buttons.on('click', '.btn_lost_rentals_cp', this._get_lost_rentals.bind(this));
            // this.$buttons.on('click', '.btn_bad_customers_cp', this._get_bad_customers.bind(this));
        },

        _update_control_panel: function () {
            // Calls the "update_control_panel" function available thanks to "ControlPanelMixin"
            // It receives a dictionary with "breadcrumbs" and "cp_content"
            //  - "breadcrumbs" defines the breadcrumbs
            //  - "cp_content" defines the buttons, the search bar, filters, paging... Here we only define the buttons area
            this.update_control_panel({
                breadcrumbs: this.action_manager.get_breadcrumbs(),
                cp_content: {$buttons: this.$buttons}
            });
        },

        _render_chart: function () {
            var chart_data = {
                nb_available_books: this.stats.nb_available_books,
                nb_rented_books: this.stats.nb_rented_books,
                nb_lost_books: this.stats.nb_lost_books,
            };
            var chart_widget = new ChartWidget(this, chart_data);
            this.$('.o_fancy_chart').empty();
            return chart_widget.appendTo(this.$('.o_fancy_chart'));
        },

        _get_lost_rentals: function (event) {
            // Returns a window action programmatically
            return this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'library.rental',
                name: _t('Lost Rentals'),
                domain: [['state', '=', 'lost']],
                views: [[false, 'list'], [false, 'form']],
                view_type: 'tree,form',
                view_mode: 'form'
            });
        },

        _get_bad_customers: function (event) {
            // Returns a window action defined in an XML file
            return this.do_action('library.action_bad_customer');
        },

        _open_books: function (event) {
            // Function linked to a custom event
            var state = event.data.state;
            var action;

            if (state === 'available') {
                action = 'library.action_available_books';
            } else if (state === 'lost') {
                action = 'library.action_lost_books';
            } else if (state === 'rented') {
                action = 'library.action_rented_books';
            } else {
                this._do_warn('Wrong state');
            }

            // Executes the corresponding window action (defined in an XML file)
            this.do_action(action);
        },
    });

    // Registers the widget in the action registry; we can use then the tag "dashboard" within the definition of a
    // client action
    Core.action_registry.add('dashboard', Dashboard);

    // Returns the created objects (in our case, the Dashboard widget)
    return {
        Dashboard: Dashboard,
    };
});
