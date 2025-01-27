import glob
import re
from datetime import datetime
from unidecode import unidecode

import fitz


PATH = '../input/yandex'
FILENAMES = glob.glob(PATH + '/*.pdf')


def get_transactions():
    transactions = []

    for filename in FILENAMES:
        file = fitz.open(filename)
        # pat_date = re.compile(r'(\d{2}.\d{2}.\d{4})')
        # pat_time = re.compile(r'(\d{2}:\d{2})')
        num_fields = 5

        for page in file:
            rows = page.get_text().split('\n')
            i = 11
            # if page.number == 1:
            #     i = 23
            # else:
            #     i = 12
            oper_flg = False
            while i < len(rows) - 1:
                oper_text = ''

                # if re.match('Страница [0-9]+ из [0-9]+', rows[i]) is not None:
                #     break
                if rows[i] == 'ЭСП':
                    oper_flg = True
                    i += 1
                if oper_flg and re.match('Страница [0-9]+ из [0-9]+', rows[i]) is None:
                    while i < len(rows) - 1 and re.match(r'(\d{2}.\d{2}.\d{4})',rows[i]) is None:
                        oper_text = ' '.join((oper_text, rows[i]))
                        i+=1
                    if re.match('Страница [0-9]+ из [0-9]+', rows[i]) is not None or i >= len(rows) - num_fields:
                        break
                    category = re.sub(r'^\s+|\s+$','', re.search(r'^[а-яА-Я ]+',oper_text).group(0))
                    text = re.sub(r'^\s+','',oper_text)
                    trans_date = rows[i][:10]
                    trans_time = rows[i + 1][2:7]

                    # if pat_date.search(trans_date) and pat_time.search(trans_time):
                    if re.match(r'\*\d{4}',rows[i+3]) is not None:
                        num_fields = 6
                        transfer_date, _, trans_sum_str = rows[i + 2:i + num_fields-1]
                    else:
                        num_fields = 5
                        transfer_date, trans_sum_str = rows[i + 2:i + num_fields-1]


                    trans_sum_str = unidecode(trans_sum_str).replace(' ', '').replace(',', '.').replace('R','')
                    trans_sum = float(trans_sum_str[1:])

                    debit = trans_sum if trans_sum_str[0] == '+' else 0
                    credit = trans_sum if trans_sum_str[0] != '+' else 0

                    transaction = {
                        'bank': 'YNDX',
                        'trans_datetime': datetime.strptime(' '.join((trans_date, trans_time)),
                                                            '%d.%m.%Y %H:%M'),
                        'transfer_datetime': datetime.strptime(transfer_date, '%d.%m.%Y'),
                        'auth_code': None,
                        'category': category,
                        'debit': debit,
                        'credit': credit,
                        'text': text
                    }

                    transactions.append(transaction)
                    i += num_fields
                    # else:
                    #     if len(transactions) != 0:
                    #         transactions[-1]['text'] += ' ' + rows[i]
                    #     i += 1
                else:
                    if len(transactions) != 0:
                        transactions[-1]['text'] += ' ' + rows[i]
                    i += 1

    return transactions


if __name__ == '__main__':
    transaction = get_transactions()
    print(transaction)
