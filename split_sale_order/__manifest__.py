{
    "name": "split_sale_order",
    "version": "15.0.1.0.0",
    "depends": ["sale_management"],
    "author": "Odoo Community Association (OCA),bizzappdev",
    "website": "https://www.bizzappdev.com",
    "category": "Sales/Sales",
    "summary": "Module to split sale orders based on criteria",
    "data": [
        "security/ir.model.access.csv",
        "wizard/sale_order_split_quotataion_view.xml",
        "views/sale_order.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
