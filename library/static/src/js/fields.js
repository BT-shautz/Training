odoo.define('library.Fields', function (require) {
    "use strict";

    var BasicFields = require('web.basic_fields');
    var FieldRegistry = require('web.field_registry');
    var Core = require('web.core');
    var QWeb = Core.qweb;
    var Widget = require('web.Widget');
    var SysTrayMenu = require('web.SystrayMenu');

    var FieldRawInteger = BasicFields.FieldInteger.extend({
        init: function (parent, data) {
            return this._super.apply(this, arguments);
        },

        _formatValue: function (value) {
            return value; // Returns the value as it comes; it is the parent who formats it
        },
    });

    var FieldColorBoolean = BasicFields.FieldBoolean.extend({
        // Gives a class to the root element of the widget; it is used in the LESS file to format the root element
        className: 'o_field_color_boolean',

        // Captures the click event performed on the widget and executes the "_onClick" function
        events: {
            'click': '_onClick'
        },

        init: function () {
            this._super.apply(this, arguments);

            // Reads the widget options provided in the view (if any) and saves them for later
            this.true_color = this.nodeOptions.true_color || 'green';
            this.false_color = this.nodeOptions.false_color || 'red';
        },

        _render: function () {
            // Changes the background color of the widget accordingly
            // This actually has an effect because our widget has been classed above and a fixed width and height have
            // been provided
            this.$el.html($('<div>').css({
                backgroundColor: this.value ? this.true_color : this.false_color
            }));
        },

        _onClick: function (event) {
            // Toggles the value if we are in edit mode
            // This action will cause the "_render" function to be called
            if (this.mode == 'edit') {
                this._setValue(!this.value);
            }
        }
    });

    var FieldFloatLibraryWarning = BasicFields.FieldFloat.extend({
        _renderReadonly: function () {
            if (this.value > 0) {
                this.$el.html(QWeb.render('FieldFloatLibraryWarning', {amount: this.value}));
            } else {
                this.$el.empty();
            }
        },
    });

    // This widget creates a text box in the system tray (top bar, right area, where the logged-in user is)
    var FieldSysTray = Widget.extend({
        template: 'FieldSysTray',

        // Indicates where in the sys tray the widget must appear
        sequence: 10,

        // The "input" event refers to the typing of one character
        events: {
            'input .o_input': '_onInput'
        },

        _onInput: function () {
            var customer_id = parseInt(this.$('.o_input').val());

            if (!_.isNaN(customer_id)) {
                // TODO: verify that the customer id exists
                this.do_action('library.action_customer_form', {
                    res_id: customer_id,
                });
            }
        },
    });

    // Registers the new field widgets in the field registry; we can use then the tags "raw-integer", "color-boolean"...
    // within views: <field name="a_field" widget="raw-integer"/>
    FieldRegistry
        .add('raw-integer', FieldRawInteger)
        .add('color-boolean', FieldColorBoolean)
        .add('float-library-warning', FieldFloatLibraryWarning);

    // Registers the systray widget in the systray menu
    // This will make our widget visible in the right area within top bar (near the logged-in name)
    SysTrayMenu.Items.push(FieldSysTray);

    // Returns the created objects (in our case, the Dashboard widget)
    return {
        FieldRawInteger: FieldRawInteger,
        FieldColorBoolean: FieldColorBoolean,
        FieldFloatLibraryWarning: FieldFloatLibraryWarning
    };
});
