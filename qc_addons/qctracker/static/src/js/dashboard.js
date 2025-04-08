odoo.define('qctracker.dashboard', function (require) {
    "use strict";
    
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    
    var QCTrackerDashboard = AbstractAction.extend({
        // Ne pas spécifier de template
        
        /**
         * @override
         */
        start: function () {
            var self = this;
            
            // Créer l'iframe directement
            this.$el.empty().addClass('qctracker_dashboard_container').css({
                'width': '100%',
                'height': '100%',
                'padding': '0',
                'margin': '0',
                'overflow': 'hidden'
            });
            
            var iframe = $('<iframe>', {
                id: 'dashboard_iframe',
                src: 'http://127.0.0.1:8050/dash/',
                frameborder: '0',
                css: {
                    'width': '100%',
                    'height': '100%',
                    'border': 'none',
                    'display': 'block',
                    'margin': '0',
                    'padding': '0'
                }
            });
            
            this.$el.append(iframe);
            
            // Ajout du CSS global pour corriger les problèmes de layout
            $('<style>')
                .text(`
                    .o_action_manager {
                        margin: 0 !important;
                        padding: 0 !important;
                        overflow: hidden !important;
                    }
                    
                    .o_control_panel, .o_cp_buttons, .o_cp_left, .o_cp_right,
                    .o_form_buttons_view, .o_form_buttons_edit, .breadcrumb {
                        display: none !important;
                    }
                    
                    .o_content {
                        padding: 0 !important;
                        margin: 0 !important;
                        height: calc(100vh - 46px) !important;
                        width: 100% !important;
                        position: absolute !important;
                        top: 46px !important;
                        left: 0 !important;
                        right: 0 !important;
                        overflow: hidden !important;
                    }
                `)
                .appendTo('head');
            
            // Fonction d'ajustement
            function adjustDimensions() {
                var headerHeight = $('.o_main_navbar').outerHeight() || 46;
                
                self.$el.parents('.o_content').css({
                    'height': 'calc(100vh - ' + headerHeight + 'px)',
                    'top': headerHeight + 'px'
                });
            }
            
            // Appliquer les ajustements
            setTimeout(adjustDimensions, 100);
            setTimeout(adjustDimensions, 500);
            
            // Réajuster lors du redimensionnement
            $(window).on('resize', adjustDimensions);
            
            return this._super.apply(this, arguments);
        },
        
        /**
         * @override
         */
        destroy: function () {
            $(window).off('resize');
            this._super.apply(this, arguments);
        },
    });
    
    core.action_registry.add('qctracker.dashboard', QCTrackerDashboard);
    
    return QCTrackerDashboard;
});