# -------------import-------------
import json
from operator import itemgetter
import time
import os

# -------------tools-------------
def automateIgScraper(userName, qtyPost):
    destinationFile = "./accounts/%s" % (userName)
    os.system('instagram-scraper --comments -m %s %s -d %s --retry-forever' % (qtyPost, userName, destinationFile))
    returnFileJSON = destinationFile + '/%s.json' % (userName)

    return returnFileJSON

def openFile(dataAkun):
    exists = os.path.isfile(dataAkun)
    if exists:
        with open(dataAkun, encoding="utf8") as f:
            d = json.load(f)
            data = d
    else:
        data = 'EMPTY DATA'

    return data

def hapusAccountName(kalimat):
    kataArr = []
    accountName = []
    for i in range(0, len(kalimat)):
        if (kalimat[i] == '@'):
            temp = []
            kataArr.append(kalimat[i])
            for j in range(i, len(kalimat)):
                if(kalimat[j] != ' '):
                    temp.append(kalimat[j])
                    if(j == len(kalimat)-1):
                        temp = "".join(temp)
                        accountName.append(temp)
                else:
                    temp = "".join(temp)
                    accountName.append(temp)
                    break
        else:
            kataArr.append(kalimat[i])

    kataArr = "".join(kataArr)
    
    for kata in accountName:
        kataArr = kataArr.replace(kata, '')

    return kataArr

def findAllAccountName(kalimat):
    accountName = []
    for i in range(0, len(kalimat)):
        if (kalimat[i] == '@'):
            temp = []
            for j in range(i, len(kalimat)):
                if(kalimat[j] != ' '):
                    temp.append(kalimat[j])
                    if(j == len(kalimat)-1):
                        temp = "".join(temp)
                        accountName.append(temp)
                else:
                    temp = "".join(temp)
                    accountName.append(temp)
                    break

    return accountName

def tambahAt(kata):
    return '@%s' % kata

def removeEmoticon(kalimat):
    return kalimat.encode('ascii', 'ignore').decode('ascii')

def cutRanking(data, potongke, desc):
    if len(data) != 0:
        if (potongke == 'all'):
            return data
        else:
            if (potongke > len(data)):
                # print('jumlah data %s hanya %s, sedangkan yang anda minta %s' % (desc, len(data), potongke))
                return data[:len(data)]
            else:
                return data[:potongke]
    else:
        # print('data kosong')
        return 'EMPTY DATA'

def isPostEmpty(accOwner):
    if (len(accOwner['GraphImages'])) > 0:
        return False
    else:
        return True

def getAccountOwner(accOwner):
    return accOwner['GraphImages'][0]['username']

def removeNullItemInArr(arr):
    arrNotNull = []
    for data in arr:
        if (data.isspace() or data == ''):
            continue
        else:
            arrNotNull.append(data)

    return arrNotNull

def filterSentiScore(data, minSentiScore):
    filterData = []
    for i in range(0, len(data)):
        if (data[i][1] >= minSentiScore):
            filterData.append(data[i])

    return filterData

def convertTime(timeData):
    ts = time.gmtime(timeData)
    # return time.strftime("%Y-%m-%d", ts)
    return time.strftime("%Y-%m-%d at %H:%M:%S ", ts)

def findCountLike(val):
    return val['count like']

def findCountComment(val):
    return val['count comment']

def sortPost(data):
    sortedLike = sorted(data, key=findCountLike, reverse=True)
    sortedComment = sorted(data, key=findCountComment, reverse=True)

    hasilCutLike = cutRanking(sortedLike, 3, 'sorting like post')
    hasilCutComment = cutRanking(sortedComment, 3, 'sorting comment post')
    
    return hasilCutLike, hasilCutComment

def format1(data):
    arrUsername = []
    arrQty = []

    for i in range(len(data)):
        arrUsername.append(data[i][0])
        arrQty.append(data[i][1])

    return arrUsername, arrQty

def format2(data, key):
    arrTime = []
    arrQty = []
    for i in reversed(range(len(data))):
        if key == 'like':
            arrTime.append(data[i]['time'])
            arrQty.append(data[i]['count like'])
        else:            
            arrTime.append(data[i]['time'])
            arrQty.append(data[i]['count comment'])
    
    return arrTime, arrQty

