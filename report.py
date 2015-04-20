#-*- coding: utf-8 -*-
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
                if type(array[i][j]) == str:
                    new_worksheet.write(i+1,j,array[i][j]);
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

def get_cell_index(cell,array,index_row):
    a = [];
    for i in cell:
        for j in range(len(array[index_row])):
            if str(array[index_row][j]) == i:
                a.append(j);
            else:
                continue;
    return a;

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

def production_list(array,col_index):
    for i in range(len(array)):
        if "Fixed Term" or "Regular" in str(array[i][2]) == True:
            print str(array[i][2])
            array[i].append("zhengshigong");
        elif "X001" or "x001" in str(array[i][col_index[0]]):
            array[i].append("intern");
    return array;

def get_useful_col(array,start_row,col):
    a = [];
    for i in range(start_row,len(array)):
        a.append([]);
        for j in col:
            a[-1].append(array[i][j]); #array is not origin,so index not working.
    return a;

origin = sys.argv[1]
wbook = xlrd.open_workbook(origin,on_demand=True);
table = wbook.sheets()[0];

rows = table.nrows;
to_write = all_data_to_array(origin);
_rows = len(to_write);
col_index = get_cell_index(["text:u'China_Badge_Number'","text:u'Work'","text:u'Employee_ID","text:u'Compensation_Grade'","text:u'Gender'","text:u'Hire_Date'","text:u'Employee_Type'"],to_write,5)

info = get_useful_col(to_write,0,col_index)
prolist = production_list(info,col_index)
#print prolist
#print type(prolist[0][3])
write_to_local_xlsx("idl.xlsx",prolist,1)
