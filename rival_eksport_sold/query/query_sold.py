sold = '''
with table_header as
(
select
'1' as f1,
'doc_payment' as f2,
'' as f3,
cast(fak.date_sdelka as date) as f4,
'4000' as f5,
users.name_cyr as f6,
'' as f7,
fak.number as f8,
'' as f9,
'' as f10,
'' as f11,
'' as f12,
'' as f13,
case
    when fak.tip = 0
then
    fak.tip + 1
else
    fak.tip
end as f14,
case
    when fak.tip = 0
    then 'Фактура'
    else 'КИ'
end as f15,
'' as f16,
'' as f17,
case
    when fak.firma_id = 1
then
    'ФЛ'
else
    'ЮЛ'
end as f18,
case
    when fak.firma_id is not null
    then firmi.name_fak
    else fak.mol
end as f19,
case
    when fak.firma_id is not null
    then firmi.bulstat
    else '999999999'
end as f20,
case
    when fak.firma_id is not null
    then coalesce(firmi.idnomdds, '')
    else '999999999'
end as f21,
'' as f22,
'' as f23,
'' as f24,
'' as f25,
'' as f26,
'' as f27,
'' as f28,
'' as f29,
'' as f30,
'' as f31,
'' as f32,
'' as f33,
'' as f34,
'' as f35,
'' as f36,
'' as f37,
'' as f38,
'' as f39,
'' as f40,
'' as f41,
'' as f42,
'' as f43,
case
    when fak.firma_id = 1
then
    'AGENT :'
else
    'PERSON :'
end as f44,
'' as f45,
--round(fak.suma, 2) as f46,
'' as f46,
'' as f47,
'' as f48
from fak
left join firmi on firmi.id = fak.firma_id
inner join pay_tip on pay_tip.id = fak.v_broi
inner join opr on opr.id = fak.opr_id
inner join users on users.id = opr.user_id
where fak.number between {first} and {last} and fak.is_deleted = 0
),
table_body as
(
 select
1 as b1,
'doc_line' as b2,
'' as b3,
cast(fak.date_sdelka as date) as b4,
'' as b5,
'' as b6,
'' as b7,
fak.number as b8,
'' as b9,
'' as b10,
'' as b11,
'' as b12,
'' as b13,
case
    when fak.tip = 0
then
    fak.tip + 1
else
    fak.tip
end as b14,
case
    when fak.tip = 0
    then 'Фактура'
    else 'КИ'
end as b15,
'' as b16,
'' as b17,
'' as b18,
case
    when fak.firma_id is not null
    then firmi.name_fak
    else fak.mol
end as b19,
case
    when fak.firma_id is not null
    then firmi.bulstat
    else '999999999'
end as b20,
case
    when fak.firma_id is not null
    then coalesce(firmi.idnomdds, '')
    else '999999999'
end as b21,
'' as b22,
'' as b23,
'' as b24,
'' as b25,
'' as b26,
'' as b27,
'' as b28,
'' as b29,
'' as b30,
'' as b31,
fak.v_broi as b32,
(select pay_tip.name_cyr from pay_tip where pay_tip.id = fak.v_broi) as b33,
'' as b34,
'' as b35,
fak_el.text as b36,
round(cast(fak_el.kol as int), 0) as b37,
'бр' as b38,
round(cast(fak_el.cena as decimal(10, 3)), 2) as b39,
'' as b40,
round(fak_el.suma_dds, 2) as b41,
dds_stavka.dds as b42,
round(fak_el.suma_total, 2) as b43,
'' as b44,
'' as b45,
case when fak_el.text like 'Депозит%' or (fak_el.text like 'Авансово плащане%') then 412
else 4119
end as b46,
'' as b47,
case when fak_el.text like 'Авансово плащане%' then right(fak_el.text, 10)
else ''
end as b48
from fak_el
inner join fak on fak.id = fak_el.fak_id
left join firmi on firmi.id = fak.firma_id
inner join dds_stavka on dds_stavka.id = fak_el.dds_id
inner join pay_tip on pay_tip.id = fak.v_broi
where fak_el.fak_id = fak.id and fak.number between {first} and {last} and fak.is_deleted = 0
)

select * from
(
select * from table_header
union all
select * from table_body
)
order by 8, 2 desc
'''

