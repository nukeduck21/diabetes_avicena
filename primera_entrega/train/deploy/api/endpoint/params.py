proyecto = 'co-keralty-costomedico'
dataset = 'Diabetes_avicena'

# examenes

fecha_para_tomar_examenes = '2019-10-31'

examenes_glicemia = ['Glicemia Basal (mg/dl)','Glicemia (mg/dl)','Glucosa']
examenes_glucosa = ['Glicemia 2 horas Postprandial (mg/dl)','Glicemia Pos(mg/dl)']
examenes_hba1c = ['Hemoglobina Glicosilada (%)','Hemoglobina Glicosilada (HbA1c) (%)','Prueba rápida hemoglobina glicosilada']
examenes_hdl = ['Colesterol HDL','Colesterol HDL (mg/dl)','HDL (mg/dl)']
examenes_ldl = ['Colesterol LDL','Colesterol LDL (mg/dl)','LDL (mg/dl)']
examenes_trigliceridos = ['Triglicéridos','Triglicéridos (mg/dl)']
examenes_albuminuria = ['Microalbuminuria (mg/l)','Relaciones albumina/creatinina (RAC)','Relación Albuminuria/creatinuria (RAC)']

# Antecedentes

codigos_medicamentos_hipertension = ['C02AB0113C01','C02AB0113C02','C02AC0113C01','C02CA0113C01','C03EA0113C02',
                                     'C03EA0113C03','C07AA0513C01','C07AA0513C02','C07AB0213C02','C07AB0213C03',
                                     'C07AB0214C01','C07AB0214C02','C07AB0214C03','C07AB0214C04','C07AB0231C01',
                                     'C07AB0313C01','C07AB0313C02','C07AB0713C01','C07AB0713C07','C07CB0313C01',
                                     'C08CA0101C01','C08CA0101C02','C08CA0101C08','C08CA0113C01','C08CA0113C02',
                                     'C08CA0113C03','C08CA0113C04','C08CA0113C05','C08CA0113C07','C08CA0113C08',
                                     'C08CA0113C10','C08CA0501C01','C08CA0503C01','C08CA0514C02','C08DA0103C02',
                                     'C08DA0113C01','C08DA0113C03','C08DA0114C02','C08DA0131C01','C08GA0213C01',
                                     'C09AA0113C01','C09AA0113C02','C09AA0213C02','C09AA0213C03','C09BB0413C01',
                                     'C09BB0413C02','C09BB0413C03','C09BB0413C04','C09BB1003C01','C09BB1013C01',
                                     'C09BX0113C02','C09BX0113C03','C09CA0113C02','C09CA0113C03','C09CA0301C14',
                                     'C09CA0813C01','C09CA0813C02','C09CA0813C03','C09DA0113C02','C09DA0113C03',
                                     'C09DA0113C04','C09DA0613C01','C09DB0101C04','C09DB0113C01','C09DB0113C02',
                                     'C09DB0113C05','C09DB0413C02','C09DB0413C03','C09DB0413C05','C09DB0513C01',
                                     'C09DB0513C02','C09DB0513C03','C09DB0513C04','C09DB0601C01','C09DX0113C02',
                                     'C09DX0113C04','C09DX0113C05','MAGISTR6018']

codigos_cardiovascular = ['I630','I631','I632','I633','I634','I635','I638','I639','I653','I658','I659','I660','I661','I662','I664','I668',
                          'I669','I672','I693','I698','I500','I509','I518','Y840','I210','I211','I212','I213','I214','I219','I220','I221',
                          'I228','I229','I230','I231','I232','I233','I234','I235','I238','I240','I250','I251','I252','I702','I708','I709',
                          'I739','I236','I240','I513','I81X','J960','J961','J969','P285','E271','E273','E274','E283','E310','E894','I051',
                          'I052','I061','I062','I071','I110','I119','I120','I129','I130','I131','I132','I340','I351','I361','I371','I500',
                          'I501','I509','I872','J951','J952','J953','J960','J961','J969','K704','K720','K721','K729','N170','N171','N172',
                          'N178','N179','N180','N188','N189','N19X','N990','O084','O904','P285','P290','P960','Q222','Q231','Q233','Z353',
                          'Z597','I210','I211','I212','I213','I214','I219','I220','I221','I228','I229','I230','I231','I232','I252','I256',
                          'P294','I200','I201','I208','I209','I10X','I110','I119','I120','I129','I130','I131','I132','I139','I150','I151']

