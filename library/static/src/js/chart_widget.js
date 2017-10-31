odoo.define('library.ChartWidget', function (require) {
    "use strict";

    var Ajax = require('web.ajax');
    var Widget = require('web.Widget');


    var ChartWidget = Widget.extend({
        tagName: 'canvas',

        // The JS library in charge of rendering the pie chart (used later via "Ajax.loadLibs(...)")
        jsLibs: ['/library/static/lib/chart.js/Chart.js'],

        init: function (parent, data) {
            this._super.apply(this, arguments);

            // This data is provided by the Dashboard widget
            this.data = data;
        },

        willStart: function () {
            // Lazy-loads the required JS libs
            return $.when(Ajax.loadLibs(this), this._super.apply(this, arguments));
        },

        start: function () {
            // Renders the chart
            this._renderChart();
            return this._super.apply(this, arguments);
        },

        _renderChart: function () {
            var self = this;
            new Chart(this.el, {
                type: 'pie',
                data: {
                    labels: ["Available", "Rented", "Lost"],
                    datasets: [{
                        label: '# of Books',
                        data: [
                            this.data.nb_available_books,
                            this.data.nb_rented_books,
                            this.data.nb_lost_books,
                        ],
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 99, 132, 0.2)',
                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255,99,132,1)',
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    onClick: function (event, chart_elements) {
                        var types = ['available', 'rented', 'lost'];
                        if (chart_elements && chart_elements.length) {
                            // Triggers an action named "open_books" that should be captured by the Dashboard widget
                            // As args a dictionary is sent where the state of the books to be opened is provided
                            self.trigger_up('open_books', {state: types[chart_elements[0]._index]});
                        }
                    },
                },
            });
        },
    });

    return ChartWidget;
});