purhcase = """
with header as
(
select
case
    when fak_in.tip = 0 then 1 else fak_in.tip
end as first_dost1,
case
    when fak_in.tip = 0 then 'Фактура' else 'КИ'
end as first_dost2,
'' as first_dost3,
'Покупка на стоки' as first_dost4,
fak_in.number as first_dost5,
LPAD(extract(day from opr.opr_date), 2, 0) || '.' || LPAD(extract(month from opr.opr_date), 2, 0) || '.' || LPAD(extract(year from opr.opr_date), 4, 0) as first_dost6,
'' as first_dost7,
'' as first_dost8,
'304,' || sklad.code as first_dost9,
'' as first_dost10,
'' as first_dost11,
'' as first_dost12,
sklad.name as first_dost13,
'' as first_dost14,
'' as first_dost15,
'' as first_dost16,
'' as first_dost17,
firmi.name_fak as first_dost18,
coalesce(firmi.idnomdds, '') as first_dost19,
firmi.bulstat as first_dost20,
'' as first_dost21,
'' as first_dost22,
'' as first_dost23,
'' as first_dost24,
'' as first_dost25,
'' as first_dost26,
fak_in.suma as first_dost27,
'' as first_dost28,
'' as first_dost29,
case
   when fak_in.pay_tip = 0 then 'В БРОИ'
   else 'БАНКОВ ПРЕВОД'
end as first_dost30,
case
   when fak_in.pay_tip = 0 then 501
   else 503
end as first_dost31
from fak_in
inner join opr on opr.id = fak_in.opr_id
inner join sklad on sklad.id = fak_in.sklad_id
inner join firmi on firmi.id = opr.kli_id
--where cast(opr.datetime as date) between '01.06.2021' and '01.06.2021'
where cast(opr.datetime as date) between '{first}' and '{last}'
--where fak_in.number between {first} and {last}
),
footer as (
select
case
    when fak_in.tip = 0 then 1 else fak_in.tip
end as first_dost1,
case
    when fak_in.tip = 0 then 'Фактура' else 'КИ'
end as first_dost2,
'20' as first_dost3,
'Покупка на стоки' as first_dost4,
fak_in.number as first_dost5,
LPAD(extract(day from opr.opr_date), 2, 0) || '.' || LPAD(extract(month from opr.opr_date), 2, 0) || '.' || LPAD(extract(year from opr.opr_date), 4, 0) as first_dost6,
'' as first_dost7,
'' as first_dost8,
'' as first_dost9,
'' as first_dost10,
'' as first_dost11,
'' as first_dost12,
sklad.name as first_dost13,
'' as first_dost14,
'' as first_dost15,
'' as first_dost16,
'' as first_dost17,
firmi.name_fak as first_dost18,
coalesce(firmi.idnomdds, '') as first_dost19,
firmi.bulstat as first_dost20,
'' as first_dost21,
'' as first_dost22,
'' as first_dost23,
'' as first_dost24,
'' as first_dost25,
'' as first_dost26,
fak_in.suma as first_dost27,
round(fak_in.dds, 3) as first_dost28,
round(fak_in.total, 2) as first_dost29,
case
   when fak_in.pay_tip = 0 then 'В БРОИ'
   else 'БАНКОВ ПРЕВОД'
end as first_dost30,
case
   when fak_in.pay_tip = 0 then 501
   else 503
end as first_dost31
from fak_in
inner join opr on opr.id = fak_in.opr_id
inner join sklad on sklad.id = fak_in.sklad_id
inner join firmi on firmi.id = opr.kli_id
--where cast(opr.datetime as date) between '01.06.2021' and '01.06.2021'
where cast(opr.datetime as date) between '{first}' and '{last}'
--where fak_in.number between {first} and {last}
)
select * from header
union all
select * from footer
order by 5, 3
"""