familiar_con_dm = ['Antecedente familiar de diabetes','!']

codigos_dm_gestacional = ['O240','O241','O242','O243','O244','O249','P700','P701','P702']

codigos_ovario_poliquistico = ['E282','!']

codigos_acantosis = ['L83X','!']

## Consulta para crear tabla de examenes

SQL_examenes = f"""SELECT DISTINCT main.numero_identificacion_paciente, 
                Intolerancia_Glucosa.Intolerancia_Glucosa,
                Glicemia.Glicemia,
                hb.HbA1c,
                hdl.HDL,
                ldl.LDL,
                trigliceridos.trigliceridos,
                albuminuria.albuminuria

                
FROM `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa` as main

LEFT JOIN 
(SELECT numero_identificacion_paciente,Intolerancia_Glucosa, orden FROM (SELECT 
      *,
      ROW_NUMBER() over (PARTITION BY numero_identificacion_paciente ORDER BY fecha_apertura_folio desc) as orden
 FROM(SELECT
      numero_identificacion_paciente,
      fecha_apertura_folio,
      IF(examen_laboratorio in {tuple(examenes_glucosa)}, MAX(resultado_examen_laboratorio), 'No Aplica') as Intolerancia_Glucosa,
FROM
      `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`
WHERE fecha_apertura_folio >= '{fecha_para_tomar_examenes}'
      AND origen in ('EXAMENES LABORATORIO') 
      AND resultado_examen_laboratorio IS NOT NULL
GROUP BY    numero_identificacion_paciente, 
            examen_laboratorio,
            resultado_examen_laboratorio, 
            fecha_apertura_folio)

WHERE Intolerancia_Glucosa <>  'No Aplica') WHERE orden = 1
) as Intolerancia_Glucosa ON Intolerancia_Glucosa.numero_identificacion_paciente = main.numero_identificacion_paciente

LEFT JOIN (SELECT numero_identificacion_paciente,Glicemia, orden FROM (SELECT 
                              *,
                              ROW_NUMBER() over (PARTITION BY numero_identificacion_paciente ORDER BY fecha_apertura_folio desc) as orden
                        FROM(SELECT
                              numero_identificacion_paciente,
                              fecha_apertura_folio,
                              IF(examen_laboratorio in {tuple(examenes_glicemia)}, MAX(resultado_examen_laboratorio),  'No Aplica') as Glicemia,
                        FROM
                              `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`
                        WHERE fecha_apertura_folio >= '{fecha_para_tomar_examenes}'
                              AND origen in ('EXAMENES LABORATORIO') 
                              AND resultado_examen_laboratorio IS NOT NULL
                        GROUP BY    numero_identificacion_paciente, 
                                    examen_laboratorio,
                                    resultado_examen_laboratorio,
                                    fecha_apertura_folio)

                        WHERE Glicemia <>  'No Aplica') WHERE orden = 1) as Glicemia ON Glicemia.numero_identificacion_paciente = main.numero_identificacion_paciente

LEFT JOIN (SELECT numero_identificacion_paciente,HbA1c, orden FROM (SELECT 
                              *,
                              ROW_NUMBER() over (PARTITION BY numero_identificacion_paciente ORDER BY fecha_apertura_folio desc) as orden
                        FROM(SELECT
                              numero_identificacion_paciente,
                              fecha_apertura_folio,
                              IF(examen_laboratorio in {tuple(examenes_hba1c)}, MAX(resultado_examen_laboratorio), 'No Aplica') as HbA1c,
                        FROM
                              `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`
                        WHERE fecha_apertura_folio >= '{fecha_para_tomar_examenes}'
                              AND origen in ('EXAMENES LABORATORIO') 
                              AND resultado_examen_laboratorio IS NOT NULL
                        GROUP BY    numero_identificacion_paciente, 
                                    examen_laboratorio,
                                    resultado_examen_laboratorio,
                                    fecha_apertura_folio)

                        WHERE HbA1c <>  'No Aplica') WHERE orden = 1 ) as hb ON hb.numero_identificacion_paciente = main.numero_identificacion_paciente

LEFT JOIN (SELECT numero_identificacion_paciente,HDL, orden FROM (SELECT 
                              *,
                              ROW_NUMBER() over (PARTITION BY numero_identificacion_paciente ORDER BY fecha_apertura_folio desc) as orden
                        FROM(SELECT
                              numero_identificacion_paciente,
                              fecha_apertura_folio,
                              IF(examen_laboratorio in {tuple(examenes_hdl)}, MIN(resultado_examen_laboratorio), 'No Aplica') as HDL,
                        FROM
                              `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`
                        WHERE fecha_apertura_folio >= '{fecha_para_tomar_examenes}'
                              AND origen in ('EXAMENES LABORATORIO') 
                              AND resultado_examen_laboratorio IS NOT NULL
                        GROUP BY    numero_identificacion_paciente, 
                                    examen_laboratorio,
                                    resultado_examen_laboratorio,
                                    fecha_apertura_folio)

                        WHERE HDL <>  'No Aplica') WHERE orden = 1 ) as hdl ON hdl.numero_identificacion_paciente = main.numero_identificacion_paciente

LEFT JOIN (SELECT numero_identificacion_paciente,LDL, orden FROM (SELECT 
                              *,
                              ROW_NUMBER() over (PARTITION BY numero_identificacion_paciente ORDER BY fecha_apertura_folio desc) as orden
                        FROM(SELECT
                              numero_identificacion_paciente,
                              fecha_apertura_folio,
                              IF(examen_laboratorio in {tuple(examenes_ldl)}, MAX(resultado_examen_laboratorio), 'No Aplica') as LDL,
                        FROM
                              `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`
                        WHERE fecha_apertura_folio >= '{fecha_para_tomar_examenes}'
                              AND origen in ('EXAMENES LABORATORIO') 
                              AND resultado_examen_laboratorio IS NOT NULL
                        GROUP BY    numero_identificacion_paciente, 
                                    examen_laboratorio,
                                    resultado_examen_laboratorio,
                                    fecha_apertura_folio)

                        WHERE ldl <>  'No Aplica') WHERE orden = 1 ) as ldl ON ldl.numero_identificacion_paciente = main.numero_identificacion_paciente

LEFT JOIN (SELECT numero_identificacion_paciente,trigliceridos, orden FROM (SELECT 
                              *,
                              ROW_NUMBER() over (PARTITION BY numero_identificacion_paciente ORDER BY fecha_apertura_folio desc) as orden
                        FROM(SELECT
                              numero_identificacion_paciente,
                              fecha_apertura_folio,
                              IF(examen_laboratorio in {tuple(examenes_trigliceridos)}, MAX(resultado_examen_laboratorio), 'No Aplica') as trigliceridos,
                        FROM
                              `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`
                        WHERE fecha_apertura_folio >= '{fecha_para_tomar_examenes}'
                              AND origen in ('EXAMENES LABORATORIO') 
                              AND resultado_examen_laboratorio IS NOT NULL
                        GROUP BY    numero_identificacion_paciente, 
                                    examen_laboratorio,
                                    resultado_examen_laboratorio,
                                    fecha_apertura_folio)

                        WHERE trigliceridos <>  'No Aplica') WHERE orden = 1 ) as trigliceridos ON trigliceridos.numero_identificacion_paciente = main.numero_identificacion_paciente

LEFT JOIN (SELECT numero_identificacion_paciente,albuminuria, orden FROM (SELECT 
                              *,
                              ROW_NUMBER() over (PARTITION BY numero_identificacion_paciente ORDER BY fecha_apertura_folio desc) as orden
                        FROM(SELECT
                              numero_identificacion_paciente,
                              fecha_apertura_folio,
                              IF(examen_laboratorio in {tuple(examenes_albuminuria)}, MAX(resultado_examen_laboratorio), 'No Aplica') as albuminuria,
                        FROM
                              `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`
                        WHERE fecha_apertura_folio >= '{fecha_para_tomar_examenes}'
                              AND origen in ('EXAMENES LABORATORIO') 
                              AND resultado_examen_laboratorio IS NOT NULL
                        GROUP BY    numero_identificacion_paciente, 
                                    examen_laboratorio,
                                    resultado_examen_laboratorio,
                                    fecha_apertura_folio)

                        WHERE albuminuria <>  'No Aplica') WHERE orden = 1 ) as albuminuria ON albuminuria.numero_identificacion_paciente = main.numero_identificacion_paciente

                        WHERE Intolerancia_Glucosa.Intolerancia_Glucosa NOT IN ('PENDIENTE')
OR Glicemia.Glicemia NOT IN ('PENDIENTE','VER ANEXO')
OR hb.HbA1c NOT IN ('PENDIENTE','VER ANEXO')
OR hdl.HDL NOT IN ('PENDIENTE','VER ANEXO')
OR ldl.LDL NOT IN ('PENDIENTE','VER ANEXO','COMENTARIO')
OR trigliceridos.trigliceridos NOT IN ('PENDIENTE','VER ANEXO')
OR albuminuria.albuminuria NOT IN ('(FE)','*******','PENDIENTE')

"""

