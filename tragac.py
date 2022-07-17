import re
import csv

#************* manipulacija txt podacima, dobijenih iz pdf dokumenta. Radi se o isporucenoj robi
def procitaj_txt(naziv_txt):
    with open(naziv_txt, encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines

def pronadji_linije_sa_part_numberima(text):
    linije_sa_part_numebrima = list()
    for line in text:
        x = re.search("^\d{5}", line)
        if x is not None:
            linije_sa_part_numebrima.append(line)
    return linije_sa_part_numebrima

def find_ukupne_cene(procitan_text):
    ukupne_cene = list()
    for line in procitan_text:
        x = re.search("\d+\\.\d{2}$", line)
        if x is not None:
            ukupne_cene.append(x.group())
    return ukupne_cene

def find_single_cene(procitan_text):
    single_cene = list()
    for line in procitan_text:
        x = re.search("\d+\\.\d{2}", line)
        if x is not None:
            single_cene.append(x.group())
    return single_cene

def find_kolicine(procitan_text):
    kolicine = list()
    for line in procitan_text:
        x = re.search("\d+\\.\d{2}", line)
        if x is not None:
            indexes = x.span()
            #print(x.span())
            #print(indexes[0])
            short_line = line[indexes[0]-5:indexes[0]]
            y = re.search("\d+", short_line)
            if y is not None:
                kolicine.append(y.group())
                #print (y.group())
    return kolicine

def find_part_numbers(procitan_text):
    part_numbers = list()
    for line in procitan_text:
        x = re.search("^\d{5}", line)
        if x is not None:
            part_numbers.append(x.group())
    return part_numbers

def find_opisi(procitan_text):
    opisi = list()
    for line in procitan_text:
        x = re.search("\d+\\.\d{2}", line)
        if x is not None:
            single_cena = float(x.group())
            #print(x.span())
            y = re.search("\d+\\.\d{2}$", line)
            ukupna_cena = float(y.group())
            kolicina = ukupna_cena / single_cena
            #print('kolicina je {:f}'.format(kolicina))
            if kolicina < 10:
                index_kraja_opisa = x.span()[0] - 5
            elif kolicina < 100:
                index_kraja_opisa = x.span()[0] - 6
            else:
                index_kraja_opisa = x.span()[0] - 7
            opis = line[6:index_kraja_opisa]
            opisi.append(opis)
    return opisi


#***************** manipulacija csv podacima, dobijenim iz excel tabele u kojoj se beleze porudbine. Radi se o porucenoj robi
def ucitaj_csv(csv_file_name):
    poruceno = {}
    with open(csv_file_name, 'rt', newline='')  as csvfile:
        csvreader = csv.reader(csvfile, skipinitialspace=True)
        for row in csvreader:
            part_number = dodaj_nule_ispred_pn(row[0])
            if part_number not in poruceno.keys():
                curr_dict = dict()
                curr_dict['part_number']    = part_number
                curr_dict['opisi']          = row[1]
                curr_dict['kolicina']       = row[2]
                curr_dict['single_cena']    = row[3]
                curr_dict['ukupna_cena']    = row[4]
                poruceno[part_number] = curr_dict
            else:
                try:
                    poruceno[part_number]['kolicina'] = int(poruceno[part_number]['kolicina']) + int(row[2])
                    poruceno[part_number]['ukupna_cena'] = float(poruceno[part_number]['ukupna_cena']) + float(row[4])
                    poruceno[part_number]['part_number'] = part_number
                    poruceno[part_number]['opisi'] = row[1]
                    poruceno[part_number]['single_cena'] = row[3]
                except:
                    print ("Error bad number format at row:")
                    print (row)

    return poruceno

def dodaj_nule_ispred_pn(part_number):
    no_zeros = 5 - len(part_number)
    zeros = ''
    pn = part_number
    if no_zeros > 0:
        for dummy_i in range(no_zeros):
            zeros = "0" + zeros
        pn = zeros + part_number
    return pn


# obrada dobijenih podataka. Porucenih i isporucenih, njihovo uporedjivanje. Potraga za nedostajucim, viskovima, razlikama...
def sum_kolicina(poruceno):
    suma = 0.0
    ukupna_kolicina = 0
    for key in poruceno.keys():
        #print("{0:<5} - {1:<80} - {2:<6}".format(poruceno[key][0], poruceno[key][1], poruceno[key][4]))
        suma = suma + float(poruceno[key]['ukupna_cena'])
        ukupna_kolicina += int(poruceno[key]['kolicina'])
    return (ukupna_kolicina, suma)

def isporuceno(part_numebrs, opisi, single_cene, ukupne_cene):
    i = 0
    isporuceno = dict()
    for i in range(len(part_numbers)):
        curr_dict = dict()
        curr_dict['part_number']    = part_numebrs[i]
        curr_dict['opisi']          = opisi[i]
        kolicina                    = int(float(ukupne_cene[i]) / float(single_cene[i]))
        print(part_numbers[i] + ' - ' + str(kolicina))
        curr_dict['kolicina']       = kolicina
        curr_dict['single_cena']    = single_cene[i]
        curr_dict['ukupna_cena']    = ukupne_cene[i]
        if (part_numbers[i] not in isporuceno.keys()):
            isporuceno[part_numbers[i]] = curr_dict
        else:
            isporuceno[part_numebrs[i]]['kolicina']        = int(isporuceno[part_numbers[i]]['kolicina']) + kolicina
            isporuceno[part_numbers[i]]['ukupna_cena']    = float(isporuceno[part_numbers[i]]['ukupna_cena']) + float(ukupne_cene[i])

    return isporuceno

def nema_pn(poruceno, isporuceno):
    count = 0
    for pn in poruceno:
        if(pn not in isporuceno.keys()):
            print('PN nije pronadjen: {0:5}'.format(poruceno[pn]['part_number']))
            count += 1
    return count

def razlika_u_kolicini(poruceno, isporuceno):
    print('')
    print('Razlike u kolicinama, pojedinacnim i ukupnim cenama:')
    count = 0
    for pn in poruceno:
        kolicina0   = int(poruceno[pn]['kolicina'])
        s_cena0     = float(poruceno[pn]['single_cena'])
        u_cena0      = float(poruceno[pn]['ukupna_cena'])
        diff = False
        if (pn in isporuceno.keys()):
            kolicinad   = int(isporuceno[pn]['kolicina'])
            s_cenad     = float(isporuceno[pn]['single_cena'])
            u_cenad     = float(isporuceno[pn]['ukupna_cena'])
            if(kolicina0 != kolicinad):
                print('{3:<20}{0:>10} se ne slaze. Poruceno - {1:5d}  | isporuceno - {2:5d} '.format(pn, kolicina0, kolicinad, 'Kolicine za pn ')) 
                count += 1
                diff = True
            if(float(poruceno[pn]['single_cena']) != float(isporuceno[pn]['single_cena'])):
                print('{3:<20}{0:>10} se ne slaze. Poruceno - {1:5.2f}  | isporuceno - {2:5.2f} '.format(pn, s_cena0, s_cenad, 'Single cena za pn')) 
                count += 1
                diff = True
            if(float(poruceno[pn]['ukupna_cena']) != float(isporuceno[pn]['ukupna_cena'])):
                print('{3:<20}{0:>10} se ne slaze. Poruceno - {1:5.2f}  | isporuceno - {2:5.2f} '.format(pn, u_cena0, u_cenad, 'Ukupna cena za pn ')) 
                count += 1
                diff = True
            if(diff):
                print('---------------------------------------------------------------------------------')
    return count 


#**********logic  - glavni to programa********************************
text = procitaj_txt('d.txt')
#print (text[10])
print("**********************************")
lsapn = pronadji_linije_sa_part_numberima(text)
ukupne_cene = find_ukupne_cene(lsapn)
single_cene = find_single_cene(lsapn)
part_numbers = find_part_numbers(lsapn)
opisi = find_opisi(lsapn)
kolicine = find_kolicine(lsapn)

isporuceno = isporuceno(part_numbers, opisi, single_cene, ukupne_cene)

#for line in lsapn:
#    print(line)
#for line in ukupne_cene:
#    print("Ukupna cena u eurima je " + line)
#for line in single_cene:
#    print("Pojedinacna cena u eurima je " + line)
#for line in part_numbers:
#    print("part number je " + line)
#for line in opisi:
#    print("opis je " + line + "*")

print(str(len(lsapn)) + "-" + str(len(ukupne_cene)))
print("--------------------------------------------")
#print("{0:d} - {1:d}".format(len(lsapn), len(part_numbers)))

csv_file_name = '0.csv'
poruceno = ucitaj_csv(csv_file_name)
#for key in poruceno:
#    print(poruceno[key])
print("--------------------------------------------")
print('Poruceni artikli zbirno su: ')
suma_kol0 = sum_kolicina(poruceno)
ukupna_cena_m = 'Ukupna cena je: '
ukupno_poruceno_m = 'Ukupno poruceno artikala: '
ukupno_isporuceno_m = 'Ukupno isporuceno artikala: '
print('{0:<30}{1:>5d}'.format(ukupno_poruceno_m, suma_kol0[0])) 
print('{0:<30}{1:>5.2f}'.format(ukupna_cena_m, suma_kol0[1])) 
print('')
print('Isporuceni artikli zbirno su: ')
suma_kold = sum_kolicina(isporuceno)
print('{0:<30}{1:>5d}'.format(ukupno_isporuceno_m, suma_kold[0])) 
print('{0:<30}{1:>5.2f}'.format(ukupna_cena_m, suma_kold[1])) 

print('****************************************************')
print('****************************************************')
print('****************************************************')
print('REZULTAT UPOREDJIVANJA')
count_nema_pn = nema_pn(poruceno, isporuceno)
print('{0:<40}{1:>3d} part numbera'.format('U isporucenim nedostaje ukupno ', count_nema_pn)) 
print('-'*100)
count_visak_pn = nema_pn(isporuceno, poruceno)
print('{0:<40}{1:3d} part numbera'.format('U isporucenim postoji visak ukupno ', count_visak_pn)) 
print('*'*100)

count_ukupno_razlika = razlika_u_kolicini(poruceno, isporuceno)
print('Razlika je pronadjena u ukupno {0:2d} slucajeva.'.format(count_ukupno_razlika))

# print ('Poruceno keys: ')
# for pn in poruceno.keys():
#     print (pn)
# print ('David keys:  ')
# for dpn in isporuceno.keys():
#     print(dpn)