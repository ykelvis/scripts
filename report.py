#-*- coding: utf-8 -*-
#!/usr/bin/python
import sys;
import xlrd;
import xlsxwriter;

def all_data_to_array(arg):
    to_write = [];
    for i in range(1,arg.nrows):
        if arg.row(i)[0].value != arg.row(i-1)[0].value:
            to_write.append(arg.row(i));
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
                new_worksheet.write(i,j,array[i][j].value,date_format);
            else:
                if type(array[i][j]) == str:
                    new_worksheet.write(i,j,array[i][j]);
                else:
                    new_worksheet.write(i,j,array[i][j].value);

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
    a.append(array[0]); #get index line
    for i in range(len(array)):
        if ("Production" in str(array[i][area])) and (int(array[i][grade].value) <= 5):
            a.append(array[i])
    return a;

def get_idl(array,area,grade):
    a = [];
    a.append(array[0]); #get index line
    for i in range(len(array)):
        if not ("Production" in str(array[i][area]) and int(array[i][grade].value) <= 5):
            a.append(array[i]);
    return a;

def production_list(array,a,b,c):
    for i in range(len(array)):
        if ("Fixed Term" in str(array[i][a])) or ("Regular" in str(array[i][a])):
            array[i].append("zhengshigong");
        elif ("X001" in str(array[i][b])) or ("x001" in str(array[i][b])) and (array[i][-1] != "zhengshigong"):
            array[i].append("Intern");
        elif ("\u5916\u5305" in str(array[i][c])):
            array[i].append("Agency Worker");
        else:
            array[i].append("Normal Dispatch");
    return array;

def get_useful_col(array,start_row,col):
    a = [];
    for i in range(start_row,len(array)):
        a.append([]);
        for j in col:
            a[-1].append(array[i][j]); #array is not origin,so index not working.
    return a;
def get_headcount(array):
    for i in range(len(array)):
        if ("zhengshigong" in str(array[i][9])) and ((array[i][6] == "") or ("\u5185\u63a8" in array[i][6])):
            array[i].append("1");
        elif ("zhengshigong" in str(array[i][9])) and (array[i][-1] != "1"):
            array[i].append("2");
    return array;

origin = sys.argv[1]
wbook = xlrd.open_workbook(origin,on_demand=True);
table = wbook.sheets()[0];

to_write = all_data_to_array(table);
to_write = to_write[5:];
_rows = len(to_write);
col_index = get_cell_index(["text:u'Employee_ID'","text:u'Chinese_Name'","text:u'Gender'","text:u'Hire_Date'","text:u'Employee_Type'","text:u'China_Badge_Number'","text:u'Agency'","text:u'Work_Area'","text:u'Compensation_Grade'"],to_write,0)
print col_index
print to_write[0]
to_write = get_dl(to_write,col_index[-2],col_index[-1])
info = get_useful_col(to_write,0,col_index)
prolist = production_list(info,4,5,6)
prolist = get_headcount(prolist)
#print prolist
#print type(prolist[0][3])
write_to_local_xlsx("idl.xlsx",prolist,1)