## Consulta para la tabla de comañias por usuario

SQL_compania = """SELECT
                        DISTINCT
                        numero_identificacion_paciente,
                        IF(conteo = 2, '2', compania) as compania
                        FROM (
                        SELECT
                            DISTINCT 
                            main.numero_identificacion_paciente,
                            second.conteo,
                            IF(main.compania_aseguradora IN ('30','31'), '0','1') AS compania
                        FROM
                            `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa` AS main
                        LEFT JOIN (
                            SELECT
                            numero_identificacion_paciente,
                            COUNT(1) AS conteo
                            FROM (
                            SELECT
                                DISTINCT 
                                numero_identificacion_paciente,
                                IF(compania_aseguradora IN ('30','31'), '0','1') AS compania
                            FROM
                                `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`
                            WHERE
                                compania_aseguradora IS NOT NULL)
                            GROUP BY
                            numero_identificacion_paciente) AS second
                        ON
                            second.numero_identificacion_paciente = main.numero_identificacion_paciente
                        WHERE
                            main.compania_aseguradora IS NOT NULL
                        ORDER BY second.conteo, main.numero_identificacion_paciente DESC)"""

## Consulta para los antecedentes de cada usuario

SQL_antecedentes = f"""SELECT DISTINCT main.numero_identificacion_paciente,
                hipertension.med_hipertension,
                fam_dm.familiar_dm,
                cardio.ant_cardiovascular,
                ovario_poliquistico.ovario_poliquistico,
                dm_gestacional.dm_gestacional,
                acantosis.acantosis_nigricans
                
FROM `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa` as main
LEFT JOIN 
(SELECT * FROM (SELECT
  *,
  ROW_NUMBER() OVER (PARTITION BY numero_identificacion_paciente ORDER BY med_hipertension DESC) AS orden
FROM (
  SELECT
    numero_identificacion_paciente,
  IF
    (codigo_atc IN {tuple(codigos_medicamentos_hipertension)},1,0) AS med_hipertension,
  FROM
    `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`))

WHERE orden = 1) as hipertension ON hipertension.numero_identificacion_paciente = main.numero_identificacion_paciente

LEFT JOIN 
(SELECT * FROM (SELECT
  *,
  ROW_NUMBER() OVER (PARTITION BY numero_identificacion_paciente ORDER BY familiar_dm DESC) AS orden
FROM (
  SELECT
    numero_identificacion_paciente,
    IF(dx_corta in {tuple(familiar_con_dm)} ,1,0) as familiar_dm,
  FROM
    `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`))

WHERE orden = 1) as fam_dm ON fam_dm.numero_identificacion_paciente = main.numero_identificacion_paciente

LEFT JOIN 
(SELECT * FROM (SELECT
  *,
  ROW_NUMBER() OVER (PARTITION BY numero_identificacion_paciente ORDER BY ant_cardiovascular DESC) AS orden
FROM (
  SELECT
    numero_identificacion_paciente,
    IF(codigo_dx in {tuple(codigos_cardiovascular)},1,0) as ant_cardiovascular,
  FROM
    `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`))

WHERE orden = 1) as cardio ON cardio.numero_identificacion_paciente = main.numero_identificacion_paciente

LEFT JOIN 
(SELECT * FROM (SELECT
  *,
  ROW_NUMBER() OVER (PARTITION BY numero_identificacion_paciente ORDER BY ovario_poliquistico DESC) AS orden
FROM (
  SELECT
    numero_identificacion_paciente,
    IF(codigo_dx in {tuple(codigos_ovario_poliquistico)},1,0) as ovario_poliquistico,
  FROM
    `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`))

WHERE orden = 1) as ovario_poliquistico ON ovario_poliquistico.numero_identificacion_paciente = main.numero_identificacion_paciente

LEFT JOIN 
(SELECT * FROM (SELECT
  *,
  ROW_NUMBER() OVER (PARTITION BY numero_identificacion_paciente ORDER BY dm_gestacional DESC) AS orden
FROM (
  SELECT
    numero_identificacion_paciente,
    IF(codigo_dx in {tuple(codigos_dm_gestacional)},1,0) as dm_gestacional,
  FROM
    `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`))

WHERE orden = 1) as dm_gestacional ON dm_gestacional.numero_identificacion_paciente = main.numero_identificacion_paciente

LEFT JOIN 
(SELECT * FROM (SELECT
  *,
  ROW_NUMBER() OVER (PARTITION BY numero_identificacion_paciente ORDER BY acantosis_nigricans DESC) AS orden
FROM (
  SELECT
    numero_identificacion_paciente,
    IF(codigo_dx in {tuple(codigos_acantosis)},1,0) as acantosis_nigricans,
  FROM
    `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`))

WHERE orden = 1) as acantosis ON acantosis.numero_identificacion_paciente = main.numero_identificacion_paciente"""

