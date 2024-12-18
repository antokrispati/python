import pandas as pd

file1 = "Original.xlsx"
file2 = "Source.xlsx"

df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

kolom_kunci = "Serial Number"

#cek kolom
print("Kolom di df1", df1.columns)
print("Kolom di df2", df2.columns)

#cek jika tidak ada kolom serial number
if kolom_kunci in df1.columns and kolom_kunci in df2.columns:
    data_sama = df2[df2[kolom_kunci].isin(df1[kolom_kunci])]
else:
    print("Kolom 'Serial Number' tidak ditemukan dalam DataFrame.")


#simpan data
output_file = "data_duplikat.xlsx"
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    data_sama.to_excel(writer, index=False, sheet_name='Sheet1')
    
    #akses workbook dan worksheet untuk format
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    
    #hilangkan format tebal pada header
    header_format = workbook.add_format({'bold': False})
    for col_num, value in enumerate(data_sama.columns.values):
        worksheet.write(0, col_num, value, header_format)


print(f"Data yang sama telah disimpan di '{output_file}'")