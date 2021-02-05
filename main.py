from flask import Flask, request,render_template
import json,os,time
from xpinyin import Pinyin
from datetime import timedelta

class Application(Flask):
    def __init__(self,import_name, template_folder='templates',static_folder='static',root_path=None):
        super(Application,self).__init__(import_name,template_folder=template_folder,root_path=root_path,static_folder=static_folder)
        #self.debug = True
        self.config['SEND_EILE_MAX_AGE_DEFULT']=timedelta(seconds=1)

    def getBooks(self):
        bookList = []
        for root, dirs, files in os.walk('static/library'):
            for i in dirs:
                path = '/static/library/' + i
                print(HandleConfig(path + '/set.ini'))
                iniFile =HandleConfig(os.getcwd() + path + '/set.ini')
                print(path + '/set.ini')
                cover = path + '/' + iniFile.get_value('cover','cover')
                name = iniFile.get_value('name','novelName')
                commentSwitch = iniFile.get_value('commentSwitch','commentSwitch')
                type = iniFile.get_value('type','type')
                comment = iniFile.get_json_data('introduce','introduce')

                userName =comment['data']['comments'][0]['createrId']['userName']
                content =comment['data']['comments'][0]['content']
                createdAt = comment['data']['comments'][0]['createdAt']
                comment = {'userName':userName,'createdAt':createdAt,'content':content}
                print(cover, name, commentSwitch, type, comment)
                from pathlib import Path
                connectFile = Path(os.getcwd() + path + '/OEBPS')
                if connectFile.is_dir():
                    new = False
                else:
                    new = True
                print('new',new)
                bookList.append({'name':name,'cover':cover,'type':type,'commentSwitch':commentSwitch,'comment':comment,'path':path,'new':new})
            return bookList
    def getRes(self):
        styleList = []
        fontList = []
        for root, dirs, files in os.walk('templates/style'):
            for i in dirs:
                styleList.append(i)
        for root, dirs, files in os.walk('static/fontsCss'):
            #print('files',files)
            for i in files:
                fontList.append(i[0:-4])
        return {'styleList':styleList,'fontList':fontList}

app = Application(__name__)


@app.route('/')
def index():
    print(app.getBooks())
    bookItem = ''
    for i in app.getBooks():
        bookItem = bookItem + render_template('bookItem.html'
                                              ,name = i['name']
                                              ,cover = i['cover']
                                              ,introduce = ''
                                              ,path = i['path']
                                              ,comment = i['comment']
                                              ,new = i['new'])
    return render_template('index.html',
                           bookItem = bookItem
                           )


@app.route('/addBook',methods=['POST','GET'])
def addBock():
    file = ''
    path = ''
    if request.method == "GET":
            return render_template('addBook.html')
    elif request.method == "POST":
        try:
            for i in request.form:
                if i == 'name':
                    novelName = request.form['name']
                elif i == 'switchButton':
                    switchButton = request.form['switchButton']
                elif i == 'type':
                    type = request.form['type']
            p = Pinyin()
            for i in range(0, 10000):
                if i == 0:
                    name = novelName
                else:
                    name = novelName + str(i)
                path = './static/library/' + p.get_pinyin(name, '-')
                isExists = os.path.exists(path)
                if not isExists:
                    os.makedirs(path)
                    break
                else:
                    pass
            file = request.files['file']
            filename = file.filename
            separator = []
            # print(filename, file)
            num = 0
            for i in filename:
                if i == '.':
                    separator.append(num)
                num = num + 1
            print(separator[-1])
            file.save(path + '/' + 'cover' + filename[separator[-1]:])

            if name.replace(novelName,'') == '':
                id = 0
            else:
                id = name.replace(novelName,'')

            if switchButton == 'true':
                introduce = getComment(novelName).comment()

            datas = {
                'name': {
                    'id': id,
                    'novelName': novelName,
                },
                'commentSwitch':{
                    'commentSwitch':switchButton,
                },
                'type':{
                    'type':type
                },
                'cover':{
                    'cover':'cover' + filename[separator[-1]:]
                },
                'introduce':{
                    'introduce': introduce
                }
            }
            result = HandleConfig.write_config(datas, path + '/set.ini')

            return {'success': True}
        except:
            import traceback
            traceback.print_exc()
            return {'success': traceback.format_exc()}


