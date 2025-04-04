# -*- coding: utf-8 -*-
################################################################################
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 202-TODAY Cybrosys Technologies (<https://www.cybrosys.com>)
#    Author: Hajaj Roshan (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
################################################################################

{
    'name': 'Open HRMS Branch Transfer',
    'version': '15.0.1.1.1',
    'summary': 'Employee transfer between branches',
    'live_test_url': 'https://youtu.be/Qva8kW6xn4c',
    'category': 'Generic Modules/Human Resources',
    'author': 'Cybrosys Techno solutions,Open HRMS',
    'maintainer': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.openhrms.com',
    'depends': ['base',
                'hr',
                'hr_employee_transfer'
                ],
    'data': [
        'views/employee_transfer.xml',
        'security/ir.model.access.csv',
        'security/branch_security.xml',
    ],
    #'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