## Consulta para tabla con los perimetros abdominales

SQL_perimetros = """SELECT numero_identificacion_paciente, PERIMETRO_ABDOMINAL, orden  FROM (SELECT
                            DISTINCT main.folio,
                            main.fecha_apertura_folio,
                            ROW_NUMBER() over (PARTITION BY main.numero_identificacion_paciente ORDER BY main.fecha_apertura_folio desc) as orden,
                            main.numero_identificacion_paciente,
                            main.genero_paciente,
                            perimetro.PERIMETRO_ABDOMINAL
                          FROM
                            `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa` AS main
                          INNER JOIN (
                            SELECT
                              DISTINCT FOLIO,
                              PERIMETRO_ABDOMINAL
                            FROM
                              `prj-dev-repository-col.bq_raw_zone_avicena.HIS_TB_EXAMEN_FISICO`
                            WHERE
                              PERIMETRO_ABDOMINAL IS NOT NULL) AS perimetro
                          ON
                            main.folio = perimetro.FOLIO
                          WHERE
                            main.fecha_apertura_folio >= '2022-10-01')

                          WHERE orden = 1"""

## Consulta para la tabla de actividad fisica por cada usuario

SQL_ejercicio = """SELECT
  DISTINCT folio.FOLIO,
  pregunta.RESPUESTA_ANTECEDENTE,
  pregunta.PARAM_ITEM_RESPUESTA,
  respuesta.DESCRIPCION_ALTERNA hace_ejercicio
FROM
  `prj-dev-repository-col.bq_raw_zone_avicena.HIS_TB_RESP_ANTECEDEN_ITEM` AS pregunta
INNER JOIN (
  SELECT
    *
  FROM
    `prj-dev-repository-col.bq_raw_zone_avicena.HIS_TB_ENC_PARAMETRO`) AS respuesta
ON
  pregunta.PARAM_ITEM_RESPUESTA = respuesta.PARAMETRO
INNER JOIN (
  SELECT
    RESPUESTA_ANTECEDENTE,
    FOLIO
  FROM
    `prj-dev-repository-col.bq_raw_zone_avicena.HIS_TB_RESP_ANTECEDENTE`) AS folio
ON
  folio.RESPUESTA_ANTECEDENTE = pregunta.RESPUESTA_ANTECEDENTE
WHERE
  pregunta.PREGUNTA = 1441
  AND pregunta.PARAM_ITEM_RESPUESTA IS NOT NULL"""

