/*odoo.define('qctracker.employee_scripts', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var EmployeeWidget = Widget.extend({
        events: {
            'click .qctracker-kanban-card': '_onKanbanCardClick',
            'mouseenter .qctracker-notebook .nav-link': '_onTabHover',
        },

        start: function () {
            this._super.apply(this, arguments);
            this._animateFields();
        },

        _animateFields: function () {
            $('.qctracker-employee-form .form-control').each(function () {
                $(this).on('focus', function () {
                    $(this).addClass('animate__animated animate__tada');
                }).on('blur', function () {
                    $(this).removeClass('animate__animated animate__tada');
                });
            });
        },

        _onKanbanCardClick: function (ev) {
            $(ev.currentTarget).addClass('animate__animated animate__pulse');
            setTimeout(function () {
                $(ev.currentTarget).removeClass('animate__animated animate__pulse');
            }, 1000);
        },

        _onTabHover: function (ev) {
            $(ev.currentTarget).addClass('animate__animated animate__bounceIn');
            setTimeout(function () {
                $(ev.currentTarget).removeClass('animate__animated animate__bounceIn');
            }, 500);
        },
    });

    core.action_registry.add('qctracker.employee_scripts', EmployeeWidget);
    return EmployeeWidget;
});*/
odoo.define('qctracker.employee_scripts', function (require) {
    "use strict";

    var core = require('web.core');

    core.action_registry.add('qctracker_employee_scripts', function () {
        // Form Input Animation
        $('.qctracker-employee-form .form-control').on('focus', function () {
            $(this).addClass('animate__animated animate__tada');
            $(this).on('blur', function () {
                $(this).removeClass('animate__animated animate__tada');
            });
        });

        // Kanban Card Click Animation
        $('.qctracker-kanban-card').on('click', function () {
            $(this).addClass('animate__animated animate__pulse');
            setTimeout(() => {
                $(this).removeClass('animate__animated animate__pulse');
            }, 1000);
        });

        // Notebook Tab Hover Animation
        $('.qctracker-notebook .nav-link').on('mouseenter', function () {
            $(this).addClass('animate__animated animate__bounceIn');
        }).on('mouseleave', function () {
            $(this).removeClass('animate__animated animate__bounceIn');
        });

        // Menu Hover and Click Animation
        $('.o_menu_sections .o_menu_entry').on('mouseenter', function () {
            $(this).addClass('animate__animated animate__pulse');
        }).on('mouseleave', function () {
            $(this).removeClass('animate__animated animate__pulse');
        });

        // Submenu Toggle Animation
        $('.o_menu_sections .dropdown-toggle').on('click', function () {
            var $dropdownMenu = $(this).next('.dropdown-menu');
            if ($dropdownMenu.is(':visible')) {
                $dropdownMenu.removeClass('animate__animated animate__slideInDown');
                $dropdownMenu.addClass('animate__animated animate__slideOutUp');
                setTimeout(() => {
                    $dropdownMenu.removeClass('animate__animated animate__slideOutUp');
                }, 300);
            } else {
                $dropdownMenu.addClass('animate__animated animate__slideInDown');
                setTimeout(() => {
                    $dropdownMenu.removeClass('animate__animated animate__slideInDown');
                }, 300);
            }
        });

        return {};
    });
});