# -------------import-------------
import json
import operator
from operator import itemgetter
import time
import os
from collections import Counter 
from datetime import datetime
from dateutil import tz
import datetime 
import calendar

# write excel
import openpyxl 
from openpyxl.styles import Font, Alignment, PatternFill, GradientFill
wb = openpyxl.Workbook() 
sheet = wb.active 

# from openpyxl import Workbook
# from openpyxl.styles import Font
# book = Workbook()

def automateIgScraper(userName, destinationFile ,qtyPost):
    # destinationFile = "../data-ig/%s" % (userName)
    os.system('instagram-scraper --comments -m %s %s -d %s --retry-forever' % (qtyPost, userName, destinationFile))
    # destJsonFile = destinationFile + '/%s.json' % (userName)

def openFile(dataAkun):
    exists = os.path.isfile(dataAkun)
    if exists:
        with open(dataAkun, encoding="utf8") as f:
            d = json.load(f)
            data = d
    else:
        data = 'EMPTY DATA'

    return data

def findDay(date): 
    born = datetime.datetime.strptime(date, '%d %m %Y').weekday() 
    return calendar.day_name[born]

def convertTime(timeData):
    ts = time.gmtime(timeData)
    # return time.strftime("%Y-%m-%d", ts)
    return time.strftime('%d %m %Y', ts)

def removeEmoticon(kalimat):
    return kalimat.encode('ascii', 'ignore').decode('ascii')

def countLikes(data):
    counter = 0
    for i in range(0, len(data)):
        if isinstance(data[i]['count like'], str) == False:
            counter += data[i]['count like']
    
    return counter

def countComments(data):
    counter = 0
    for i in range(0, len(data)):
        if isinstance(data[i]['count comment'], str) == False:
            counter += data[i]['count comment']
    
    return counter

def countUsersThatComment(data):
    countUsersThatCommen = {}    
    for i in range(0, len(data)):
        for j in range(0, len(data[i]['Users That Comment'])):
            if data[i]['Users That Comment'][j] in countUsersThatCommen:
                countUsersThatCommen[data[i]['Users That Comment'][j]] += 1
            else:
                countUsersThatCommen[data[i]['Users That Comment'][j]] = 1

    k = Counter(countUsersThatCommen)
    highest = k.most_common(5)
    
    # for i in highest:
    #     print(i[0]," :",i[1]," ") 

    return highest

def getAllPostData(accOwner):
    allDataPost = []

    for i in range(0, len(accOwner['GraphImages'])):
        tempPost = {}
        idPost = accOwner['GraphImages'][i]['id'] 
        if(len(accOwner['GraphImages'][i]['edge_media_to_caption']['edges']) != 0):
            caption = removeEmoticon(accOwner['GraphImages'][i]['edge_media_to_caption']['edges'][0]['node']['text'])
            if(len(accOwner['GraphImages'][i]['tags']) != 0):
                separator = ', '
                tags = separator.join(accOwner['GraphImages'][i]['tags'])
            else:
                tags = ''
        else:
            caption = ''
            tags = ''
        img = accOwner['GraphImages'][i]['thumbnail_resources'][2]['src']
        time = convertTime(accOwner['GraphImages'][i]['taken_at_timestamp'])
        countLike = accOwner['GraphImages'][i]['edge_media_preview_like']['count']
        if (accOwner['GraphImages'][i]['comments_disabled'] == False):
            countComment = accOwner['GraphImages'][i]['edge_media_to_comment']['count']
            usersThatComment = []
            for j in range(0, len(accOwner['GraphImages'][i]['comments']['data'])):
                if accOwner['GraphImages'][i]['comments']['data'][j]['owner']['username'] != username:
                    usersThatComment.append(accOwner['GraphImages'][i]['comments']['data'][j]['owner']['username'])
        else:
            countComment = 0
        
        tempPost['id post'] = idPost
        tempPost['caption'] = caption
        tempPost['tags'] = tags
        tempPost['image'] = img
        tempPost['time'] = time
        tempPost['day'] = findDay(time)
        tempPost['count like'] = countLike
        tempPost['count comment'] = countComment
        tempPost['Users That Comment'] = usersThatComment
        allDataPost.append(tempPost)

    return allDataPost

