odoo.define('backend_debranding.dialog', function(require) {
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;
    var rpc = require('web.rpc');
//    var Model = require('web.DataModel')
//    var debranding_new_name = 'Ctotal';
    var debranding_new_name = 'BriQ';
//            var model = new Model("ir.config_parameter");
            var r = rpc.query({
                    model: 'ir.config_parameter',
                    method: 'search_read',
                    args: [[['key', '=', 'backend_debranding.new_name']],['value']],
                    limit: 1,
                }).then(function (data) {
                    if (!data.length)
                        return;
                    debranding_new_name = data[0].value;
                });

    var CrashManager = require('web.CrashManager')
    CrashManager.include({
        init: function () {
            this._super();
            var self = this;
//            var model = new Model("ir.config_parameter");
            self.debranding_new_name = _t('Software');
            if (!openerp.session.db)
                return;
//            var r = model.query(['value'])
//                .filter([['key', '=', 'backend_debranding.new_name']])
//                .limit(1)
//                .all().then(function (data) {
//                    if (!data.length)
//                        return;
//                    self.debranding_new_name = data[0].value;
//                });
            var r = rpc.query({
                    model: 'ir.config_parameter',
                    method: 'search_read',
                    args: [[['key', '=', 'backend_debranding.new_name']],['value']],
                    limit: 1,
                }).then(function (data) {
                    if (!data.length)
                        return;
                    self.debranding_new_name = data[0].value;
                });
        },
    });

    var Dialog = require('web.Dialog')
    Dialog.include({
        init: function (parent, options) {

            // TODO find another way to get debranding_new_name
            if (parent && parent.debranding_new_name){
                debranding_new_name = parent.debranding_new_name;
            }
            options = options || {};
            if (options['title']){
                var title = options['title'].replace(/Odoo/ig, debranding_new_name);
                options['title'] = title;
            } else {
                options['title'] = debranding_new_name;
            }
            if (options.$content){
                if (!(options.$content instanceof $)){
                    options.$content = $(options.$content)
                }
                var content_html = options.$content.html().replace(/Odoo/ig, debranding_new_name);
                options.$content.html(content_html);
            }
            this._super(parent, options);
        },
    });
});
