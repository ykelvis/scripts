#!/usr/bin/python
import sys;
import xlrd;
import xlsxwriter;

def all_data_to_array(arg):
    to_write = [];
    for i in range(1,rows):
        if table.row(i)[0].value != table.row(i-1)[0].value:
            to_write.append(table.row(i));
        else:
            continue;
    return to_write;

def write_to_local_xlsx(file_name,array,mode):
    new_workbook = xlsxwriter.Workbook(file_name);
    new_worksheet = new_workbook.add_worksheet();
    date_format = new_workbook.add_format({'num_format': 'yyyy-mm-dd'});
    for i in range(len(array)):
        for j in range(len(array[i])):
            if table.cell(i,j).ctype == 3:
                new_worksheet.write(i+1,j,array[i][j].value,date_format);
            else:
                new_worksheet.write(i+1,j,array[i][j].value);
    #dont forget first line
    if mode == 1:
        length_first_line = len(table.row(0));
        for i in range(0,length_first_line):
            new_worksheet.write(0,i,table.row(0)[i].value);
    else:
        pass;
    new_workbook.close();

def get_cell_index(cell,array,row):
    for i in range(len(array[row])):
        if str(array[row][i]) == cell:
            return i;
        else:
            continue;

def get_dl(array,area,grade):
    a = [];
    for i in range(len(array)):
        if "Production" in str(array[i][area]) and int(array[i][grade].value) <= 5:
            a.append(array[i])
    return a;

def get_idl(array,area,grade):
    a = [];
    for i in range(len(array)):
        if not ("Production" in str(array[i][area]) and int(array[i][grade].value) <= 5):
            a.append(array[i]);
    return a;

def production_list(array,e_type):
    for i in range(len(array)):
        if "Fix Term" or "Regular" in str(array[i][e_type]):
            array[i].append("zhengshi");
    return array;

def get_useful_col(array,start_row,rows,col):
    a = [];
    for i in range(start_row,rows):
        a.append([]);
        for j in col:
            a[-1].append(array[i][j]); #array is not origin,so index not working.
    return a;

'''
if __name__ == '__main__':
    origin = sys.argv[1]
    to_file = "modified-" + origin;
    wbook = xlrd.open_workbook(origin,on_demand=True);
    table = wbook.sheets()[0];
    rows = table.nrows;
    to_write = all_data_to_array(origin);
    write_to_local_xlsx(to_file);
    '''
origin = sys.argv[1]
wbook = xlrd.open_workbook(origin,on_demand=True);
table = wbook.sheets()[0];
rows = table.nrows;
to_write = all_data_to_array(origin);
col_workarea = get_cell_index("text:u'Work_Area'",to_write,5);
col_employee_id = get_cell_index("text:u'Employee_ID'",to_write,5);
col_compensation_grade = get_cell_index("text:u'Compensation_Grade'",to_write,5)
col_gender = get_cell_index("text:u'Gender'",to_write,5);
col_hire_date = get_cell_index("text:u'Hire_Date'",to_write,5);
col_employee_type = get_cell_index("text:u'Employee_Type'",to_write,5)

print col_employee_id,col_gender,col_hire_date,col_workarea,col_compensation_grade,col_employee_type;
col = [col_employee_id,col_gender,col_hire_date,col_workarea,col_compensation_grade,col_employee_type];

length = len(to_write);

info = get_dl(to_write,col_workarea,col_compensation_grade);
info = get_useful_col(info,5,rows,col)
write_to_local_xlsx("idl.xlsx",info,1)
