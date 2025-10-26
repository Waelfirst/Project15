# -*- coding: utf-8 -*-

def migrate(cr, version):
    """Pre-migration script to ensure all fields exist in work_order_operation_line"""

    # Check if work_order_operation_line table exists
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'work_order_operation_line'
        );
    """)

    table_exists = cr.fetchone()[0]

    if table_exists:
        # List of all fields that should exist
        fields_to_add = [
            ('execution_line_id', 'INTEGER'),
            ('project_id', 'INTEGER'),
            ('product_id', 'INTEGER'),
            ('execution_id', 'INTEGER'),
            ('component_id', 'INTEGER'),
            ('production_id', 'INTEGER'),
            ('workorder_id', 'INTEGER'),
            ('operation_id', 'INTEGER'),
            ('workcenter_id', 'INTEGER'),
            ('name', 'VARCHAR'),
            ('sequence', 'INTEGER DEFAULT 10'),
            ('selected', 'BOOLEAN DEFAULT FALSE'),
            ('duration_expected', 'DOUBLE PRECISION DEFAULT 0'),
            ('duration_real', 'DOUBLE PRECISION DEFAULT 0'),
            ('actual_duration', 'DOUBLE PRECISION DEFAULT 0'),
            ('workers_assigned', 'INTEGER DEFAULT 0'),
            ('machines_assigned', 'INTEGER DEFAULT 0'),
            ('qty_production', 'DOUBLE PRECISION DEFAULT 0'),
            ('qty_produced', 'DOUBLE PRECISION DEFAULT 0'),
            ('date_start', 'TIMESTAMP'),
            ('date_finished', 'TIMESTAMP'),
            ('additional_code', 'TEXT'),
            ('specification_text', 'TEXT'),
            ('is_completed', 'BOOLEAN DEFAULT FALSE'),
            ('progress_percentage', 'DOUBLE PRECISION DEFAULT 0'),
            ('state', 'VARCHAR'),
        ]

        for field_name, field_type in fields_to_add:
            # Check if field exists
            cr.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='work_order_operation_line' 
                AND column_name=%s;
            """, (field_name,))

            if not cr.fetchone():
                print(f"Adding field: {field_name}")
                cr.execute(f"""
                    ALTER TABLE work_order_operation_line 
                    ADD COLUMN {field_name} {field_type};
                """)

        # Add indexes for better performance
        indexes = [
            'work_order_operation_line_execution_line_id_index',
            'work_order_operation_line_project_id_index',
            'work_order_operation_line_product_id_index',
            'work_order_operation_line_execution_id_index',
            'work_order_operation_line_production_id_index',
        ]

        for index_name in indexes:
            cr.execute(f"""
                CREATE INDEX IF NOT EXISTS {index_name} 
                ON work_order_operation_line({index_name.replace('work_order_operation_line_', '').replace('_index', '')});
            """)

        print("Pre-migration completed successfully")