import time

import streamlit as st
import pandas as pd
import numpy as np
import random
import openpyxl
import sys
import sklearn 
import Orange
import pickle
import json

countHealthy = 0
countIll = 0

def getFeaturesFromModel(model):
    print('Получить список и очерёдность исков')
    listOfFeatures = []

    for ind, __ in enumerate(model.domain.attributes):
        listOfFeatures.append(model.domain.attributes[ind].name)
    return listOfFeatures

def getValuesForModel(model, dictOfVal):
    print ('Формирование значений признаков для конкретной модели')
    listOfFeatures = getFeaturesFromModel(model)
    dictOfValForModel = {}
    for colName in listOfFeatures:
        print(colName, end = '')
        if  colName in dictOfVal: 
            print(f' ...Найден, значение: {dictOfVal[colName]}')
            dictOfValForModel[colName] = dictOfVal[colName]
        else:
            raise Exception(f'Отсутствует необходимый x:{colName}')
    return dictOfValForModel

def isHealthy(x, threshold=0.5):
     global countHealthy, countIll
     if x < threshold:
          countHealthy += 1
          return "Здоров"
     else:
          countIll += 1
          return "Болен"

def isHealthyAvg(healthy, ill):
    if healthy == ill:
        return "Для уточнения диагноза требуется наблюдение в динамике"
    if healthy > ill:
        return "Здоров"
    else:
        return "Болен"

st.set_page_config(
  page_title="Диагностический калькулятор",
  page_icon="chart_with_upwards_trend",
  initial_sidebar_state="expanded"
)

st.header("Диагностический калькулятор для оценки стадии колоректального рака")
st.sidebar.header("Введите необходимые показатели")

#Создание вкладок боковой панели
tab1, tab2 = st.sidebar.tabs(["Ввод показателей", "Доп. настройки"])

#----------------------------------------------------------------------------------------------------------
modelFilePath = r"Контрольная VS КРР_любой=Логистическая регрессия(Orange3) 2023-05-03. vPub.pkcls"
print("Попытка загрузить файл по пути:", modelFilePath)
with open(modelFilePath, 'rb') as filestream:
    clf1 = pickle.load(filestream)
print("Файл успешно найден и загружен")

#----------------------------------------------------------------------------------------------------------
modelFilePath2 = r"Контрольная VS КРР_любой=Дерево5(Orange3) 2023-05-03. vPub.pkcls"
print("Попытка загрузить файл по пути:", modelFilePath2)
with open(modelFilePath2, 'rb') as filestream:
    clf2 = pickle.load(filestream)
print("Файл успешно найден и загружен")

#----------------------------------------------------------------------------------------------------------
modelFilePath3 = r"Контрольная VS КРР_любой=Лес(деревъев3, глубина3) (Orange3) 2023-05-03. vPub.pkcls"
print("Попытка загрузить файл по пути:", modelFilePath3)
with open(modelFilePath3, 'rb') as filestream:
    clf3 = pickle.load(filestream)
print("Файл успешно найден и загружен")

#----------------------------------------------------------------------------------------------------------
modelFilePath4 = r"КРР(1-2 стадии) VS КРР(3-4 стадии) =Лес(деревъев3, глубина3) (Orange3) 2023-06-03. vPub.pkcls"
print("Попытка загрузить файл по пути:", modelFilePath4)
with open(modelFilePath4, 'rb') as filestream:
    clf4 = pickle.load(filestream)
print("Файл успешно найден и загружен")

#----------------------------------------------------------------------------------------------------------
modelFilePath5 = r"КРР(1-2 стадии) VS КРР(3-4 стадии) =Логистическая регрессия(Orange3) 2023-06-02. vPub.pkcls"
print("Попытка загрузить файл по пути:", modelFilePath5)
with open(modelFilePath5, 'rb') as filestream:
    clf5 = pickle.load(filestream)
print("Файл успешно найден и загружен")


recallClf1 = 0.875
recallClf2 = 0.852
recallClf3 = 0.847