## Consulta principal

SQL_diabetes = """SELECT * FROM  (SELECT 
                              DISTINCT
                              exam.tipo_identificacion_paciente,
                              exam.numero_identificacion_paciente,
                              DATE_DIFF(CURRENT_DATE(),DATETIME(exam.fecha_nacimiento_paciente),YEAR) AS edad,
                              IF(exam.genero_paciente = 'Femenino', 0, 1) as genero,
                              exam.codigo_ciudad_sucursal,
                              exam.nivel_academico_paciente,
                              compania.compania,
                              exam.raza_paciente,
                              peso.peso,
                              peso.talla,
                              peso.imc,
                              labs.Glicemia as Glicemia,
                              labs.Intolerancia_Glucosa as Intolerancia_Glucosa,
                              labs.HbA1c as HbA1c,
                              labs.HDL as HDL,
                              labs.LDL as LDL,
                              labs.trigliceridos as trigliceridos,
                              labs.albuminuria as albuminuria,
                              antecedentes.med_hipertension,
                              antecedentes.familiar_dm,
                              antecedentes.ant_cardiovascular,
                              antecedentes.ovario_poliquistico,
                              antecedentes.dm_gestacional,
                              antecedentes.acantosis_nigricans,
                              perimetros.PERIMETRO_ABDOMINAL,
                              ejercicio.hace_ejercicio,
                              IF(CAST(Glicemia AS FLOAT64) > 100, 2,0) as ind_1,
                              IF(CAST(HDL AS FLOAT64) < 35, 1,0) as ind_2,
                              IF(CAST(LDL AS FLOAT64) > 150,1,0) as ind_3,
                              IF(CAST(trigliceridos AS FLOAT64) >= 250,1,0) as ind_4
                        FROM `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa` as exam 

                    INNER JOIN (SELECT * FROM (SELECT  numero_identificacion_paciente,
                                        peso,
                                        talla,
                                        peso/(talla*talla) AS imc,
                                        ROW_NUMBER() over (PARTITION BY numero_identificacion_paciente ORDER BY fecha_apertura_folio desc) as orden
                              FROM `prj-dev-repository-col.bq_finalzone_avicena.consulta_externa`
                              WHERE fecha_apertura_folio >= '2023-04-01' AND peso IS NOT NULL AND talla IS NOT NULL) WHERE orden = 1) as peso

                    ON peso.numero_identificacion_paciente = exam.numero_identificacion_paciente

                    INNER JOIN `co-keralty-costomedico.Diabetes_avicena.examenes_por_usuarios` as labs ON labs.numero_identificacion_paciente = exam.numero_identificacion_paciente
                    INNER JOIN `co-keralty-costomedico.Diabetes_avicena.compania_x_usuarios` as compania ON compania.numero_identificacion_paciente = exam.numero_identificacion_paciente
                    INNER JOIN `co-keralty-costomedico.Diabetes_avicena.perimetros_x_usuarios` as perimetros ON perimetros.numero_identificacion_paciente = exam.numero_identificacion_paciente
                    INNER JOIN `co-keralty-costomedico.Diabetes_avicena.actividadFisica_x_usuarios` as ejercicio ON ejercicio.FOLIO = exam.folio


                  INNER JOIN `co-keralty-costomedico.Diabetes_avicena.antecedentes_x_usuario` as antecedentes ON antecedentes.numero_identificacion_paciente = exam.numero_identificacion_paciente

                    WHERE exam.origen = 'EXAMENES' AND 
                          peso.peso IS NOT NULL  
                          AND peso.talla IS NOT NULL 
                          AND exam.numero_identificacion_paciente IS NOT NULL 
                          AND exam.genero_paciente IS NOT NULL
                          AND exam.fecha_apertura_folio BETWEEN '2022-01-01' AND '2023-12-31'
                          )

                    WHERE imc > 4 AND Glicemia NOT IN ('PENDIENTE','VER ANEXO')
                          AND HDL NOT IN ('PENDIENTE','VER ANEXO')
                          AND trigliceridos NOT IN ('PENDIENTE','VER ANEXO')
                          AND LDL NOT IN ('PENDIENTE','VER ANEXO','COMENTARIO')"""


