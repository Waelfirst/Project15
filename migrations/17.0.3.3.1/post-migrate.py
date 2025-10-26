# -*- coding: utf-8 -*-

def migrate(cr, version):
    """Post-migration script to populate related fields"""

    # Update execution_id from execution_line_id
    cr.execute("""
        UPDATE work_order_operation_line wol
        SET execution_id = wel.execution_id
        FROM work_order_execution_line wel
        WHERE wol.execution_line_id = wel.id
        AND wol.execution_id IS NULL;
    """)

    # Update project_id from execution
    cr.execute("""
        UPDATE work_order_operation_line wol
        SET project_id = we.project_id
        FROM work_order_execution we
        WHERE wol.execution_id = we.id
        AND wol.project_id IS NULL;
    """)

    # Update product_id from execution
    cr.execute("""
        UPDATE work_order_operation_line wol
        SET product_id = we.product_id
        FROM work_order_execution we
        WHERE wol.execution_id = we.id
        AND wol.product_id IS NULL;
    """)

    # Update component_id from execution_line
    cr.execute("""
        UPDATE work_order_operation_line wol
        SET component_id = wel.component_id
        FROM work_order_execution_line wel
        WHERE wol.execution_line_id = wel.id
        AND wol.component_id IS NULL;
    """)

    # Update production_id from execution_line
    cr.execute("""
        UPDATE work_order_operation_line wol
        SET production_id = wel.production_id
        FROM work_order_execution_line wel
        WHERE wol.execution_line_id = wel.id
        AND wol.production_id IS NULL;
    """)