@app.route('/loadingBook')
def loadingBook():
    import configparser
    path = request.args.get('path')
    print(path)
    setIni = HandleConfig('.' + path + '/set.ini')
    print(setIni)
    novelName = setIni.get_value('name','novelname')
    imgData = path + '/' + setIni.get_value('cover','cover')
    novelType = setIni.get_value('type','type')
    try :
        launchTime = setIni.get_value('launchTime','launchTime')
    except configparser.NoSectionError:
        launchTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if launchTime == None:
        launchTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        authorName = setIni.get_value('authorName','authorName')
    except configparser.NoSectionError:
        authorName = '未知作者'
    if authorName == None:
        authorName = '未知作者'
    try:
        novelTime = setIni.get_value('novelTime','novelTime')
    except configparser.NoSectionError:
        novelTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if novelTime == None:
        novelTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    tocIni = HandleConfig('.' + path + '/toc.ini')
    history = tocIni.get_int('history','history')
    chapterTitleList = tocIni.get_eval_data('chapterTitleList','chapterTitleList')

    chapterName = chapterTitleList[history-1]
    content = open('.' + path + '/OEBPS/Text/chapter' + str(history) + '.html',mode='r',encoding='utf-8').read()
    chapterWords = len(content)

    try:
        setIni = HandleConfig('.' + path + '/toc.ini')
        styleName = setIni.get_value('styleName','styleName')
    except configparser.NoSectionError:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        styleName = tocSetIni.get_value('styleName', 'styleName')
    if styleName == None:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        styleName = tocSetIni.get_value('styleName', 'styleName')


    try:
        setIni = HandleConfig('.' + path + '/toc.ini')
        fontName = setIni.get_value('fontName','fontName')
    except configparser.NoSectionError:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        fontName = tocSetIni.get_value('fontName', 'fontName')
    if styleName == None:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        fontName = tocSetIni.get_value('fontName', 'fontName')

    indexPath = './style/%s/index.html'%(styleName)
    print('indexPath',indexPath)

    return render_template(indexPath,
                                   history = history,
                                   path = path,
                                   chapterName=chapterName,
                                   novelName=novelName,
                                   authorName=authorName,
                                   chapterWords=chapterWords,
                                   novelTime=novelTime,
                                   content=content,
                                   imgData=imgData,
                                   novelType=novelType,
                                   launchTime=launchTime,
                                   fontName=fontName,
                           )
    '''
    novelName 小说名称 *不为空
    authorName 作者名称
    imgData 封面图片数据流 *不为空
    novelType 小说类型 *不为空
    launchTime 发布时间
    chapterName 章节名称 *不为空
    novelTime 章节发布时间
    content 内容 *不为空
    chapterWords 字数
    '''

