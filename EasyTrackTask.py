import camelot.io as camelot
import pandas
import glob
import os

class convertPDFtocsv:

    def __init__(self,filePath):
        self.path = filePath
        

    #Determine which Bank it is
    def classify_Bank(self):

        if 'bankA' in self.path:
            self.bankA()
        elif 'bankB' in self.path:
            self.bankB()
        elif 'bankC' in self.path:
            self.bankC()



    def bankA(self):
        
        #Read bankA statement
        tables = camelot.read_pdf(self.path,pages='all', flavor='stream')
        #Export each page of bankA pdf
        tables.export('./bank.csv', f='csv')
        self.removeExtraColumnsBankA()
        self.concatenateBankA()

    def removeExtraFiles(self,fileList):
        for fileName in fileList:
            os.remove(fileName)
    

    #Remove extra empty/incorrect columns due to incorrect pdf-csv file conversion
    def removeExtraColumnsBankA(self):
        fileList=sorted(glob.glob("./bank-page-*-table-1.csv"))
        for idx,filename in enumerate(fileList):
            df=pandas.read_csv(filename,skiprows=3)
            for columnName in df.columns:
                if("Unnamed" in columnName):
                    df.drop(columnName,axis=1,inplace=True)
                
                df.to_csv('./convert'+str(idx)+'.csv')
        self.removeExtraFiles(fileList)

    #Concatenates multiple csv files and remove duplicated Headers
    def concatenateBankA(self):
        fileList=sorted(glob.glob("./convert*.csv"))
        dfList = []
        colNames=['0','Value Date', 'Trans Reference', 'Description',
                'Nominal Amount/Quantity','Transaction Amount','Available Balance']
        for filename in fileList:
            df=pandas.read_csv(filename,header=None,skiprows=2)
            dfList.append(df)
        concatDf=pandas.concat(dfList,axis=0)
        concatDf.columns=colNames
        del concatDf['0']
        concatDf.to_csv("./bankASolution.csv",index=None)
        self.removeExtraFiles(fileList)

    def bankB(self):
        #Read bankB statement 
        tables = camelot.read_pdf(self.path, flavor='stream', columns=['72,95,209,327,442,529'],table_areas=['0,792,800,100'])

        #Export pages of bankB pdf
        tables.export('./bankB.csv', f='csv')
        #read data from the csv file
        df=pandas.read_csv('./bankB-page-1-table-1.csv',skiprows=4)

        # Merge Information and Empty Columns 
        df['InformationReplacing'] = df['Information'].fillna(df['Unnamed: 2'])

        # drop the Information and Unamed columns
        df['Information'] = df['InformationReplacing']
        df.to_csv('./tempB1.csv')

        
        #read tempB1 file
        df1=pandas.read_csv('./tempB1.csv')

        #Drop Unnecessary columns 
        for idx,columnName in enumerate(df1.columns):
            if("Unnamed" in columnName):
                df1.drop(columnName,axis=1,inplace=True)
        df1.drop('InformationReplacing',axis=1,inplace=True)

        #output bankB Solution
        df1.to_csv('./bankBSolution.csv')
        os.remove('./bankB-page-1-table-1.csv')
        os.remove('./tempb1.csv')



    def bankC(self):
        #Read bankC statement 
        #table area to keep only top table
        tables = camelot.read_pdf(self.path, flavor='stream',table_areas=['0,792,800,400'])

        #Export pages of bankC
        tables.export('./bankC.csv', f='csv')

        #read csv file
        df=pandas.read_csv('./bankC-page-1-table-1.csv',skiprows=1)

        #output bankC Solution
        df.to_csv('./bankCSolution.csv')
        os.remove('./bankC-page-1-table-1.csv')
        
 
# Enter pdf file
# bankA.pdf or bankB.pdf or bankC.pdf
A = convertPDFtocsv(input('Enter bank(*).pdf where * is type of Bank: '))
A.classify_Bank() 

