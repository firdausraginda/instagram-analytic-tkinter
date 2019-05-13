# tanpa custom lex, akurasi lvl dokumen 90% tapi lvl kalimat rendah
# lexCustom = []

# akurasi lvl dokumen 90% dan lvl kalimat lebih tinggi
# lexCustom = [['tidak ada', 0], ['ga ada', 0], ['masukkan', -1], ['masukan', -1]]

lexCustom = [['cerita', 0], ['saya', 0], ['aku', 0], ['selama', 0], ['tidak ada', 0], ['ga ada', 0], ['yang', 0], ['pa', 0], ['bagus', 2], ['keren', 2],['sangat baik', 4], ['sangat bagus', 4], ['sangat menyenangkan', 3], ['cukup', 1], ['masukkan', -1], ['masukan', -1]]

# ga ada = tidak ada = 0
# masukkan dan masukan = saran = -1