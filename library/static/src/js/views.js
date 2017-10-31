odoo.define('library.Views', function (require) {
    "use strict";

    var Core = require('web.core');
    var BasicModel = require('web.BasicModel');
    var ViewRegistry = require('web.view_registry');
    var QWeb = Core.qweb;
    var _lt = Core._lt;

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var FormView = require('web.FormView');

    var KanbanController = require('web.KanbanController');
    var KanbanRenderer = require('web.KanbanRenderer');
    var KanbanView = require('web.KanbanView');
    var KanbanModel = require('web.KanbanModel');

    // Form controller for new form view defined later
    var LibraryCustomerController = FormController.extend({
        renderButtons: function ($node) {
            var self = this;
            this._super.apply(this, arguments);

            // Renders our custom buttons and appends them to the existing buttons
            var $libraryButtons = $(QWeb.render('LibraryCustomerButtons'));
            this.$buttons.find('.o_form_buttons_view').append($libraryButtons);

            // Binds click events to each of our custom button
            this.$buttons.on('click', '.o_geolocate', function () {
                self._onGeolocateClick();
            });
            this.$buttons.on('click', '.o_pay_amount', function () {
                // Disables the button
                // TODO: However, if we reload the page, the button appears enabled again; maybe we should override the
                // "start" method and see if we can get the "amount_owed" value needed to perform the condition
                $(this).attr('disabled', true);
                self._onPayAmountClick();
            });
        },

        _update: function (state) {
            if (this.$buttons) {
                var $payButton = this.$buttons.find('.o_pay_amount');
                $payButton.attr('disabled', state.data.amount_owed <= 0);
            }
            return this._super(state);
        },

        _onGeolocateClick: function () {
            var self = this;
            var res_id = this.model.get(this.handle, {raw: true}).res_id;
            this._rpc({
                model: 'res.partner',
                method: 'geo_localize',
                args: [res_id]
            }).then(function () {
                self.reload();
            });
        },

        _onPayAmountClick: function () {
            var self = this;
            var res_id = this.model.get(this.handle, {raw: true}).res_id;
            this._rpc({
                model: 'res.partner',
                method: 'pay_amount',
                args: [res_id]
            }).then(function () {
                self.reload();
            });
        },
    });

    // Creates a new form view that will be controlled by the controller defined above
    var LibraryCustomerView = FormView.extend({
        config: {
            Model: BasicModel,
            Renderer: FormRenderer,
            Controller: LibraryCustomerController // This is the only custom config
        },
    });

    // Kanban controller for new kanban view defined later
    var LibraryRentalController = KanbanController.extend({
        events: {
            'click .o_customer': '_onCustomerClicked',
        },

        willStart: function () {
            var def1 = this._super.apply(this, arguments);
            var def2 = this._loadCustomers();
            return $.when(def1, def2);
        },

        reload: function (params) {
            if (this.activeCustomerID) {
                params = params || {};
                // TODO: The domain should be extended, not replaced
                params.domain = [['customer_id', '=', this.activeCustomerID]];
            }
            var def1 = this._super(params);
            var def2 = this._loadCustomers();
            return $.when(def1, def2);
        },

        _loadCustomers: function () {
            var self = this;
            return this._rpc({
                route: '/web/dataset/search_read',
                model: 'res.partner',
                fields: ['display_name'],
                limit: 80,
            }).then(function (result) {
                self.customers = result.records;
            });
        },

        _update: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$('.o_kanban_view').prepend(QWeb.render('CustomerList', {
                    activeCustomerID: self.activeCustomerID,
                    customers: self.customers,
                }));
            });
        },

        _onCustomerClicked: function (ev) {
            this.activeCustomerID = $(ev.currentTarget).data('id');
            this.reload();
        },
    });

    var LibraryRentalView = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: KanbanModel,
            Renderer: KanbanRenderer,
            Controller: LibraryRentalController,
        }),
        display_name: _lt('Library Kanban'),
        icon: 'fa-th-list',
    });

    // Registers the new form view in the view registry so that it can be used in form views:
    //   <form js_class="library_customer"/>
    ViewRegistry.add('library_customer', LibraryCustomerView);
    ViewRegistry.add('library_rental', LibraryRentalView);
});
