import json
import base64
from odoo import http
from odoo.http import request, Response


class ProductAPI(http.Controller):
    @http.route('/api/product/list', type='http', website=True, methods=['GET'], auth='public')
    def product_list(self):
        q = request.params.get('q')
        if q:
            products = request.env['product.template'].sudo().search([
                '|',
                ('default_code', 'ilike', '%' + q + '%'),
                ('name', 'ilike', '%' + q + '%')
            ])
        else:
            products = request.env['product.template'].sudo().search([])

        rows = []
        for p in products:
            image = None
            if p.image_1920:
                image = 'data:image/jpeg;base64,' + base64.b64decode(base64.b64encode(p.image_1920)).decode('utf-8')
            data = {
                'code': p.default_code,
                'name': p.name,
                'barcode': p.barcode,
                'sale_price': p.list_price,
                'cost_price': p.standard_price,
                'image': image
            }
            rows.append(data)
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/product/add', methods=['POST'], type='json', csrf=False, auth='public')
    def product_add(self, **kwargs):
        product = http.request.params
        request.env['product.template'].sudo().create({
            'name': product['name'],
            'list_price': product['sale_price'],
        })
        return json.dumps({'result': 'Success'})

    @http.route('/api/product/addform', methods=['POST'], type='http', csrf=False, auth='public')
    def product_add_form(self, **kwargs):
        request.env['product.template'].sudo().create({
            'name': kwargs.get('name'),
            'list_price': kwargs.get('sale_price'),
        })
        return json.dumps({'result': 'Success'})

    @http.route('/api/product/chart/bestseller', type='http', website=True, methods=['GET'], auth='public')
    def product_best_seller(self):
        query = """
            select 
                pc.name,
                sum(sl.product_uom_qty)
            from sale_order so left join sale_order_line sl on so.id=sl.order_id
                left join product_template pt on sl.product_id=pt.id
                left join product_category pc on pt.categ_id=pc.id
            where pc.name <> 'All'
            group by pc.name
        """
        request.cr.execute(query)
        results = request.cr.fetchall()
        return Response(json.dumps({'ok': True, 'rows': results}), content_type='application/json')
