# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([
        ('new','New'), ('received','Offer Received'),
        ('accepted','Offer Accepted'), ('sold','Sold'), ('cancel','Cancelled')
        ], default='new', string ='Status')
    type_id = fields.Many2one('estate.property.type', string='Property Type')
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tag')
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From')
    expected_price = fields.Float('Expected Price')

    
    best_offer = fields.Float('Best Offer', compute='_compute_best_offer')
    selling_price = fields.Float('Selling Price', readonly=True)
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')
    ], string='Garden Orientation')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    sales_id = fields.Many2one('res.users', string='Salesman')
    buyer_id = fields.Many2one('res.partner', string='Buyer', domain=[('is_company', '=', True)])
    phone = fields.Char('Phone', related='buyer_id.phone')

    total_area = fields.Integer('Total Area', compute='_compute_total_area')

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer = 0

    # @api.depends('garden_area','living_area')
    # def _compute_total_area(self):
    #     for rec in self:
    #         rec.total_area = rec.garden_area + rec.living_area

    #bisa juga pake onchange tapi mending depends, karna onchange hanya berlaku untuk form view yg dimaksud aja
    @api.onchange('garden_area','living_area')
    def _compute_total_area(self):
         self.total_area = self.garden_area + self.living_area

    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'cancel'
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    offer_count = fields.Integer(string="Offer Counts", compute=_compute_offer_count)




class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    name = fields.Char('Name', required=True)


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'

    name = fields.Char('Name', required=True)
    color = fields.Integer(string='Color')