sidebar = st.sidebar
with sidebar:
    with tab1:
        is_age         = st.checkbox('список КРР возраст', value=True, key="age")
        age = st.number_input('список КРР возраст', disabled= not st.session_state.age)
        is_ast         = st.checkbox('БХ КРР АСТ', value=True, key="ast")
        ast = st.number_input('БХ КРР АСТ', disabled= not st.session_state.ast)
        is_acid        = st.checkbox('БХ КРР Мочевая кислота', value=True, key="acid")
        acid = st.number_input('БХ КРР Мочевая кислота', disabled= not st.session_state.acid)
        is_tryglycer   = st.checkbox('БХ КРР Триглицериды', value=True, key="tryglycer")
        tryglycer = st.number_input('БХ КРР Триглицериды', disabled= not st.session_state.tryglycer)
        is_urea        = st.checkbox('БХ КРР Мочевина', value=True, key="urea")
        urea = st.number_input('БХ КРР Мочевина', disabled= not st.session_state.urea)
        is_protein     = st.checkbox('БХ КРР Общий белок', value=True, key="protein")
        protein = st.number_input('БХ КРР Общий белок', disabled= not st.session_state.protein)
        is_glucose     = st.checkbox('БХ КРР Глюкоза крови', value=True, key="glucose")
        glucose = st.number_input('БХ КРР Глюкоза крови', disabled= not st.session_state.glucose)
        is_ggtp        = st.checkbox('БХ КРР ГГТП', value=True, key="ggtp")
        ggtp = st.number_input('БХ КРР ГГТП', disabled= not st.session_state.ggtp)
        is_erythrocyte = st.checkbox('ОАК КРР Количество эритроцитов', value=True, key="erythrocyte")
        erythrocyte = st.number_input('ОАК КРР Количество эритроцитов', disabled= not st.session_state.erythrocyte)
        is_hemoglobin  = st.checkbox('ОАК КРР Гемоглобин', value=True, key="hemoglobin")
        hemoglobin = st.number_input('ОАК КРР Гемоглобин', disabled= not st.session_state.hemoglobin)
        is_hemotocrit  = st.checkbox('ОАК КРР Гематокрит', value=True, key="hemotocrit")
        hemotocrit = st.number_input('ОАК КРР Гематокрит', disabled= not st.session_state.hemotocrit)
        is_leukocytes  = st.checkbox('ОАК КРР Количество лейкоцитов', value=True, key="leukocytes")
        leukocytes = st.number_input('ОАК КРР Количество лейкоцитов', disabled= not st.session_state.leukocytes)
        is_platelets   = st.checkbox('ОАК КРР Тромбоциты', value=True, key="platelets")
        platelets = st.number_input('ОАК КРР Тромбоциты', disabled= not st.session_state.platelets)
        is_alt = st.checkbox('БХ КРР АЛТ', value=True, key="alt")
        alt = st.number_input('БХ КРР АЛТ', disabled= not st.session_state.alt)
        is_omega3 = st.checkbox('ЛП КРР e омега-3', value=True, key="omega3")
        omega3 = st.number_input('ЛП КРР e омега-3', disabled= not st.session_state.omega3)
        is_c16 = st.checkbox('ЛП КРР s 9,12-C16:2', value=True, key="c16")
        c16 = st.number_input('ЛП КРР s 9,12-C16:2', disabled= not st.session_state.c16)
        is_c18 = st.checkbox('ЛП КРР s c-C18:1', value=True, key="c18")
        c18 = st.number_input('ЛП КРР s c-C18:1', disabled= not st.session_state.c18)
        is_c20 = st.checkbox('ЛП КРР s 5,8,11,14-C20:4', value=True, key="c20")
        c20 = st.number_input('ЛП КРР s 5,8,11,14-C20:4', disabled= not st.session_state.c20)
        is_c22 = st.checkbox('ЛП КРР s 7,10,13,16-C22:4', value=True, key="c22")
        c22 = st.number_input('ЛП КРР s 7,10,13,16-C22:4', disabled= not st.session_state.c22)
        is_mono = st.checkbox('ЛП КРР s мононенасыщ', value=True, key="mono")
        mono = st.number_input('ЛП КРР s мононенасыщ', disabled= not st.session_state.mono)
        is_poli = st.checkbox('ЛП КРР s полиненасыщ', value=True, key="poli")
        poli = st.number_input('ЛП КРР s полиненасыщ', disabled= not st.session_state.poli)
        is_spherocytes = st.checkbox('ВУХ КРР Доля сфероцитов', value=True, key="spherocytes")
        spherocytes = st.number_input('ВУХ КРР Доля сфероцитов', disabled= not st.session_state.spherocytes)
        is_deformcells = st.checkbox('ВУХ КРР Доля деформир.клеток', value=True, key="deformcells")
        deformcells = st.number_input('ВУХ КРР Доля деформир.клеток', disabled= not st.session_state.deformcells)
        is_deformamplitude = st.checkbox('ВУХ КРР Амплитуда деформации на 1МГц', value=True, key="deformamplitude")
        deformamplitude = st.number_input('ВУХ КРР Амплитуда деформации на 1МГц', disabled= not st.session_state.deformamplitude)
        is_deformdegree = st.checkbox('ВУХ КРР Степень деформации на 0,5МГц в %', value=True, key="deformdegree")
        deformdegree = st.number_input('ВУХ КРР Степень деформации на 0,5МГц в %', disabled= not st.session_state.deformdegree)
        is_stiffness = st.checkbox('ВУХ КРР Обобщенная жесткость', value=True, key="stiffness")
        stiffness = st.number_input('ВУХ КРР Обобщенная жесткость', disabled= not st.session_state.stiffness)
        is_viscocity = st.checkbox('ВУХ КРР Обобщенная вязкость', value=True, key="viscocity")
        viscocity = st.number_input('ВУХ КРР Обобщенная вязкость', disabled= not st.session_state.viscocity)
        is_membranecapacity = st.checkbox('ВУХ КРР Емкость мембран', value=True, key="membranecapacity")
        membranecapacity = st.number_input('ВУХ КРР Емкость мембран', disabled= not st.session_state.membranecapacity)
        is_omega63 = st.checkbox('ЛП КРР e омега-6|омега-3', value=True, key="omega63")
        omega63 = st.number_input('ЛП КРР e омега-6|омега-3', disabled= not st.session_state.omega63)
        is_serumiron = st.checkbox('БХ КРР Железо сыворотки', value=True, key="serumiron")
        serumiron = st.number_input('БХ КРР Железо сыворотки', disabled= not st.session_state.serumiron)

    with tab2:
        thresholdlr = st.slider('Пороговое значение для модели Лог. регр', value=0.5, min_value=0.0, max_value=1.0)
        thresholdtree = st.slider('Пороговое значение для модели Дерево', value=0.5, min_value=0.0, max_value=1.0)
        thresholdforest = st.slider('Пороговое значение для модели Лес', value=0.5, min_value=0.0, max_value=1.0)

