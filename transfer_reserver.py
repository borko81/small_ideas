import csv
import fdb

FILE_NAME = 'res.csv'

path_to_database = {
    'host': '192.168.1.100',
    'database': 'flask',
    'user': 'SYSDBA',
    'password': 'masterkey'
}


def con_to_fb_database(query):
    ''' ВРЪЗКА С БАЗАТА '''
    con = fdb.connect(host=path_to_database['host'], database=path_to_database['database'],
                      user=path_to_database['user'], password=path_to_database['password'])
    cur = con.cursor()
    cur.execute(query)
    con.commit()


def insert_data(room, date, days, dogovor_id, counter_guest, ref_n, pansion, description, notes):
    query = '''
    execute block as
    declare variable R_ID integer;
    declare variable N_ID integer;
    declare variable MY_OPR_ID integer;
    declare variable GUEST_COUNT integer;
    declare variable ROOM_ID_GET integer;
    declare variable opr_id integer;
    declare variable smetka_nomer integer;
    declare variable mydepozit_id integer;
    declare variable def_nast_id integer;
    declare variable dog_id integer;
    begin
    GUEST_COUNT = '{counter_guest}';
    insert into opr (opr.opr_tip_id , opr.user_id, opr.pc_id) values (10, 1, 1)
    returning opr.id into :opr_id;

    insert into reserve (reserve.flag_titul, reserve.ref_no, reserve.fromwho, reserve.notes) values(0, '{ref_n}', '{description}' , '{notes}')
    RETURNING reserve.id INTO :R_ID;
    def_nast_id = null;
    while ( GUEST_COUNT > 0 ) do begin
        INSERT INTO nast (nast.room_id, nast.check_in_date, nast.days, nast.reserve_id, nast.last_opr_type, nast.dogovor_id, nast.pansion_id, nast.nast_id, nast.bulfor, nast.country_id, nast.flag_smetka)
        VALUES((select rooms.id from rooms where rooms.name = '{room}'), '{date}', '{days}', :R_ID, 1, '{dogovor_id}', '{pansion}', :def_nast_id, 1, 0, 1)
        returning nast.id into :N_ID;
        INSERT INTO nast_promo_node (nast_promo_node.nast_id, nast_promo_node.promo_paket_id, nast_promo_node.idx) VALUES (:n_id,  1, 1);
        GUEST_COUNT = GUEST_COUNT - 1;
        def_nast_id = coalesce(:def_nast_id, :n_id);
        insert into active_nast_reserve (active_nast_reserve.nast_id) values(:N_ID);
        insert into OPR  (OPR_TIP_ID, USER_ID, PC_ID) VALUES (1, 1,2)
        returning opr.id into :MY_OPR_ID;
        insert into RESERVE_HIST (RESERVE_ID, OPR_ID,NAST_ID) VALUES(:R_ID, :MY_OPR_ID, :N_ID);
    end
    end
    '''.format(room=room, date=date, days=days, dogovor_id=dogovor_id, counter_guest=counter_guest, ref_n=ref_n, pansion=pansion, description=description, notes=notes)
    con_to_fb_database(query)


def insert_data_without_pansion(room, date, days, dogovor_id, counter_guest, ref_n, description, notes):
    query = '''
    execute block as
    declare variable R_ID integer;
    declare variable N_ID integer;
    declare variable MY_OPR_ID integer;
    declare variable GUEST_COUNT integer;
    declare variable ROOM_ID_GET integer;
    declare variable opr_id integer;
    declare variable smetka_nomer integer;
    declare variable mydepozit_id integer;
    declare variable def_nast_id integer;
    begin
    GUEST_COUNT = '{counter_guest}';
    insert into opr (opr.opr_tip_id , opr.user_id, opr.pc_id) values (10, 1, 1)
    returning opr.id into :opr_id;

    insert into reserve (reserve.flag_titul, reserve.ref_no, reserve.fromwho, reserve.notes) values(0, '{ref_n}', '{description}' , '{notes}')
    RETURNING reserve.id INTO :R_ID;
    def_nast_id = null;
    while ( GUEST_COUNT > 0 ) do begin
        INSERT INTO nast (nast.room_id, nast.check_in_date, nast.days, nast.reserve_id, nast.last_opr_type, nast.dogovor_id, nast.nast_id, nast.bulfor, nast.country_id, nast.flag_smetka)
        VALUES((select rooms.id from rooms where rooms.name = '{room}'), '{date}', '{days}', :R_ID, 1, '{dogovor_id}', :def_nast_id, 1, 0, 1)
        returning nast.id into :N_ID;
        INSERT INTO nast_promo_node (nast_promo_node.nast_id, nast_promo_node.promo_paket_id, nast_promo_node.idx)
        VALUES (:n_id,  1, 1);
        GUEST_COUNT = GUEST_COUNT - 1;
        def_nast_id = coalesce(:def_nast_id, :n_id);
        insert into active_nast_reserve (active_nast_reserve.nast_id) values(:N_ID);
        insert into OPR  (OPR_TIP_ID, USER_ID, PC_ID) VALUES (1, 1,2)
        returning opr.id into :MY_OPR_ID;
        insert into RESERVE_HIST (RESERVE_ID, OPR_ID,NAST_ID) VALUES(:R_ID, :MY_OPR_ID, :N_ID);
    end
    end
    '''.format(room=room, date=date, days=days, dogovor_id=dogovor_id, counter_guest=counter_guest, ref_n=ref_n, description=description, notes=notes)
    con_to_fb_database(query)


with open(FILE_NAME, 'r') as f:
    csv_data = csv.reader(f, delimiter=';')
    for line in csv_data:
        ref_n = str(line[0].strip())
        date, days = line[1].split()
        date = date + '.2021'
        days = days.replace('(', '')
        days = days.replace(')', '')
        room = line[2]
        counter_guest = eval(line[3])
        dogovor_id = line[4]
        description = line[5]
        pansion = line[6]
        notes = line[8]
        if pansion.startswith('BB'):
            try:
                insert_data_without_pansion(room, date, days, dogovor_id, counter_guest, ref_n, description, notes)
            except:
                print(f'error in {ref_n}')
        else:
            pansion = 1
            try:
                insert_data(room, date, days, dogovor_id, counter_guest, ref_n, pansion, description, notes)
            except:
                print(f'error in {ref_n}')
