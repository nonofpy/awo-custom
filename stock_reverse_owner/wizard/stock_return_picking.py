# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

class stock_return_picking(models.TransientModel):
    _inherit = 'stock.return.picking'
    
    return_category = fields.Selection(
        [('repair', 'Repair'),
        ('return_company', 'Return ­Company'),
        ('return_vci', 'Return ­VCI'),
        ('return_no_ownership_change', 'Return no Ownership Change')],
        string='Return Category',
        required=True,
    )
    supplier_id = fields.Many2one(
        'res.partner',
        string='Supplier',
        domain="[('supplier', '=', 1)]",
    )

    @api.one
    @api.onchange('return_category')
    def onchange_return_category(self):
        if self.return_category == 'return_vci':
            active_ids =  self.env.context.get('active_ids', [])
            picking_ids = self.env['stock.picking'].browse(active_ids)
            for picking in picking_ids:
                for move in picking.move_lines:
                    if move.reserved_quant_ids:
                        for quant in move.reserved_quant_ids:
                            if quant.owner_id:
                                self.supplier_id = quant.owner_id

    @api.multi
    def _create_returns(self):
        for data in self:
            for move in data.product_return_moves:
                if not move.lot_id and data.return_category == 'return_vci':
                    raise Warning (_('You can not return picking with return category option Return VCI in case serial number on return lines are empty. Please select serial number and then try to process.'))
        new_picking, picking_type_id = super(stock_return_picking, self)._create_returns()
        picking = self.env['stock.picking'].browse(new_picking)
        for rec in self:
            picking.return_category = rec.return_category
            if rec.return_category == 'repair':
                picking.owner_id = picking.partner_id.id
            #    repair_loc_id = self.env['stock.location'].search([('is_repaired_location', '=', True)])#Fixed using hook
            #    if repair_loc_id:
            #        for move in picking.move_lines:
            #            move.location_dest_id = repair_loc_id.id
            elif rec.return_category == 'return_company':
                picking.owner_id = picking.company_id.partner_id.id
            elif rec.return_category == 'return_vci':
                picking.owner_id = rec.supplier_id.id
            else:
                pass # odoo standard case
        return new_picking, picking_type_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
