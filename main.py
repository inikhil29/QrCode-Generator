import pyqrcode
import cairosvg
import pandas as panda
import os
import random
import string

def createQRPNG(text, filename = ""):
    qr = pyqrcode.create(text)
    if filename != "":
        qr.png(filename+'.png', scale=10)
    else:
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        qr.png(filename+".png", scale=10)

def getFileData(filepath):
    if filepath != "":
        filename_array = filepath.split('/')
        filename = filename_array[len(filename_array - 1)] if len(filename_array) > 1 else filename_array[0]
        if filename != "":
            file_extension_array = filename.split('.')
            file_extension = file_extension_array[len(file_extension_array) - 1] if len(file_extension_array) > 1 else ""
            if file_extension == "xlsx":
                try:
                    result = panda.read_excel(filepath)
                except IOError as e:
                    print("Something Went Wrong Please Check Again : \n"+e)
                else:
                    total_items = len(result.index.values)
                    return {
                        "data":result,
                        "total_items": total_items,
                        "keys": result.keys().tolist(),
                        "total_keys": len(result.keys().tolist())
                    }
            elif file_extension == "csv":
                try:
                    result = panda.read_csv(filepath)
                except IOError as e:
                    print("Something Went Wrong Please Check Again : \n"+e)
                else:
                    total_items = len(result.index.values)
                    return {
                        "data":result,
                        "total_items": total_items,
                        "keys": result.keys().tolist(),
                        "total_keys": len(result.keys().tolist())
                    }
            else:
                return ""
def getCoustomizedKeys(keys, total):
    key_mapping = {}
    if input("\nDo you want to change the column name  OR Remove some unnecessary column if yes type 'yes' else enter any key : ") in ['yes', 'YES', 'Yes']:
        for i in range(total):
            choice = input("Current Column Name : --{}-- \n1.For Name Changing enter 1\n2.For Remove the Column enter 0\n3.To Continue please enter\nEnter Your Choice  : ".format(keys[i]))
            if choice == '1':
                key_mapping[keys[i]] = input("Enter the new name : ")
                print("Name Changed...\n")
            elif choice == '0':
                key_mapping[keys[i]] = 0
                print("Column Removed")
            else:
                 key_mapping[keys[i]] =  keys[i]
    else:
        key_mapping = {x:x for x in keys}
    return key_mapping

def changeOrderOfPrint(keys, total):
    print("-------------------------------------------------")
    for i in range(total):
        if keys[i] != 0:
            pass


def createQRCODE(data, keys, newkeys, index, print_name = False):
    print("keys: ", keys)
    print('newkeys : ', newkeys)
    text = ''
    for i in keys:
        if newkeys[i] != 0:
            text += (str(newkeys[i]) + ': '+str(data[i][index])+'\n') if print_name else  (str(data[i][index])+'\n')
    # print(text)
    createQRPNG(text)

if __name__ == "__main__":
    print("----------------------------------Welcome----------------------------------")
    #filepath = input('Enter Your File Path : ')
    print("\nExcel Files In Current Directory :")
    files = os.listdir(os.getcwd())
    files = [f for f in files if f.endswith('.csv') or f.endswith('.xlsx')] 
    for i in range(len(files)):
        print("{}. {}".format(i+1, files[i]))
    file_select = int(input("Enter Which File To Select : "))
    if file_select > len(files) or file_select <= 0:
        print("Error : Invalid Number Entered")
    else:
        print("\nYou Have Selected : {}".format(files[file_select - 1]))
        if input("\nFor Next Step Type 'Yes' ") in ['yes', 'YES', 'Yes']:
            getData = getFileData(files[file_select - 1]) 
            if getData != "":
                data = getData['data']
                keys = getData['keys']
                total = getData['total_items']
                total_keys = getData['total_keys']
                newKeys = {}
                # print(data)
                # exit
                print("\n\nColumn Names are : ")
                for i in range(total_keys):
                    print("{}.{}".format(i+1, keys[i]))
                if input("\nDo You Want To Coustomize if Yes type 'y' else type any key : ") in ['y', 'Y']:
                    newKeys = getCoustomizedKeys(keys, total_keys)
                else:
                    newKeys = {x : x for x in keys}
                item_len = len(data.index.values)
                # if input("\nDo You Want To Print The column name in the text if Yes type 'y' else type any key : ") in ['y', 'Y']:
                print_name = input("\nDo You Want To Print The column name in the text if Yes type 'y' else type any key : ") in ['y', 'Y']
                for i in range(item_len):
                    createQRCODE(data, keys, newKeys, i, print_name)
                







