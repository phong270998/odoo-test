# Copyright © 2025 Namtech
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    percent = fields.Float('Percent', default=0.0)
    @api.onchange('percent')
    def _onchange_percent(self):
        for r in self:
            if len(r.product_tmpl_id.seller_ids) == 1:
                r.percent = 100.0 

    @api.onchange('product_tmpl_id')
    def _onchange_product_default_percent(self):
        for r in self:
            s = r.product_tmpl_id.seller_ids
            if not s:
                continue
            if len(s) == 1:
                s.percent = 100.0
            elif all((x.percent or 0.0) == 0.0 for x in s):
                s[0].percent = 100.0
                for x in s[1:]:
                    x.percent = 0.0

    @api.constrains('percent', 'product_tmpl_id')
    def _check_total(self):
        for r in self:
            pt = r.product_tmpl_id
            if not pt:
                continue
            total = sum((x.percent or 0.0) for x in pt.seller_ids.exists())
            if total > 100.0:
                raise ValidationError(
                    f"Total percentage of vendors cannot exceed 100% (present: {total:.2f}%)."
                )