def format3(data):
    arrAccount = []
    arrComment = []
    for i in range(len(data['all sorted ranked comments'])):
        for j in range(len(data['all sorted ranked comments'][i]['sorted ranked comments'])):
            arrAccount.append(data['all sorted ranked comments'][i]['account name'])
            arrComment.append(data['all sorted ranked comments'][i]['sorted ranked comments'][j][0])

    return arrAccount, arrComment

# -------------main function-------------
def scrapingAllComments(accOwner, isOwnerInclude):
    komenPerPost = []

    for i in range(0, len(accOwner['GraphImages'])):
        if (accOwner['GraphImages'][i]['comments_disabled'] == False):
            komen = []
            for j in range(0, len(accOwner['GraphImages'][i]['comments']['data'])):
                if (isOwnerInclude == True):
                    komen.append(accOwner['GraphImages'][i]['comments']['data'][j]['text'])
                else:
                    if (accOwner['GraphImages'][i]['comments']['data'][j]['owner']['id'] != accOwner['GraphImages'][i]['owner']['id']):
                        komen.append(accOwner['GraphImages'][i]['comments']['data'][j]['text'])
            komenPerPost.append(komen)
        # else:
        #     print('post no-',i,' komen nya di disabled')

    return komenPerPost

def scrapingCommentAccount(accOwner, rank):
    comAcc = {}
    
    usernameOwner = accOwner['GraphImages'][0]['username']

    for i in range(0, len(accOwner['GraphImages'])):
        # cek komen disable atau tidak
        if (accOwner['GraphImages'][i]['comments_disabled'] == False):
            # cek post ini ada komen nya ga
            if (accOwner['GraphImages'][i]['edge_media_to_comment'] != 0):
                for j in range(0, len(accOwner['GraphImages'][i]['comments']['data'])):
                    # cek komen ini punya owner atau bukan
                    if (accOwner['GraphImages'][i]['comments']['data'][j]['owner']['username'] != usernameOwner):
                        # tambahin @ di nama akun
                        namaAkunSetelahTambahAt = tambahAt(accOwner['GraphImages'][i]['comments']['data'][j]['owner']['username'])
                        # cek akun yg komen ini udah ada atau belum di comAcc 
                        if (namaAkunSetelahTambahAt in comAcc):
                            comAcc[namaAkunSetelahTambahAt] += 1
                        else:
                            comAcc[namaAkunSetelahTambahAt] = 1                            

    hasilSorting = sorted(comAcc.items(), key=itemgetter(1), reverse=True)
    hasilRank = cutRanking(hasilSorting, rank, 'account comment')

    return hasilRank

def scrapingAccountMentionedByUser(accOwner, rank):
    allCommentsFromOwner = []
    allAccName = []
    accMend = {}

    usernameOwner = accOwner['GraphImages'][0]['username']

    for i in range(0, len(accOwner['GraphImages'])):
        # get caption post
        if (len(accOwner['GraphImages'][i]['edge_media_to_caption']['edges']) != 0):
            allCommentsFromOwner.append(accOwner['GraphImages'][i]['edge_media_to_caption']['edges'][0]['node']['text'])

        # cek komen disable atau tidak
        if (accOwner['GraphImages'][i]['comments_disabled'] == False):
            # cek post ini ada komen nya ga
            if (accOwner['GraphImages'][i]['edge_media_to_comment'] != 0):
                for j in range(0, len(accOwner['GraphImages'][i]['comments']['data'])):
                    # cek komen ini punya owner atau bukan
                    if (accOwner['GraphImages'][i]['comments']['data'][j]['owner']['username'] == usernameOwner):
                        allCommentsFromOwner.append(accOwner['GraphImages'][i]['comments']['data'][j]['text'])

    for komen in allCommentsFromOwner:
        allAccName.append(findAllAccountName(komen))

    for post in allAccName:
        for acc in post:
            # cek akun ini udah ada di accMend belum
            if (acc in accMend):
                accMend[acc] += 1
            else:
                accMend[acc] = 1
    
    hasilSorting = sorted(accMend.items(), key=itemgetter(1), reverse=True)
    hasilRank = cutRanking(hasilSorting, rank, 'account mentioned by user')

    return hasilRank