dictOfVal = {
    'список КРР возраст':age,
    'БХ КРР АСТ':ast,
    'БХ КРР Мочевая кислота':acid,
    'БХ КРР Триглицериды':tryglycer,
    'БХ КРР Мочевина':urea,
    'БХ КРР Общий белок':protein,
    'БХ КРР Глюкоза крови': glucose,
    'БХ КРР ГГТП':ggtp,
    'ОАК КРР Количество эритроцитов':erythrocyte,
    'ОАК КРР Гемоглобин':hemoglobin,
    'ОАК КРР Гематокрит': hemotocrit,
    'ОАК КРР Количество лейкоцитов':leukocytes,
    'ОАК КРР Тромбоциты':platelets,
    'БХ КРР АЛТ':alt,
    'БХ КРР Железо сыворотки':serumiron,
    'ВУХ КРР Амплитуда деформации на 1МГц':deformamplitude,
    'ВУХ КРР Доля деформир.клеток': deformcells,
    'ВУХ КРР Доля сфероцитов':spherocytes,
    'ВУХ КРР Емкость мембран':membranecapacity,
    'ВУХ КРР Обобщенная вязкость':viscocity,
    'ВУХ КРР Обобщенная жесткость':stiffness,
    'ВУХ КРР Степень деформации на 0,5МГц в %':deformdegree,
    'ЛП КРР e омега-3':omega3,
    'ЛП КРР s 5,8,11,14-C20:4':c20,
    'ЛП КРР s 7,10,13,16-C22:4':c22,
    'ЛП КРР s 9,12-C16:2':c16,
    'ЛП КРР s мононенасыщ':mono,
    'ЛП КРР e омега-6|омега-3':omega63,
    'ЛП КРР s полиненасыщ':poli,
    'ЛП КРР s c-C18:1':c18,
}

tab1_main, tab2_main = st.tabs(["Скрининг диагностики", "Оценка стадии рака"])
state = st.session_state

dictxformodel1 = getValuesForModel(clf1, dictOfVal)
dictxformodel2 = getValuesForModel(clf2, dictOfVal)
dictxformodel3 = getValuesForModel(clf3, dictOfVal)

dictxformodel4 = getValuesForModel(clf4, dictOfVal)
dictxformodel5 = getValuesForModel(clf5, dictOfVal)

df_model1 = pd.DataFrame.from_dict(dictxformodel1,orient='index').T
df_model2 = pd.DataFrame.from_dict(dictxformodel2,orient='index').T
df_model3 = pd.DataFrame.from_dict(dictxformodel3,orient='index').T

df_model4 = pd.DataFrame.from_dict(dictxformodel4,orient='index').T
df_model5 = pd.DataFrame.from_dict(dictxformodel5,orient='index').T

