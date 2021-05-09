sold = '''
with table_header as
(
select
'1' as f1,
'doc_payment' as f2,
'' as f3,
cast(fak.date_sdelka as date) as f4,
'400' as f5,
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
'' as f44,
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
