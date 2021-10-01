#!/usr/bin/env python
# coding: utf-8

import csv


def menu() -> int:
    """ выводит меню и возвращает корректный выбор пользователя
    ecли выбор не корректен спрашивает вновь
    
    """
    print('1 Вывести в понятном виде иерархию команд, т.е. департамент и все команды, которые входят в него\n')
    print('2 Вывести сводный отчёт по департаментам: название, численность, "вилка" зарплат в виде мин – макс,\n',
          ' среднюю зарплату\n')
    print('3 Сохранить сводный отчёт из предыдущего пункта в виде csv-файла. При этом необязательно вызывать\n',
          ' сначала команду из п.2')
    print('4 завершить программу')
    print('выберите действие из списка выше:\n')

    while True:
        try:
            x = int(input())
            if (x>0 and x<5): 
                break
            else: 
                print('нет такого варианта\nвыберите действие из списка выше:\n')
        except ValueError:
            print('введите число!:\n')
    return x


def print_structure(path_name : str) :
    """
    открывает файл указанный в path_name и печатает список департаментов и их отделов,
    если не удалось печатает ошибку открытия файла
    
    """
    try:
        with open(path_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile,delimiter=';')
            departments = {}
            for row in reader:                
                departments[row['Департамент']] = departments.get( row['Департамент'], set([row['Отдел']]) )
                departments[row['Департамент']].add(row['Отдел'])
            for key,value in departments.items(): 
                print(key, ':', ', '.join(value)) 
                
    except FileNotFoundError:
        print(f'no file in directory:{path_name}')


def make_report(path_name : str) -> list :
    """
    открывает файл указанный в path_name и печатает в report.csv название, численность,
    "вилка" зарплат в виде мин – макс, среднюю зарплату
    
    если не удалось печатает ошибку открытия или создания файла
    
    """
    try:
        with open(path_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile,delimiter=';')
            departments = {}
            for row in reader:                
                departments[row['Департамент']] = departments.get( row['Департамент'], [0,int(row['Оклад']),0,0] )
                departments[row['Департамент']][0] += 1
                departments[row['Департамент']][1] = min(departments[row['Департамент']][1], int(row['Оклад']))
                departments[row['Департамент']][2] = max(departments[row['Департамент']][1], int(row['Оклад']))
                departments[row['Департамент']][3] += int(row['Оклад'])
        reports = []
        for key,value in departments.items():
            report = {}
            report['Департамент'] = key
            report['Численность'] = value[0]
            report['Mинимальная зп'] = value[1]
            report['Mаксимальная зп'] = value[2]
            report['Cредняя зп'] = int(value[3]/value[0])
            reports.append(report)
            
    except FileNotFoundError:
        print(f'no file in directory:{path_name}')    
    return reports
        
    
def print_report(path_name : str) -> None :
    reports = make_report(path_name)
    for report in reports:
        for key, value in report.items():
            print(f'{key}: {value}')
        print()
        
        
def save_report(path_name : str) -> None:    
    reports = make_report(path_name)
    with open('report.csv', 'w') as f:  
        w = csv.DictWriter(f, reports[0].keys())
        w.writeheader()
        for r in reports:
            w.writerow(r)
        print('report saved as "report.csv"')

        
def main():
    """основная ячейка """
    path_name = 'Corp_Summary.csv'

    while True:
        x = menu()
        options = {
            1: print_structure,
            2: print_report,
            3: save_report,
        }
        if x == 4: break
        elif x in options.keys():
            options[x](path_name)
        else: print('нет такого варианта\nвыберите действие из списка выше:\n')