isUseLogReg = is_age and is_acid and is_tryglycer and is_protein and is_hemoglobin and is_leukocytes and is_platelets
isUseTree = is_age and is_tryglycer and is_ggtp and is_erythrocyte and is_hemoglobin
isUseForest = is_age and is_ast and is_tryglycer and is_urea and is_glucose and is_ggtp and is_hemoglobin and is_hemotocrit

isUseLogRegStage = alt and ggtp and serumiron and tryglycer and spherocytes and membranecapacity and deformdegree and omega63 and hemoglobin and leukocytes and platelets
isUseForestStage = alt and deformamplitude and deformcells and spherocytes and membranecapacity and viscocity and stiffness and deformdegree and omega3 and c20 and c22 and c16 and mono and poli and c18

targetClassesName = clf1.domain.class_var.values

with tab1_main:
        st.header("Скрининг диагностики")
        st.subheader("Результаты работы моделей")
        if st.button('Рассчитать', key=1):
            if(isUseLogReg):
                y1 = clf1.predict_proba(df_model1.values)
                st.write(f' {"Лог. регрессия":>20}: ' + f'{y1[0][0]:.1%}' + ' -> Вывод: ' + isHealthy(y1[0][0], thresholdlr))
            else:
                st.write(f' {"Лог. регрессия":>20}: Недостаточно данных')
            if(isUseTree):
                y2 = clf2.predict_proba(df_model2.values)
                st.write(f' {"Дерево":>20}: ' + f'{y2[0][0]:.1%}' + ' -> Вывод: ' + isHealthy(y2[0][0], thresholdtree))
            else:
                st.write(f' {"Дерево":>20}: Недостаточно данных')
            if(isUseForest):
                 y3 = clf3.predict_proba(df_model3.values)
                 st.write(f' {"Лес":>20}: ' + f'{y3[0][0]:.1%}' + ' -> Вывод: ' + isHealthy(y3[0][0], thresholdforest))
            else:
                st.write(f' {"Лес":>20}: Недостаточно данных')
            if(isUseLogReg and isUseTree and isUseForest):
                avg = (y1[0][0]*recallClf1 + y2[0][0]*recallClf2 + y3[0][0]*recallClf3)/(recallClf1 + recallClf2 + recallClf3)
                st.write('Общая оценка: ' + f'{avg:.1%}' + ' -> Вывод: ' + isHealthyAvg(countHealthy, countIll))
            else:
                if(isUseLogReg and isUseTree):
                    avg = (y1[0][0]*recallClf1 + y2[0][0]*recallClf2)/(recallClf1 + recallClf2)
                    st.write('Общая оценка: ' + f'{avg:.1%}' + ' -> Вывод: ' + isHealthyAvg(countHealthy, countIll))
                if(isUseLogReg and isUseForest):
                    avg = (y1[0][0]*recallClf1 + y3[0][0]*recallClf3)/(recallClf1 + recallClf3)
                    st.write('Общая оценка: ' + f'{avg:.1%}' + ' -> Вывод: ' + isHealthyAvg(countHealthy, countIll))
                if(isUseTree and isUseForest):
                    avg = (y2[0][0]*recallClf2 + y3[0][0]*recallClf3)/(recallClf2 + recallClf3)
                    st.write('Общая оценка: ' + f'{avg:.1%}' + ' -> Вывод: ' + isHealthyAvg(countHealthy, countIll))
        st.subheader("Введенные показатели")
        st.write("Модель Логистическая регрессия")
        df_model1
        st.write("Модель Дерево")
        df_model2
        st.write("Модель Случайный лес")
        df_model3

with tab2_main:
        st.header("Оценка стадии колоректального рака")
        st.subheader("Результаты работы моделей")
        if st.button('Рассчитать', key=2):
            st.subheader('Модель лес:')
            if(isUseForestStage):
                y4 = clf4.predict_proba(df_model4.values)
                st.write(f' {"Ранняя стадия":>20}: ' + f'{y4[0][0]:.1%}')
                st.write(f' {"Поздняя стадия":>20}: ' + f'{y4[0][1]:.1%}')
            else:
                st.write('Недостаточно данных')
            
            st.subheader('Модель логистичской регрессии:')
            if(isUseLogRegStage):
                y5 = clf5.predict_proba(df_model5.values)
                st.write(f' {"Ранняя стадия":>20}: ' + f'{y5[0][0]:.1%}')
                st.write(f' {"Поздняя стадия":>20}: ' + f'{y5[0][1]:.1%}')
            else:
                st.write('Недостаточно данных')

        st.subheader("Введенные показатели")
        st.write("Модель Случайный лес")
        df_model4
        st.write("Модель Логистическая регрессия")
        df_model5