## Consulta de la informacion para entrenar

SQL_train = """SELECT tipo_identificacion_paciente,
  numero_identificacion_paciente,
  edad,
  genero,
  codigo_ciudad_sucursal,
  nivel_academico_paciente,
  compania,
  raza_paciente,
  peso,
  talla,
  imc,
  Glicemia,
  HbA1c,
  HDL,
  LDL,
  trigliceridos,
  med_hipertension,
  familiar_dm,
  ant_cardiovascular,
  ovario_poliquistico,
  dm_gestacional,
  acantosis_nigricans,
  PERIMETRO_ABDOMINAL,
  hace_ejercicio,
  riesgo,
  findrisc,
  IF(findrisc <= 7, riesgo, IF(findrisc <= 11,3+riesgo,IF(findrisc <= 14, 6+riesgo,IF(findrisc<=20,13+riesgo,IF(findrisc>20,18+riesgo,18+riesgo))))) as riesgo_final FROM 
  (SELECT
  tipo_identificacion_paciente,
  numero_identificacion_paciente,
  edad,
  genero,
  codigo_ciudad_sucursal,
  nivel_academico_paciente,
  compania,
  raza_paciente,
  peso,
  talla,
  imc,
  Glicemia,
  HbA1c,
  HDL,
  LDL,
  trigliceridos,
  med_hipertension,
  familiar_dm,
  ant_cardiovascular,
  ovario_poliquistico,
  dm_gestacional,
  acantosis_nigricans,
  PERIMETRO_ABDOMINAL,
  hace_ejercicio,
  ind_1 + ind_2 + ind_3 + ind_4 as Riesgo,
  (IF(edad < 45, 0,IF(edad < 64,2,4))  +
  IF(imc < 25, 0,IF(imc < 30,1,3))  +
  IF(genero = 0,IF(PERIMETRO_ABDOMINAL < 90,0,4),IF(PERIMETRO_ABDOMINAL < 94,0,4))  +
  IF(hace_ejercicio in ('40 minutos\\n', '60 minutos\\n'), 0,2)  +
  IF(med_hipertension = 1, 2,0)  +
  IF(CAST(Glicemia AS FLOAT64) > 100, 5,0)  +
  IF(familiar_dm = 1, 4,0)  ) as findrisc
FROM
  `co-keralty-costomedico.Diabetes_avicena.diabetes`
WHERE
  Glicemia IS NOT NULL
  AND HDL IS NOT NULL
  AND LDL IS NOT NULL
  AND trigliceridos IS NOT NULL)"""