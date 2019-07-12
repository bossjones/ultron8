# Example spreadsheet schema from stack overflow: [Table structure/schema for spreadsheet-like web app (ex: Google Docs)?](https://dba.stackexchange.com/questions/13047/table-structure-schema-for-spreadsheet-like-web-app-ex-google-docs)

```
Spreadsheet
    spreadsheet_id (unique key)
    name
    num_rows
    num_cols

column_types
    type_id (unique key)
    type_name

spreadsheet_rows
    spreadsheet_row_id (unique key)
    spreadsheet_id (refers to spreadsheet.spreadsheet_id)
    row_seq_num (for on-screen row-ordering)
    row_name

spreadsheet_cols
    spreadsheet_col_id (unique key)
    spreadsheet_id (refers to spreadsheet.spreadsheet_id)
    col_seq_num (for on-screen column-ordering)
    column_type_id (refers to column_types.type_id)
    column_name

spreadsheet_cells
    cell_id (unique key)
    spreadsheet_id (refers to spreadsheet.spreadsheet_id)
    row_id (refers to spreadsheet_rows.spreadsheet_row_id)
    col_id (refers to spreadsheet_cols.spreadsheet_col_id)
    cell_value (holds the actual value!)
```

# ultron8 schema
