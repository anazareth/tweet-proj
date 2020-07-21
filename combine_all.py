import pandas as pd
import os


def main():
    user_file_name = r'meta\num_communities.xlsx'
    sname = 'accounts_gathered'
    user_list = pd.read_excel(user_file_name, sheet_name=sname).loc[:, 'Handle'].to_list()
    all_file_name = os.path.join('data', 'all_users_clean.csv')
    for username in user_list:
        print('------------Adding user ' + username + '------------')
        file_name = os.path.join('data', username + '_clean.csv')
        if not os.path.exists(all_file_name):
            new_df = pd.read_csv(file_name)
            print(str(len(new_df)) + ' rows read from file \'' + file_name+'\'')
        else:
            df = pd.read_csv(file_name)
            print(str(len(df)) + ' rows read from file \'' + file_name + '\'')
            all_df = pd.read_csv(all_file_name)
            print(str(len(all_df)) + ' rows read from file \'' + all_file_name + '\'')
            new_df = pd.concat((df, all_df), axis=0)
        new_df.to_csv(all_file_name, index=False)
        print(str(len(new_df)) + ' rows written to file \'' + all_file_name + '\'')


if __name__ == '__main__':
    main()
