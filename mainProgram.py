from getJSON import mainProgramGetJSON, getVeryPositiveComments, automateIgScraper, format1, format2, format3
# from sentimentAnalysisDocs import mainProgramSA

def mainProg(account, qtyPost, qtyAcc):

    accOwner = automateIgScraper(account, qtyPost)

    if(type(mainProgramGetJSON(accOwner, qtyAcc)) != str):
        hasilScrapingComAcc, hasilAccMenByUser, hasilSelCom, hasilGetPost, hasilSortLike, hasilSortComment, curAcc = mainProgramGetJSON(accOwner, qtyAcc)
        # hasilSentAnaly = mainProgramSA(hasilSelCom, curAcc)
        # hasilKomenMenarik = getVeryPositiveComments(hasilSentAnaly, curAcc)
        
        arrKeyComAcc, arrQtyComAcc = format1(hasilScrapingComAcc)
        # arrKeyMenByUser, arrQtyMenByUser = format1(hasilAccMenByUser)
        arrKeyGetPostLike, arrQtyGetPostLike = format2(hasilGetPost, 'like')
        arrKeyGetPostComment, arrQtyGetPostComment = format2(hasilGetPost, 'comment')
        # arrAccount, arrComment = format3(hasilKomenMenarik)

        # print(arrKeyComAcc)
        # print(arrQtyComAcc)
        # print('===============================================================')
        # print(arrKeyMenByUser)
        # print(arrQtyMenByUser)
        # print('===============================================================')
        # print(arrKeyGetPostLike)
        # print(arrQtyGetPostLike)
        # print('===============================================================')
        # print(arrKeyGetPostComment)
        # print(arrQtyGetPostComment)
        # print('===============================================================')
        # print(arrAccount)
        # print(arrComment)

        # print('akun yang paling banyak komen di instagram %s: %s' % (curAcc, hasilScrapingComAcc))
        # print('===============================================================')
        # print('akun yang paling banyak di mention oleh %s: %s' % (curAcc, hasilAccMenByUser))
        # print('===============================================================')
        # print('analisis sentimen sorted, filtered, cleaned comments %s' % (hasilKomenMenarik))
        # print('===============================================================')
        print('hasil post dengan like terbanyak: %s' % (hasilSortLike))
        print('===============================================================')
        print('hasil post dengan comment terbanyak: %s' % (hasilSortComment))

        return arrKeyComAcc, arrQtyComAcc, arrKeyGetPostLike, arrQtyGetPostLike, arrKeyGetPostComment, arrQtyGetPostComment, hasilSortLike, hasilSortComment, curAcc
        # return hasilScrapingComAcc, hasilAccMenByUser, hasilKomenMenarik, hasilSortLike, hasilSortComment

    else:
        return mainProgramGetJSON(accOwner, qtyAcc)
        # print(mainProgramGetJSON(accOwner, qtyAcc))

# mainProg('vilo.na', 10, 5)