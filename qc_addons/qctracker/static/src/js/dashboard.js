odoo.define('qctracker.dashboard', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');

    var QCTrackerDashboard = AbstractAction.extend({
        template: 'qctracker_dashboard_template',

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._renderChart();
            });
        },

        _renderChart: function () {
            var ctx = document.getElementById('tasksChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Completed', 'Pending', 'Ongoing'],
                    datasets: [{
                        data: [
                            this.$el.find('[name="completed_tasks_count"]').text(),
                            this.$el.find('[name="pending_tasks_count"]').text(),
                            this.$el.find('[name="ongoing_projects_count"]').text()
                        ],
                        backgroundColor: ['#28a745', '#ffc107', '#17a2b8']
                    }]
                },
                options: {
                    animation: {
                        animateRotate: true,
                        animateScale: true
                    },
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    });

    core.action_registry.add('qctracker.dashboard', QCTrackerDashboard);
    return QCTrackerDashboard;
});
