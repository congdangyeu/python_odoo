from odoo import fields, api, models, _
import datetime
class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread"]
    _description = "Hospital Appointment"

    name = fields.Char(string="Name", required=True, track_visibility='always')
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    age = fields.Integer(string="Age", related='patient_id.age', track_visibility='always')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancel')], string='State', default="draft",
                             track_visibility='always')
    # responsible_id = fields.Many2one('res.partner', string="Responsible", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, string='Gender', track_visibility='always')
    note = fields.Text(string="Description")
    date_appointment = fields.Date(string='Date')
    date_checkup = fields.Datetime(string='Check Up Time')


    def action_confirm(self):
        self.state = 'confirm'
        print('Test GIT111!!!')

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New patient'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(HospitalAppointment, self).create(vals)

    @api.onchange('patient_id')
    def onchange_patient(self):
        if self.patient_id and self.patient_id.gender:
            self.gender = self.patient_id.gender
        else:
            self.gender = ''