def selectedComments(accOwner, findAccComments):
    selectedComRes = {}

    for data in findAccComments:
        komen = []
        cleanKomen = []
        
        for i in range(0, len(accOwner['GraphImages'])):
            if (accOwner['GraphImages'][i]['comments_disabled'] == False):
                for j in range(0, len(accOwner['GraphImages'][i]['comments']['data'])):
                    accTambahAt = tambahAt(accOwner['GraphImages'][i]['comments']['data'][j]['owner']['username'])
                    if (accTambahAt == data[0]):
                        komen.append(accOwner['GraphImages'][i]['comments']['data'][j]['text'])

        # cleaning komen
        tempClean = []
        for perKomen in komen:
            hasilAN = hapusAccountName(perKomen)
            hasilRE = removeEmoticon(hasilAN)
            tempClean.append(hasilRE)
        cleanKomen = removeNullItemInArr(tempClean)

        selectedComRes[data[0]] = cleanKomen

    return selectedComRes

def getVeryPositiveComments(data, curAcc):
    allPositiveCom = {}
    positiveCom = []
    for i in range(0, len(data['all comments'])):
        temp = {}

        accName = data['all comments'][i]['account name']
        
        # sorting, filtering, cleaning data
        hasilSort = sorted(data['all comments'][i]['comments'], key=itemgetter(1), reverse=True)
        hasilFilterSentiScore = filterSentiScore(hasilSort, 4)
        hasilCut = cutRanking(hasilFilterSentiScore, 3, 'very positive comments')
        if ('EMPTY DATA' not in hasilCut):
            temp['account name'] = accName
            temp['sorted ranked comments'] = hasilCut
            positiveCom.append(temp)
    
    allPositiveCom['account name'] = curAcc
    allPositiveCom['all sorted ranked comments'] = positiveCom

    return allPositiveCom

def getAllPostData(accOwner):
    allDataPost = []

    for i in range(0, len(accOwner['GraphImages'])):
        tempPost = {}

        if(len(accOwner['GraphImages'][i]['edge_media_to_caption']['edges']) != 0):
            caption = removeEmoticon(accOwner['GraphImages'][i]['edge_media_to_caption']['edges'][0]['node']['text'])
        else:
            caption = ''
        if(len(accOwner['GraphImages'][i]['tags']) != 0):
            separator = ', '
            tags = separator.join(accOwner['GraphImages'][i]['tags'])
        else:
            tags = ''
        img = accOwner['GraphImages'][i]['thumbnail_resources'][2]['src']
        time = convertTime(accOwner['GraphImages'][i]['taken_at_timestamp'])
        countLike = accOwner['GraphImages'][i]['edge_media_preview_like']['count']
        if (accOwner['GraphImages'][i]['comments_disabled'] == False):
            countComment = accOwner['GraphImages'][i]['edge_media_to_comment']['count']
        else:
            countComment = ''
        
        tempPost['caption'] = caption
        tempPost['tags'] = tags
        tempPost['image'] = img
        tempPost['time'] = time
        tempPost['count like'] = countLike
        tempPost['count comment'] = countComment
        allDataPost.append(tempPost)

    return allDataPost

# -------------main program-------------
def mainProgramGetJSON(account, inputanRank):
    accOwner = openFile(account)
    
    # cek if json exist ==> if akun private or not
    if (accOwner != 'EMPTY DATA'):
        curAcc = getAccountOwner(accOwner)
        hasilScrapingComAcc = scrapingCommentAccount(accOwner, inputanRank)
        hasilAccMenByUser = scrapingAccountMentionedByUser(accOwner, inputanRank)
        hasilSelCom = selectedComments(accOwner, hasilScrapingComAcc)                  
        hasilGetPost = getAllPostData(accOwner)
        hasilSortLike, hasilSortComment = sortPost(hasilGetPost)

        return hasilScrapingComAcc, hasilAccMenByUser, hasilSelCom, hasilGetPost, hasilSortLike, hasilSortComment, curAcc
    else:
        return 'account is private or have not post anything yet'

# mainProgramGetJSON('../data-instagram/ra.ginda/ra.ginda.json', 3)