def writeExcel(data, usersComments, totalPosts, totalLikes, totalComments):
    sheet.merge_cells('G4:H4')
    sheet.title = username
    sheet['A1'] = 'Id Post'
    sheet['B1'] = 'Time'
    sheet['C1'] = 'Interactions'
    sheet['D1'] = 'Likes'
    sheet['E1'] = 'Comments'
    sheet['G1'] = 'Total Posts'
    sheet['H1'] = 'Total Likes'
    sheet['I1'] = 'Total Comments'
    sheet['G4'] = 'Users With Highest Number of Comments'
    sheet['G5'] = 'Users'
    sheet['H5'] = 'Number of Comments'
    # sheet['E1'] = 'Tags'
    # sheet['F1'] = 'Caption'
    # sheet['G1'] = 'Image Url'

    sheet['A1'].font = Font(bold=True)
    sheet['B1'].font = Font(bold=True)
    sheet['C1'].font = Font(bold=True)
    sheet['D1'].font = Font(bold=True)
    sheet['E1'].font = Font(bold=True)
    sheet['G1'].font = Font(bold=True)
    sheet['H1'].font = Font(bold=True)
    sheet['I1'].font = Font(bold=True)
    sheet['G4'].font = Font(bold=True)
    sheet['G5'].font = Font(bold=True)
    sheet['H5'].font = Font(bold=True)
    sheet['G2'].alignment = Alignment(horizontal="center", vertical="center")
    sheet['H2'].alignment = Alignment(horizontal="center", vertical="center")
    sheet['I2'].alignment = Alignment(horizontal="center", vertical="center")
    # sheet['E1'].font = Font(bold=True)
    # sheet['F1'].font = Font(bold=True)
    # sheet['G1'].font = Font(bold=True)

    for i in range(0, len(data)):
        sheet.cell(row=i+2, column=1).value = data[i]['id post']
        sheet.cell(row=i+2, column=2).value = data[i]['time']
        sheet.cell(row=i+2, column=3).value = data[i]['count like'] + data[i]['count comment']
        sheet.cell(row=i+2, column=4).value = data[i]['count like']
        sheet.cell(row=i+2, column=5).value = data[i]['count comment']
        # sheet.cell(row=i+2, column=5).value = data[i]['tags']
        # sheet.cell(row=i+2, column=6).value = data[i]['caption']
        # sheet.cell(row=i+2, column=7).value = data[i]['image']
    
    for i in range(0, len(usersComments)):
        sheet.cell(row=i+6, column=7).value = usersComments[i][0]
        sheet.cell(row=i+6, column=8).value = usersComments[i][1]

    sheet['G2'].value = totalPosts
    sheet['H2'].value = totalLikes
    sheet['I2'].value = totalComments

    wb.save('instagram-analytic-%s.xlsx' % (sheet.title))

def mainProg(username):
    res2 = openFile('../data-ig/%s/%s.json' % (username, username))
    if (res2 != 'EMPTY DATA'):
        allPostsData = getAllPostData(res2)
        totalPosts = len(allPostsData)
        totalLikes = countLikes(allPostsData)
        totalComments = countComments(allPostsData)
        countUsersComment = countUsersThatComment(allPostsData)
        # print(allPostsData)
        writeExcel(allPostsData, countUsersComment, totalPosts, totalLikes, totalComments)
    else:
        print('account is private or have not post anything yet')

# -----------------------------------------Pre-set-----------------------------------------
username = 'ra.ginda'
destFile = "../data-ig/%s" % (username)
maxData = 5

# -----------------------------------------Automate IG Scraper-----------------------------------------
# automateIgScraper(username, destFile, maxData)

# -----------------------------------------Main Program-----------------------------------------
mainProg(username)