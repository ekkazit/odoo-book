from odoo import http
from odoo.http import request
from werkzeug import utils


class Customer(http.Controller):
    @http.route('/customer', auth='public', website=True)
    def index(self, **kw):
        customers = request.env['res.partner'].search([])
        return http.request.render('purchase_request.index', {
            'customers': customers,
        })

    @http.route('/customer/add', auth='public', methods=['POST'], csrf=False, website=True)
    def customer_add(self, **kw):
        http.request.env['res.partner'].sudo().create({
            'name': kw['txt_name'],
            'street': kw['txt_address'],
        })
        return utils.redirect('/customer')