@app.route('/nextChapter',methods=['POST'])
def nextChapter():
    import configparser
    path = request.form['path']
    setIni = HandleConfig('.' + path + '/set.ini')
    print(setIni)
    novelName = setIni.get_value('name', 'novelname')
    imgData = path + '/' + setIni.get_value('cover', 'cover')
    novelType = setIni.get_value('type', 'type')
    try:
        launchTime = setIni.get_value('launchTime', 'launchTime')
    except configparser.NoSectionError:
        launchTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if launchTime == None:
        launchTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        authorName = setIni.get_value('authorName', 'authorName')
    except configparser.NoSectionError:
        authorName = '未知作者'
    if authorName == None:
        authorName = '未知作者'
    try:
        novelTime = setIni.get_value('novelTime', 'novelTime')
    except configparser.NoSectionError:
        novelTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if novelTime == None:
        novelTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    tocIni = HandleConfig('.' + path + '/toc.ini')
    history = tocIni.get_int('history', 'history') + 1
    a = tocIni.modify_config('history', 'history',str(history),'.' + path + '/toc.ini')
    print('修改结果：',a)
    chapterTitleList = tocIni.get_eval_data('chapterTitleList', 'chapterTitleList')

    chapterName = chapterTitleList[history - 1]
    content = open('.' + path + '/OEBPS/Text/chapter' + str(history) + '.html', mode='r', encoding='utf-8').read()
    chapterWords = len(content)

    try:
        styleName = setIni.get_value('styleName', 'styleName')
    except configparser.NoSectionError:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        styleName = tocSetIni.get_value('styleName', 'styleName')
    if styleName == None:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        styleName = tocSetIni.get_value('styleName', 'styleName')

    newPagePath = './style/%s/newPage.html' % (styleName)

    return render_template(newPagePath,
                           history=history,
                           path=path,
                           chapterName=chapterName,
                           novelName=novelName,
                           authorName=authorName,
                           chapterWords=chapterWords,
                           novelTime=novelTime,
                           content=content,
                           imgData=imgData,
                           novelType=novelType,
                           launchTime=launchTime,
                           )
@app.route('/lastChapter',methods=['POST'])
def lastChapter():
    import configparser
    path = request.form['path']
    history = int(request.form['history'])-1
    print(path,history)
    setIni = HandleConfig('.' + path + '/set.ini')
    print(setIni)
    novelName = setIni.get_value('name', 'novelname')
    imgData = path + '/' + setIni.get_value('cover', 'cover')
    novelType = setIni.get_value('type', 'type')
    try:
        launchTime = setIni.get_value('launchTime', 'launchTime')
    except configparser.NoSectionError:
        launchTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if launchTime == None:
        launchTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        authorName = setIni.get_value('authorName', 'authorName')
    except configparser.NoSectionError:
        authorName = '未知作者'
    if authorName == None:
        authorName = '未知作者'
    try:
        novelTime = setIni.get_value('novelTime', 'novelTime')
    except configparser.NoSectionError:
        novelTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if novelTime == None:
        novelTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    tocIni = HandleConfig('.' + path + '/toc.ini')

    chapterTitleList = tocIni.get_eval_data('chapterTitleList', 'chapterTitleList')

    chapterName = chapterTitleList[history - 1]
    content = open('.' + path + '/OEBPS/Text/chapter' + str(history) + '.html', mode='r', encoding='utf-8').read()
    chapterWords = len(content)

    try:
        styleName = setIni.get_value('styleName', 'styleName')
    except configparser.NoSectionError:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        styleName = tocSetIni.get_value('styleName', 'styleName')
    if styleName == None:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        styleName = tocSetIni.get_value('styleName', 'styleName')

    newPagePath = './style/%s/newPage.html' % (styleName)

    return render_template(newPagePath,
                           history=history,
                           path=path,
                           chapterName=chapterName,
                           novelName=novelName,
                           authorName=authorName,
                           chapterWords=chapterWords,
                           novelTime=novelTime,
                           content=content,
                           imgData=imgData,
                           novelType=novelType,
                           launchTime=launchTime,
                           )

@app.route('/catalog', methods=['POST'])#获取目录
def getCatalog():
    path = request.form['path']

    def fun(number, recursive_depth=0):
        str_number = str(number)
        if len(str_number) > 4:
            str_number = str_number[-4:]
        bits = "零 一 二 三 四 五 六 七 八 九".split(" ")
        units = " 十 百 千".split(" ")
        large_unit = ' 万 亿 万'.split(" ")  # 可扩展,以万为单位
        number_len = len(str_number)
        result = ""

        for i in range(number_len):
            result += bits[int(str_number[i])]
            if str_number[i] != "0":
                result += units[number_len - i - 1]

        # 去除连续的零
        while "零零" in result:
            result = result.replace("零零", "零")
        # 去除尾部的零
        if result[-1] == "零":
            result = result[:-1]
        # 调整10~20之间的数
        if result[:2] == "一十":
            result = result[1:]
        # 字符串连接上大单位
        result += large_unit[recursive_depth]

        # 判断是否递归
        if len(str(number)) > 4:
            recursive_depth += 1
            return fun(str(number)[:-4], recursive_depth) + result
        else:
            return result

    tocIni = HandleConfig('.' + path + '/toc.ini')
    chaptersNameList = tocIni.get_eval_data('chapterTitleList', 'chapterTitleList')
    history = tocIni.get_int('history', 'history') - 1

    id = 1
    childrenListALL = []
    for i in chaptersNameList:
        childrenListALL.append({'title': i, 'id': id})
        id = id + 1

    catalogList = []
    count = 1
    for i in range(0, len(chaptersNameList) // 100):
        if history < count * 100 + 1 and history > 100 * (count - 1) + 1:  # 历史记录在分卷中，分卷展开
            catalogList.append({'title': '分卷（%s）' % fun(count)
                            , 'spread': 'True'
                            , 'children': childrenListALL[100 * (count - 1):count * 100]
                         })
        else:
            catalogList.append({'title': '分卷（%s）' % fun(count)
                            , 'children': childrenListALL[100 * (count - 1):count * 100]
                         })
        # print(len(chaptersNameList[count-1:count*100]))
        # print(fun(count))
        count = count + 1
    if history > 100 * (count - 1) + 1:  # 历史记录在分卷中，分卷展开
        catalogList.append({'title': '分卷（%s）' % fun(count)
                        , 'spread': 'True'
                        , 'children': childrenListALL[100 * (count - 1):]
                     })
    else:
        catalogList.append({'title': '分卷（%s）' % fun(count)
                        , 'children': childrenListALL[100 * (count - 1):]
                     })
    data = {1:catalogList}
    return data, 201

@app.route('/catalogClick', methods=['POST'])#目录项被点击
def catalogClick():
    import configparser
    path = request.form['path']
    history = int(request.form['id'])

    tocIni = HandleConfig('.' + path + '/toc.ini')
    tocIni.modify_config('history', 'history', str(history), '.' + path + '/toc.ini')

    print(path, history)
    setIni = HandleConfig('.' + path + '/set.ini')
    print(setIni)
    novelName = setIni.get_value('name', 'novelname')
    imgData = path + '/' + setIni.get_value('cover', 'cover')
    novelType = setIni.get_value('type', 'type')
    try:
        launchTime = setIni.get_value('launchTime', 'launchTime')
    except configparser.NoSectionError:
        launchTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if launchTime == None:
        launchTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        authorName = setIni.get_value('authorName', 'authorName')
    except configparser.NoSectionError:
        authorName = '未知作者'
    if authorName == None:
        authorName = '未知作者'
    try:
        novelTime = setIni.get_value('novelTime', 'novelTime')
    except configparser.NoSectionError:
        novelTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if novelTime == None:
        novelTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    tocIni = HandleConfig('.' + path + '/toc.ini')

    chapterTitleList = tocIni.get_eval_data('chapterTitleList', 'chapterTitleList')

    chapterName = chapterTitleList[history - 1]
    content = open('.' + path + '/OEBPS/Text/chapter' + str(history) + '.html', mode='r', encoding='utf-8').read()
    chapterWords = len(content)

    try:
        styleName = setIni.get_value('styleName', 'styleName')
    except configparser.NoSectionError:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        styleName = tocSetIni.get_value('styleName', 'styleName')
    if styleName == None:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        styleName = tocSetIni.get_value('styleName', 'styleName')

    newPagePath = './style/%s/newPage.html' % (styleName)

    return render_template(newPagePath,
                           history=history,
                           path=path,
                           chapterName=chapterName,
                           novelName=novelName,
                           authorName=authorName,
                           chapterWords=chapterWords,
                           novelTime=novelTime,
                           content=content,
                           imgData=imgData,
                           novelType=novelType,
                           launchTime=launchTime,
                           )
@app.route('/bookSet',methods=['POST'])
def bookSet():
    import werkzeug,configparser
    path = request.form['path']
    try:
        fontSize = request.form['fontSize']
        pageWidth = request.form['pageWidth']
        setIni = HandleConfig('.' + path + '/toc.ini')
        if fontSize != None:
            try:
                fontSize = setIni.get_value('fontSize', 'fontSize')
                fontSize = request.form['fontSize']
                setIni.modify_config('fontSize', 'fontSize', str(fontSize), '.' + path + '/toc.ini')
            except configparser.NoSectionError:
                setIni.add_config('fontSize', 'fontSize', str(fontSize), '.' + path + '/toc.ini')
        if pageWidth != None:
            try:
                pageWidth = setIni.get_value('pageWidth', 'pageWidth')
                pageWidth = request.form['pageWidth']
                setIni.modify_config('pageWidth', 'pageWidth', str(pageWidth), '.' + path + '/toc.ini')
            except configparser.NoSectionError:
                setIni.add_config('pageWidth', 'pageWidth', str(pageWidth), '.' + path + '/toc.ini')


    except werkzeug.exceptions.BadRequestKeyError:#没有参数放弃操作
        pass

    try:
        styleName = request.form['styleName']
        print(styleName)
        setIni = HandleConfig('.' + path + '/toc.ini')
        try:
            styleName = setIni.get_value('styleName', 'styleName')
            styleName = request.form['styleName']
            setIni.modify_config('styleName', 'styleName', str(styleName), '.' + path + '/toc.ini')
        except configparser.NoSectionError:
            setIni.add_config('styleName', 'styleName', str(styleName), '.' + path + '/toc.ini')

    except werkzeug.exceptions.BadRequestKeyError:#没有参数放弃操作
        pass

    try:
        fontName = request.form['fontName']
        print(fontName)
        setIni = HandleConfig('.' + path + '/toc.ini')
        try:
            fontName = setIni.get_value('fontName', 'fontName')
            fontName = request.form['fontName']
            setIni.modify_config('fontName', 'fontName', str(fontName), '.' + path + '/toc.ini')
        except configparser.NoSectionError:
            setIni.add_config('fontName', 'fontName', str(fontName), '.' + path + '/toc.ini')

    except werkzeug.exceptions.BadRequestKeyError:#没有参数放弃操作
        pass


    return {'sucess':True}

@app.route('/getBookSet',methods=['POST'])#获取set（字体大小，页面宽度……）
def getBookSet():
    import configparser
    path = request.form['path']
    try:
        setIni = HandleConfig('.' + path + '/toc.ini')
        fontSize = setIni.get_value('fontSize', 'fontSize')
        pageWidth = setIni.get_value('pageWidth', 'pageWidth')
    except configparser.NoSectionError:
        setIni = HandleConfig('.' + '/userData/tocSet.ini')
        fontSize = setIni.get_value('fontSize', 'fontSize')
        pageWidth = setIni.get_value('pageWidth', 'pageWidth')
    return {'fontSize':fontSize,'pageWidth':pageWidth}

@app.route('/getResList',methods=['POST'])#获取资源列表（主题名称，字体）
def getResList():
    import configparser
    path = request.form['path']
    resList = app.getRes()
    styleList = resList['styleList']
    fontList = resList['fontList']
    returnStyleList = []
    returnFontList = []
    try:
        setIni = HandleConfig('.' + path + '/toc.ini')
        styleName = setIni.get_value('styleName','styleName')
    except configparser.NoSectionError:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        styleName = tocSetIni.get_value('styleName', 'styleName')
    if styleName == None:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        styleName = tocSetIni.get_value('styleName', 'styleName')
    for i in styleList:
        if i == styleName:
            returnStyleList.append('<option selected>%s</option>' % i)
        else:
            returnStyleList.append('<option>%s</option>'%i)
    styleStr = ''
    for i in returnStyleList:
        styleStr = styleStr + i


    try:
        setIni = HandleConfig('.' + path + '/toc.ini')
        fontName = setIni.get_value('fontName','fontName')
    except configparser.NoSectionError:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        fontName = tocSetIni.get_value('fontName', 'fontName')
    if fontName == None:
        tocSetIni = HandleConfig('./userData/tocSet.ini')
        fontName = tocSetIni.get_value('fontName', 'fontName')

    for i in fontList:
        if i == fontName:
            returnFontList.append('<option selected>%s</option>' % i)
        else:
            returnFontList.append('<option>%s</option>'%i)
    fontStr = ''
    for i in returnFontList:
        fontStr = fontStr + i

    print('fontStr:',fontStr)

    return {'styleStr':styleStr,'fontStr':fontStr}

@app.route('/uploadTXT',methods=['POST'])
def uploadTXT():
    try:
        print('输出path', request.form['path'])
        path = request.form['path']
        file = request.files['file']
        print(path + '/' + 'total.txt')
        file.save('.' + path + '/' + 'total.txt')
        try:
            connect = open('.' + path + '/' + 'total.txt','r',encoding='utf-8').read()
        except UnicodeDecodeError as e:
            try:
                connect = open('.' + path + '/' + 'total.txt', 'r',encoding='ansi').read()
            except UnicodeDecodeError as e:
                connect = open('.' + path + '/' + 'total.txt', 'r', encoding='gbk').read()
        import re
        pattern = re.compile(r'第[\u4e00-\u9fa5a-zA-Z0-9]{1,7}章.*\n')
        chapterTitleList = pattern.findall(connect)
        result = re.split(pattern,connect)  # 以pattern的值 分割字符串
        chapterConnect = []
        #print(result)
        for i in result:
            if len(i) <= 200 or i == '':
                print(len(i))
                pass
            else:
                chapterConnect.append(i)
        OEBPSpath = '.' + path + '/' + 'OEBPS'

        isExists = os.path.exists(OEBPSpath)

        # 判断结果
        if not isExists:
            os.makedirs(OEBPSpath)
            TextPath = OEBPSpath + '/Text'
            os.makedirs(TextPath)
        num = 1
        for i in chapterConnect:
            i = i.replace('\n','</br>')
            f = open(TextPath + '/chapter' + str(num) + '.html',mode='w',encoding='utf-8')
            f.write(i)
            f.close()
            num = num + 1

        datas = {
            'history':{
                'history':1
                },
            'chapterTitleList':{
                'chapterTitleList':chapterTitleList
                }
            }
        HandleConfig.write_config(datas, '.' + path + '/toc.ini')

        return {'success': True}
    except:
        import traceback
        traceback.print_exc()
        return {'success': traceback.format_exc()}

# 封装读取保存配置文件功能
from configparser import ConfigParser
class HandleConfig:
    """
    配置文件读写数据的封装
    """
    def __init__(self, filename):
        """
        :param filename: 配置文件名
        """
        self.filename = filename
        self.config = ConfigParser()  # 读取配置文件1.创建配置解析器
        self.config.read(self.filename, encoding="utf-8")  # 读取配置文件2.指定读取的配置文件
        ''' self.filename = filename
        with open(self.filename,'r',encoding="utf-8") as f:
            self.text = f.read()'''

    # get_value获取所有的字符串，section区域名, option选项名
    def get_value(self, section, option):
        return self.config.get(section, option)
        '''import pickle
        data = pickle.load(self.text)
        return '''

    # get_int获取整型，section区域名, option选项名
    def get_int(self, section, option):
        return self.config.getint(section, option)

    # get_float获取浮点数类型，section区域名, option选项名
    def get_float(self, section, option):
        return self.config.getfloat(section, option)

    # get_boolean（译：比例恩）获取布尔类型，section区域名, option选项名
    def get_boolean(self, section, option):
        return self.config.getboolean(section, option)

    # get_eval_data 获取列表，section区域名, option选项名
    def get_eval_data(self, section, option):
        return eval(self.config.get(section, option))  # get 获取后为字符串，再用 eval 转换为列表

    def get_json_data(self,section,option):
        import json
        return json.loads(self.config.get(section, option))# get 获取后为字符串，再用json解析

    @staticmethod
    def write_config(datas, filename):
        """
        写入配置操作
        :param datas: 需要传入写入的数据
        :param filename: 指定文件名
        :return:
        """
        # 做校验，为嵌套字典的字典才可以（意思.隐私.谈.ce)
        if isinstance(datas, dict):  # 遍历，在外层判断是否为字典
            # 再来判断内层的 values 是否为字典
            for value in datas.values():    # 先取出value
                if not isinstance(value, dict):     # 在判断
                    return False

            config = ConfigParser()
            for key in datas:
                config[key] = datas[key]

            with open(filename, "w",encoding="utf-8") as file:
                config.write(file)
            return True
    def modify_config(self,section,option,value,fileName):#修改值
        print('修改值')
        print(section,option,value,fileName)
        self.config.set(section, option, value)
        with open(fileName, mode="w",encoding='utf-8')  as  configfile:
            return self.config.write(configfile)

    def add_config(self,section,option,value,fileName):#添加值
        print('add')
        if self.config.has_section(section):
            self.config.set(section, option, value)
            with open(fileName, mode="w", encoding='utf-8')  as  configfile:
                return self.config.write(configfile)
        else:
            self.config.add_section(section)
            self.config.set(section, option, value)
            with open(fileName, mode="w",encoding='utf-8')  as  configfile:
                return self.config.write(configfile)

class getComment:
    def __init__(self,name):
        import requests,json
        res = requests.get('https://www.yousuu.com/api/search?type=title&value='+ name +'&page=1')
        res.encoding = 'utf-8'
        jsonText = json.loads(res.text)
        self.id = jsonText['data']['books'][0]['bookId']
        self.author = jsonText['data']['books'][0]['author']
        self.type = jsonText['data']['books'][0]['tags']
        print(self.id,self.author,self.type)


        comment = requests.get('https://www.yousuu.com/api/book/'+ str(self.id) +'/comment?type=&page=1')
        jsonText = json.loads(comment.text)
        print(jsonText['data']['comments'][0])
        self.returnTxt = comment.text
    def comment(self):
        return self.returnTxt


from PyQt5.QtWidgets import QWidget,QApplication
from PyQt5.QtWidgets import QSystemTrayIcon,QAction,QMenu
from PyQt5.QtGui import QIcon

class occupancyReminder(QWidget):
    def __init__(self, parent=None):
        super(occupancyReminder, self).__init__(parent)

        import psutil
        pid = os.getpid()
        selfProcess = psutil.Process(pid)
        self.parentProcess = psutil.Process(selfProcess.ppid())
        # 设置标题与初始窗口大小
        icon = QIcon('./icon/logo.ico')
        self.QSystemTray = QSystemTrayIcon()
        self.QSystemTray.setIcon(icon)
        self.QSystemTray.show()
        self.QSystemTray.showMessage('LiView_Reader','LiView_Reader已启动！')
        #QSystemTrayIcon.setIcon(icon)
        self.quitAction = QAction(QIcon('./icon/quit.ico'),"&退出", self,triggered=self.quit)

        self.aboutAction = QAction(QIcon('./icon/home.ico'),"&主页面", self,
                                         triggered=self.home)
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.aboutAction)
        self.trayIconMenu.addAction(self.quitAction)
        self.QSystemTray.setContextMenu(self.trayIconMenu)

        self.home()


    def quit(self):
        self.parentProcess.kill()
    def home(self):
        import webbrowser
        webbrowser.open("http://127.0.0.1:5000/")
from threading import Thread
class UItheard(Thread):
    def __init__(self):
        super(UItheard,self).__init__()

    def run(self):
        import sys
        pyapp = QApplication(sys.argv)
        LiView = occupancyReminder()
        pyapp.processEvents()
        # LiView.show()
        sys.exit(pyapp.exec_())


if __name__ == '__main__':
    try:
        a = UItheard()
        a.start()
        app.run(host='127.0.0.1', port=5000)  # 这里指定了地址和端口号。
    except:
        import traceback
        traceback.print_exc()

    #web('牧龙师')
